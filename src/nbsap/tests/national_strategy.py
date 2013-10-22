# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import StaffUserFactory
from .factories import NationalStrategyFactory, NationalObjectiveFactory
from .factories import AichiGoalFactory, AichiTargetFactory


class NationalStrategyTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_list_national_strategies(self):
        nat_strategy = NationalStrategyFactory()
        aichi_goal = AichiGoalFactory(targets=(nat_strategy.relevant_target,))
        resp = self.app.get(reverse('list_national_strategy'), user='staff')
        self.assertEqual(200, resp.status_code)

        tds = resp.pyquery('.table').find('tbody').find('td')
        objective = nat_strategy.objective
        goal = nat_strategy.relevant_target.get_parent_goal()
        self.assertIn(objective.code, tds[0].text_content())
        self.assertIn(goal.code, tds[1].text_content())

    def test_add_national_strategy(self):
        aichi_target = AichiTargetFactory()
        aichi_goal = AichiGoalFactory(targets=(aichi_target,))
        nat_objective = NationalObjectiveFactory()

        data = {
            'nat_objective': nat_objective.pk,
            'aichi_goal': aichi_goal.pk,
            'aichi_target': aichi_target.pk,
        }
        resp = self.app.get(reverse('edit_national_strategy'), user='staff')
        form = resp.forms['national-strategy-add']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalStrategy', pk=1,
                                    objective=nat_objective,
                                    relevant_target=aichi_target)

    def test_add_national_strategy_fail(self):
        aichi_target = AichiTargetFactory()
        nat_objective = NationalObjectiveFactory()

        data = {
            'nat_objective': nat_objective.pk,
            'aichi_goal': 'invalid_pk',
            'aichi_target': aichi_target.pk,
        }
        resp = self.app.get(reverse('edit_national_strategy'), user='staff')
        form = resp.forms['national-strategy-add']
        self.populate_fields(form, data)
        resp = form.submit()
        self.assertEqual(200, resp.status_code)
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('NationalStrategy', pk=1)


# from django.test.client import Client
# from django.utils import unittest
# from django.test import TestCase
# from django.contrib.auth.models import User
# from django.conf import settings

# from nbsap import models
# from django.conf import settings

# class NationalStrategyTestCase(TestCase):


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
