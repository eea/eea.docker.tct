# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import StaffUserFactory
from .factories import NationalObjectiveFactory, NationalActionFactory


class NationalActionsTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_list_national_objectives(self):
        nat_obj = NationalObjectiveFactory()
        resp = self.app.get(reverse('list_national_objectives'), user='staff')
        self.assertEqual(200, resp.status_code)
        trs = resp.pyquery('.table tr')
        self.assertEqual(1, len(trs))
        self.assertIn(nat_obj.title, trs[0].text_content())

    def test_add_national_objective(self):
        nat_obj = NationalObjectiveFactory.build()
        objective = {
            'language': 'en',
            'title': nat_obj.title_en,
            'description': nat_obj.description_en,
        }
        url = reverse('edit_national_objective')
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-add']
        self.populate_fields(form, objective)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective',
                                    title_en=nat_obj.title_en,
                                    description_en=nat_obj.description_en)

    def test_view_national_objective(self):
        nat_obj = NationalObjectiveFactory()
        url = reverse('view_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)
        titles = resp.pyquery('#objective-title')
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
        titles = resp.pyquery('#action-title')
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
            'title': nat_act.title_en,
            'description': nat_act.description_en,
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-action-add']
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase('NationalAction', pk=1,
                                    title_en=nat_act.title_en,
                                    description_en=nat_act.description_en)

    def test_add_national_action_with_encodings(self):
        nat_obj = NationalObjectiveFactory()
        nat_act = NationalActionFactory.build()
        url = reverse('edit_national_action', kwargs={'objective': nat_obj.pk})
        data = {
            'language': 'en',
            'title': nat_act.title_en,
            'description': 'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
        }
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-action-add']
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase('NationalAction', pk=1,
                                    title_en=nat_act.title_en,
                                    description_en=data['description'])

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

        self.assertObjectInDatabase('NationalAction', pk=1,
                                    title_en='action_edited',
                                    description_en='description_edited')

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

        self.assertObjectInDatabase('NationalAction', pk=1,
                                    description_en=data['description'])

    def test_delete_national_action(self):
        nat_act = NationalActionFactory()
        nat_obj = NationalObjectiveFactory(actions=(nat_act,))
        url = reverse('delete_national_action', kwargs={
            'objective': nat_obj.pk,
            'pk': nat_act.pk,
        })
        self.app.delete(url, user='staff')

        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('NationalAction', pk=1)
