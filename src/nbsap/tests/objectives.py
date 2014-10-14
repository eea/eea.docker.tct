# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import NationalObjectiveFactory, NationalActionFactory
from .factories import StaffUserFactory


class NationalObjectiveTest(BaseWebTest):

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
        data = {
            'language': 'en',
            'title': nat_obj.title_en,
            'description': nat_obj.description_en,
        }
        url = reverse('edit_national_objective')
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-add']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=1,
                                    title_en=nat_obj.title_en,
                                    description_en=nat_obj.description_en)

    def test_add_national_objective_with_encodings(self):
        nat_obj = NationalObjectiveFactory.build()
        data = {
            'language': 'en',
            'title': nat_obj.title_en,
            'description': 'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
        }
        url = reverse('edit_national_objective')
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-add']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=1,
                                    title_en=nat_obj.title_en,
                                    description_en=data['description'])

    def test_edit_national_objective(self):
        nat_obj = NationalObjectiveFactory()
        data = {
            'language': 'en',
            'code': nat_obj.code,
            'title': 'Title edited',
            'description': 'Description edited',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=1,
                                    title_en=data['title'],
                                    description_en=data['description'])

    def test_edit_national_objective_code_updates_subobjective_code(self):
        """Test code prefix of subobjective is changed on parent code edit."""
        nat_obj = NationalObjectiveFactory()
        old_code = '1.1'
        nat_subobj = NationalObjectiveFactory(parent=nat_obj, code=old_code)
        edited_code = '42'
        data = {
            'language': 'en',
            'code': edited_code,
            'title': nat_obj.title,
            'description': nat_obj.description,
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()

        self.assertObjectInDatabase('NationalObjective', pk=2,
                                    title_en=nat_subobj.title_en,
                                    description_en=nat_subobj.description_en,
                                    code='{0}.1'.format(edited_code),
                                    parent=nat_obj)

    def test_edit_national_objective_fail_code(self):
        nat_obj = NationalObjectiveFactory()
        nat_obj_2 = NationalObjectiveFactory()
        data = {
            'language': 'en',
            'code': nat_obj_2.code,
            'title': 'Title edited',
            'description': 'Description edited',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        resp = form.submit()
        self.assertEqual(200, resp.status_code)
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('NationalObjective', pk=1,
                                        title_en=data['title'],
                                        description_en=data['description'])

    def test_edit_national_objective_with_encodings(self):
        nat_obj = NationalObjectiveFactory()
        data = {
            'language': 'en',
            'code': nat_obj.code,
            'title': 'Title edited',
            'description': 'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        self.assertEqual(200, resp.status_code)

        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=1,
                                    title_en=data['title'],
                                    description_en=data['description'])

    def test_delete_national_objective(self):
        nat_obj = NationalObjectiveFactory()
        url = reverse('delete_national_objective', kwargs={'pk': nat_obj.pk})
        resp = self.app.get(url, user='staff').follow()
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('NationalObjective', pk=1)


class ObjectivesTest(BaseWebTest):

    def setUp(self):
        NationalActionFactory.reset_sequence()

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
        self.assertIn('Action 1', action_title[0].text_content())
        self.assertIn('(action1_title_en)', action_title[0].text_content())
