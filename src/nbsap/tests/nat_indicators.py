# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import StaffUserFactory
from .factories import NationalIndicatorFactory

class NationalIndicatorsTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_list_national_indicators(self):
        nat_indicator = NationalIndicatorFactory()
        resp = self.app.get(reverse('list_nat_indicators'), user='staff')
        self.assertEqual(200, resp.status_code)
        trs = resp.pyquery('.table tr')
        self.assertEqual(2, len(trs))
        self.assertIn(nat_indicator.title, trs[1].text_content())

    def test_view_simple_national_indicator(self):
        nat_indicator = NationalIndicatorFactory()
        url = reverse('view_nat_indicator',
                      kwargs={'pk': nat_indicator.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        title = resp.pyquery('.page-title')
        self.assertEqual(1, len(title))
        cleaned_title = ' '.join(title[0].text_content().split())
        expected_title = 'Indicator {}: {}'.format(nat_indicator.code,
                                                   nat_indicator.title)

        self.assertEqual(expected_title, cleaned_title)

    def test_add_national_indicator(self):
        nat_indicator = NationalIndicatorFactory()
        url = reverse('edit_nat_indicator')
        data = {
            'code': '01',
            'language': 'en',
            'title': nat_indicator.title_default,
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms[0]
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase(
            'NationalIndicator',
            {
                'pk': nat_indicator.pk,
                'title_default': nat_indicator.title_default,
            }
        )


    def test_edit_national_indicator(self):
        nat_indicator = NationalIndicatorFactory()
        url = reverse('edit_nat_indicator',
                      kwargs={'pk': nat_indicator.pk})
        data = {
            'title': 'Title edited',
        }
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        form = resp.forms['national-indicator-edit']
        self.populate_fields(form, data)
        form.submit()
        self.assertObjectInDatabase(
            'NationalIndicator',
            {
                'pk': nat_indicator.pk,
                'title_default': data['title'],
            }
        )

    def test_delete_national_indicator(self):
        nat_indicator = NationalIndicatorFactory()
        url = reverse('delete_nat_indicator', kwargs={'pk': nat_indicator.pk})
        self.app.post(url, user='staff').follow()
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase(
                'NationalIndicator',
                {
                    'pk': nat_indicator.pk,
                }
            )
