# from django.test.client import Client
# from django.utils import unittest
# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.conf import settings

# from nbsap import models
# from django.conf import settings

# class NationalStrategyTestCase(TestCase):
#     fixtures = ['be_actions.json', 'be_objectives.json', ]

#     def __init__(self, *args, **kwargs):
#         if settings.EU_STRATEGY:
#             self.fixtures.append('be_mapping_with_eu.json')
#         else:
#             self.fixtures.append('be_mapping_no_eu.json')

#         super(NationalStrategyTestCase, self).__init__(*args, **kwargs)

#     def setUp(self):
#         self.user = User.objects.create_user('test_admin', 'test@admin.com', 'q')
#         self.client = Client()
#         self.user.is_staff = True
#         self.user.save()

#         call = self.client.post('/accounts/login/', {'username': 'test_admin',
#                                                      'password': 'q'})

#     def test_list_national_strategies(self):
#         response = self.client.get('/administration/mapping/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.context['strategies']), 47)
#         content = response.content
#         self.assertIn("Delete", content)
#         self.assertIn("Add Mapping", content)
#         self.assertIn("Edit", content)

#     def test_add_national_strategy_only_with_required_fields(self):
#         mydata = {
#             'nat_objective': 2,
#             'aichi_goal': 'a',
#             'aichi_target': 4
#         }

#         response = self.client.get('/administration/mapping/add')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/mapping/add',
#                                     mydata,
#                                     follow= True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Mapping successfully added", response.content)

#         strategies = models.NationalStrategy.objects.all()
#         added_strategy = strategies[len(strategies)- 1]
#         self.assertEqual(added_strategy.objective.id, mydata['nat_objective'])
#         self.assertEqual(added_strategy.relevant_target.id,
#                          mydata['aichi_target'])
#         self.assertEqual(added_strategy.relevant_target.get_parent_goal().code,
#                          mydata['aichi_goal'])

#     def test_add_national_strategy_only_with_incorrect_goal(self):
#         mydata = {
#             'nat_objective': 2,
#             'aichi_goal': 'b',
#             'aichi_target': 4
#         }
#         response = self.client.post('/administration/mapping/add',
#                                     mydata,
#                                     follow= True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Mapping successfully added", response.content)


#         strategies = models.NationalStrategy.objects.all()
#         added_strategy = strategies[len(strategies) - 1]
#         self.assertFalse(added_strategy.relevant_target.get_parent_goal().code  ==  mydata['aichi_goal'])

#     def test_add_national_strategy_only_with_all_fields(self):
#         mydata = {
#             'nat_objective': 2,
#             'aichi_goal': 'b',
#             'aichi_target': 5,
#             'other_targets': [1,3],
#             'eu_targets': [4],
#             'eu_actions': [36]
#         }

#         response = self.client.post('/administration/mapping/add',
#                                     mydata,
#                                     follow= True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Mapping successfully added", response.content)

#         strategies = models.NationalStrategy.objects.all()
#         added_strategy = strategies[len(strategies)- 1]
#         self.assertEqual(added_strategy.objective.id, mydata['nat_objective'])
#         self.assertEqual(added_strategy.relevant_target.id,
#                          mydata['aichi_target'])
#         self.assertEqual(added_strategy.relevant_target.get_parent_goal().code,
#                          mydata['aichi_goal'])

#         for target in added_strategy.other_targets.all():
#             self.assertIn(target.id, mydata['other_targets'])
#         self.assertEqual(len(added_strategy.other_targets.all()),
#                          len(mydata['other_targets']))

#         if settings.EU_STRATEGY:
#             for target in added_strategy.eu_targets.all():
#                 self.assertIn(target.id, mydata['eu_targets'])
#             for target in added_strategy.eu_actions.all():
#                 self.assertIn(target.id, mydata['eu_actions'])

#             self.assertEqual(len(added_strategy.eu_targets.all()),
#                              len(mydata['eu_targets']))
#             self.assertEqual(len(added_strategy.eu_actions.all()),
#                              len(mydata['eu_actions']))



#     def test_delete_national_strategy(self):
#         mydata = {
#             'nat_objective': 2,
#             'aichi_goal': 'b',
#             'aichi_target': 5,
#             'other_targets': [1,3],
#             'eu_targets': [4],
#             'eu_actions': [36]
#         }
#         response = self.client.post('/administration/mapping/add',
#                                     mydata,
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)

#         strategies = models.NationalStrategy.objects.all()
#         added_strategy = strategies[len(strategies)- 1]
#         my_id = added_strategy.id
#         response = self.client.get('/administration/mapping/%s/delete' %
#                                    (str(my_id)))
#         strategies = models.NationalStrategy.objects.all().filter(id=my_id)
#         if strategies:
#           self.assertEqual(1,2)



#     def test_edit_national_strategy_with_all(self):
#         mydata = {
#             'nat_objective': 2,
#             'aichi_goal': 'b',
#             'aichi_target': 5,
#             'other_targets': [1,3],
#             'eu_targets': [4],
#             'eu_actions': [36]
#         }
#         response = self.client.get('/administration/mapping/1/add')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/mapping/1/add',
#                                     mydata,
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Saved changes", response.content)

#         strategy = models.NationalStrategy.objects.all().filter(id=1)[0]
#         self.assertEqual(strategy.objective.id, mydata['nat_objective'])
#         self.assertEqual(strategy.relevant_target.id, mydata['aichi_target'])

#         for target in strategy.other_targets.all():
#             self.assertIn(target.id, mydata['other_targets'])
#         self.assertEqual(len(strategy.other_targets.all()),
#                          len(mydata['other_targets']))

#         if settings.EU_STRATEGY:
#             for target in strategy.eu_targets.all():
#                 self.assertIn(target.id, mydata['eu_targets'])
#             for target in strategy.eu_actions.all():
#                 self.assertIn(target.id, mydata['eu_actions'])

#             self.assertEqual(len(strategy.eu_targets.all()),
#                              len(mydata['eu_targets']))
#             self.assertEqual(len(strategy.eu_actions.all()),
#                              len(mydata['eu_actions']))

#     def test_edit_national_strategy_with_required_fields(self):
#         mydata = {
#             'nat_objective': 2,
#             'aichi_goal': 'b',
#             'aichi_target': 5,
#         }
#         response = self.client.get('/administration/mapping/1/add')
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post('/administration/mapping/1/add',
#                                     mydata,
#                                     follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Saved changes", response.content)

#         strategy = models.NationalStrategy.objects.all().filter(id=1)[0]
#         self.assertEqual(strategy.objective.id, mydata['nat_objective'])
#         self.assertEqual(strategy.relevant_target.id, mydata['aichi_target'])

#         self.assertEqual(len(strategy.other_targets.all()), 0)

#         if settings.EU_STRATEGY:
#             self.assertEqual(len(strategy.eu_targets.all()), 0)
#             self.assertEqual(len(strategy.eu_actions.all()), 0)



#     def tearDown(self):
#         self.user.delete()
