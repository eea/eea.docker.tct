# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import StaffUserFactory
from .factories import NationalObjectiveFactory, NationalActionFactory


class NationalActionsTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_view_national_objective(self):
        nat_obj = NationalObjectiveFactory()
        url = reverse('view_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        titles = resp.pyquery('.page-title')
        self.assertEqual(1, len(titles))
        expected_title = 'Objective {}: {}'.format(nat_obj.code,
                                                   nat_obj.title)
        self.assertEqual(expected_title, titles[0].text_content())

    def test_list_national_sub_objectives(self):
        nat_obj = NationalObjectiveFactory()
        nat_sub_obj = NationalObjectiveFactory(parent=nat_obj)
        url = reverse('view_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        trs = resp.pyquery('.table tr')
        self.assertEqual(2, len(trs))
        self.assertIn(nat_sub_obj.title, trs[0].text_content())

    def test_list_national_actions(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        url = reverse('view_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        trs = resp.pyquery('.table tr')
        self.assertEqual(2, len(trs))
        self.assertIn(nat_act.title, trs[1].text_content())

    def test_view_national_action(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        url = reverse('view_national_action', kwargs={'objective': nat_obj.pk,
                                                      'pk': nat_act.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        expected_title = 'Action {}: {}'.format(nat_act.code,
                                                nat_act.title)
        titles = resp.pyquery('.page-title')
        self.assertEqual(1, len(titles))
        self.assertEqual(expected_title, titles[0].text_content())

        descriptions = resp.pyquery('div.admin-obj-description')
        self.assertEqual(1, len(descriptions))
        self.assertIn(nat_act.description, descriptions[0].text_content())

    def test_add_national_action(self):
        nat_obj = NationalObjectiveFactory()
        nat_act = NationalActionFactory.build()
        url = reverse('edit_national_action', kwargs={'objective': nat_obj.pk})
        data = {
            'language': 'en',
            'title': nat_act.title_default,
            'description': nat_act.description_default,
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-action-add']
        self.populate_fields(form, data)
        form.submit()

        self.assertObjectInDatabase(
            'NationalAction',
            {
                'pk': 1,
                'title_default': nat_act.title_default,
                'description_default__contains': nat_act.description_default,
            }
        )

    def test_add_national_action_with_encodings(self):
        nat_obj = NationalObjectiveFactory()
        nat_act = NationalActionFactory.build()
        url = reverse('edit_national_action', kwargs={'objective': nat_obj.pk})
        data = {
            'language': 'en',
            'title': nat_act.title_default,
            'description': 'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-action-add']
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase(
            'NationalAction',
            {
                'pk': 1,
                'title_default': nat_act.title_default,
                'description_default__contains': data['description'],
            }
        )

    def test_edit_national_action(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        url = reverse('edit_national_action', kwargs={
            'objective': nat_obj.pk,
            'pk': nat_act.pk,
        })
        data = {
            'language': 'en',
            'title': 'action_edited',
            'description': 'description_edited',
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-action-edit']
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase(
            'NationalAction',
            {
                'pk': 1,
                'title_default': 'action_edited',
                'description_default__contains': 'description_edited',
            }
        )

    def test_edit_national_action_with_encodings(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        url = reverse('edit_national_action', kwargs={
            'objective': nat_obj.pk,
            'pk': nat_act.pk,
        })
        data = {
            'language': 'en',
            'description': 'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-action-edit']
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase(
            'NationalAction',
            {
                'pk': 1,
                'description_default__contains': data['description'],
            }
        )

    def test_delete_national_action(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        url = reverse('delete_national_action', kwargs={
            'objective': nat_obj.pk,
            'pk': nat_act.pk,
        })
        self.app.post(url, user='staff')

        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase(
                'NationalAction',
                {
                    'pk': 1,
                }
            )
