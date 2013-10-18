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

        self.assertObjectInDatabase('NationalAction', pk=1)

# class NationalActionTestCase(TestCase):

#     # def __init__(self, *args, **kwargs):
#     #     if settings.EU_STRATEGY:
#     #         self.fixtures = ['be_mapping_with_eu.json']
#     #     else:
#     #         self.fixtures = ['be_mapping_no_eu.json']

#     #     super(NationalActionTestCase, self).__init__(*args, **kwargs)

#     def setUp(self):
#         self.user = User.objects.create_user('admin',
#                                              'jd@example.com',
#                                             'admin')
#         self.user.is_staff = True
#         self.user.save()

#         self.client = Client()
#         # blind call to set user info on session
#         call = self.client.post('/accounts/login/',
#                                 {'username': 'test_admin',
#                                  'password': 'q'})

#     def test_list_national_action(self):
#         """ Listing National objective 1.1's actions """
#         response = self.client.get('/administration/objectives/16')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Actions related to objective 1.1', response.content)

#     def test_view_national_action(self):
#         """ Test the view of national action """
#         response = self.client.get('/administration/objectives/16/actions/1/')
#         self.assertEqual(response.status_code, 200)
#         content = response.content
#         self.assertIn("Biological Evaluation Maps (BWK)", content)

#     def test_edit_national_action(self):
#         """ Test editing national action for objective's 1.1 """
#         mydata = {
#             'language': 'en',
#             'description': 'My new description'
#         }

#         response = self.client.get('/administration/objectives/16/actions/1/edit')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/objectives/16/actions/1/edit',
#                                     mydata,
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Saved changes", response.content)

#         edited_object = models.NationalAction.objects.all().filter(id=1)[0]
#         self.assertEqual(edited_object.description, mydata['description'])

#     def test_edit_national_action_with_encodings(self):
#         """ Test editing national action for Objective 1.1's """
#         mydata = {
#             'language': 'en',
#             'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF'
#         }

#         response = self.client.get('/administration/objectives/16/actions/1/edit')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/objectives/16/actions/1/edit',
#                                     mydata,
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Saved changes", response.content)

#         edited_object = models.NationalAction.objects.all().filter(id=1)[0]
#         self.assertEqual(edited_object.description, mydata['description'])

#     def test_add_national_action(self):
#         """ Test national action adding """
#         mydata = {
#             'objective': {
#                             'language': 'en',
#                             'title': 'My new objective title',
#                             'description': 'My new objective description'
#             },
#             'action': {
#                         'language': 'en',
#                         'description': 'My new action description'
#                 }

#         }
#         # add an objective first
#         response = self.client.get('/administration/objectives/add/')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/objectives/add/', mydata['objective'])
#         added_object = models.NationalObjective.objects.all().filter(code='16')[0]
#         self.assertEqual(added_object.title, mydata['objective']['title'])
#         self.assertEqual(added_object.description, mydata['objective']['description'])

#         # secondly, add a specific action
#         response = self.client.get('/administration/objectives/101/actions/add')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/objectives/101/actions/add',
#                                     mydata['action'],
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Action successfully added", response.content)

#         added_action = models.NationalAction.objects.filter(id=78)[0]
#         self.assertEqual(added_action.description, mydata['action']['description'])


#         # clean the mess by deleting the action
#         action_id = str(added_action.id)
#         response = self.client.get('/administration/objectives/101/actions/%s/delete' % action_id)

#         # clean the mess by deleting the objective
#         response = self.client.get('/administration/objectives/%s/delete' % (str(added_object.id)))

#     def test_add_national_action_with_encodings(self):
#         """ Test national action adding with encodings """
#         mydata = {
#             'objective': {
#                             'language': 'en',
#                             'title': 'My new objective title',
#                             'description': 'My new objective description'
#             },
#             'action': {
#                         'language': 'en',
#                         'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF'
#             }

#         }
#         # add an objective first
#         response = self.client.get('/administration/objectives/add/')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/objectives/add/', mydata['objective'])
#         added_object = models.NationalObjective.objects.all().filter(code='16')[0]
#         self.assertEqual(added_object.title, mydata['objective']['title'])
#         self.assertEqual(added_object.description, mydata['objective']['description'])

#         # secondly, add a specific action
#         objective_id = str(added_object.id)
#         response = self.client.get('/administration/objectives/%s/actions/add' % objective_id)
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/objectives/%s/actions/add' % objective_id,
#                                     mydata['action'],
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Action successfully added", response.content)

#         added_action = models.NationalAction.objects.filter(code=16)[0]
#         self.assertEqual(added_action.description, mydata['action']['description'])

#         # clean the mess by deleting the action
#         action_id = str(added_action.id)
#         response = self.client.get('/administration/objectives/101/actions/%s/delete' % action_id)

#         # clean the mess by deleting the objective
#         response = self.client.get('/administration/objectives/%s/delete' % (str(added_object.id)))

#     def test_delete_national_action(self):
#         """ Test national action deleting - Objective 1.2's action deleted """

#         _object = models.NationalAction.objects.all().filter(id='2')[0]
#         self.assertIn('fauna of the Brussels Capital Region.', _object.description)

#         response = self.client.get('/administration/objectives/17/actions/2/delete')

#         try:
#             _object = models.NationalAction.objects.all().filter(id='2')[0]
#         except:
#             pass
#         else:
#             # something went wrong when deleting
#             self.assertEqual(1,2)

#     def tearDown(self):
#          self.user.delete()
