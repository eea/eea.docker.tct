# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import NationalObjectiveFactory, NationalActionFactory
from .factories import StaffUserFactory


class ObjectivesTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_list_objectives(self):
        nat_obj = NationalObjectiveFactory()
        resp = self.app.get(reverse('nat_strategy'))
        self.assertEqual(200, resp.status_code)
        h1 = resp.pyquery('h1')
        h1_expected = 'Objective %s: %s' % (nat_obj.code, nat_obj.title)
        description = resp.pyquery('.objective-description')
        self.assertEqual(1, len(h1))
        self.assertEqual(1, len(description))
        self.assertEqual(h1_expected, h1[0].text_content())
        self.assertIn(nat_obj.description, description[0].text_content())

    def test_view_objective(self):
        nat_obj = NationalObjectiveFactory()
        url = reverse('nat_strategy', kwargs={'code': nat_obj.code})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        h1 = resp.pyquery('h1')
        h1_expected = 'Objective %s: %s' % (nat_obj.code, nat_obj.title)
        description = resp.pyquery('.objective-description')
        self.assertEqual(1, len(h1))
        self.assertEqual(1, len(description))
        self.assertEqual(h1_expected, h1[0].text_content())
        self.assertIn(nat_obj.description, description[0].text_content())

    def test_list_objectives_when_database_empty(self):
        resp = self.app.get(reverse('nat_strategy'))
        self.assertEqual(200, resp.status_code)
        content = resp.pyquery('.homepage_view')
        self.assertEqual(1, len(content))
        self.assertIn('No objectives found', content[0].text_content())

    def test_view_objective_when_database_empty(self):
        url = reverse('nat_strategy', kwargs={'code': '1'})
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        content = resp.pyquery('.homepage_view')
        self.assertEqual(1, len(content))
        self.assertIn('No objectives found', content[0].text_content())

    def test_view_implementation(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        resp = self.app.get(reverse('implementation'))
        self.assertEqual(200, resp.status_code)
        h1 = resp.pyquery('h1')
        h1_expected = 'Actions related to Objective %s: %s' % (nat_obj.code,
                                                               nat_obj.title)
        actions = resp.pyquery('.element_field')
        self.assertEqual(1, len(h1))
        self.assertEqual(h1_expected, h1[0].text_content().strip())
        self.assertEqual(1, len(actions))
        action_title = actions.find('h2')
        self.assertEqual(1, len(action_title))
        self.assertEqual('Action 1', action_title[0].text_content())
