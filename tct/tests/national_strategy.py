# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import (
    StaffUserFactory, NationalStrategyFactory, NationalObjectiveFactory,
    AichiGoalFactory, AichiTargetFactory
)


class NationalStrategyTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_list_national_strategies(self):
        nat_strategy = NationalStrategyFactory()
        resp = self.app.get(reverse('list_national_strategy'), user='staff')
        self.assertEqual(200, resp.status_code)

        tds = resp.pyquery('.table').find('tbody').find('td')
        objective = nat_strategy.objective
        goals = ', '.join(g.code for g in nat_strategy.get_goals)
        self.assertIn(objective.code, tds[0].text_content())
        self.assertIn(goals, tds[1].text_content())

    def test_add_national_strategy(self):
        aichi_target = AichiTargetFactory(__sequence=1)
        aichi_goal = AichiGoalFactory(targets=(aichi_target,))
        nat_objective = NationalObjectiveFactory()

        data = {
            'nat_objective': nat_objective.pk,
            'aichi_goals': aichi_goal.code,
            'aichi_targets': aichi_target.code,
        }

        resp = self.app.get(reverse('edit_national_strategy'), user='staff')
        form = resp.forms['national-strategy-add']
        self.populate_fields(form, data)
        form.submit().follow()

        obj = self.assertObjectInDatabase(
            'NationalStrategy',
            {
                'pk': 1,
                'objective': nat_objective,
            }
        )
        self.assertEqual(list(obj.relevant_targets.all()), [aichi_target])

    def test_add_national_strategy_fail(self):
        aichi_target = AichiTargetFactory(__sequence=1)
        nat_objective = NationalObjectiveFactory()

        data = {
            'nat_objective': nat_objective.pk,
            'aichi_goals': 'invalid_pk',
            'aichi_targets': aichi_target.code,
        }
        resp = self.app.get(reverse('edit_national_strategy'), user='staff')
        form = resp.forms['national-strategy-add']
        self.populate_fields(form, data)
        resp = form.submit()
        self.assertEqual(200, resp.status_code)
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase(
                'NationalStrategy',
                {
                    'pk': 1,
                }
            )

    def test_delete_national_strategy(self):
        nat_strategy = NationalStrategyFactory()
        url = reverse('delete_national_strategy',
                      kwargs={'strategy': nat_strategy.pk})
        self.app.get(url, user='staff').follow()
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase(
                'NationalStrategy',
                {
                    'pk': 1,
                }
            )

    def test_edit_national_strategy(self):
        nat_strategy = NationalStrategyFactory()
        nat_objective_for_edit = NationalObjectiveFactory()
        targets = [t.id for t in nat_strategy.relevant_targets.all()]
        AichiGoalFactory(targets=targets)
        goals = [g.code for g in nat_strategy.get_goals]
        data = {
            'nat_objective': nat_objective_for_edit.pk,
            'aichi_goals': goals,
            'aichi_targets': [t.code
                              for t in nat_strategy.relevant_targets.all()],
        }
        url = reverse('edit_national_strategy', kwargs={'pk': nat_strategy.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-strategy-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase(
            'NationalStrategy',
            {
                'pk': 1,
                'objective': nat_objective_for_edit.pk,
            }
        )
