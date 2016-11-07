# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import (
    AichiGoalFactory, AichiTargetFactory,
    CMSGoalFactory, CMSTargetFactory,
    RamsarGoalFactory, RamsarTargetFactory
)


class AichiTest(BaseWebTest):
    def test_aichi_homepage(self):
        aichi_target = AichiTargetFactory(code='1')
        aichi_goal = AichiGoalFactory(code='a', targets=(aichi_target,))
        resp = self.app.get(reverse('aichi_home'))
        self.assertEqual(200, resp.status_code)

        # Test Goal title and description
        title = resp.pyquery('h1.goal-title')
        title_expected = 'Aichi Goal %s:' % (aichi_goal.code.upper())
        self.assertEqual(title_expected, title[0]
                         .text_content().rstrip().strip())
        description = resp.pyquery('h1.goal-desc')
        self.assertEqual(aichi_goal.description, description[0]
                         .text_content().rstrip().strip())

        # Test Target title and description
        title = resp.pyquery('div.section h2')
        title_expected = 'Aichi Target %s' % (aichi_target.code)
        self.assertEqual(title_expected, title[0]
                         .text_content().rstrip().strip())
        description = resp.pyquery('p.target-description')
        self.assertEqual(aichi_target.description, description[0]
                         .text_content().rstrip().strip())

    def test_list_aichi_targets_without_goal(self):
        AichiTargetFactory.create_batch(2)
        resp = self.app.get(reverse('list_targets'))
        self.assertEqual(200, resp.status_code)
        targets = resp.pyquery('ul.list-targets-wrapper li')
        self.assertEqual(2, targets.length)

    def test_list_aichi_targets_with_goal(self):
        AichiTargetFactory()
        aichi_target = AichiTargetFactory()
        aichi_goal = AichiGoalFactory(targets=(aichi_target,))
        resp = self.app.get(
            reverse('list_targets', kwargs={'code': aichi_goal.code}))
        self.assertEqual(200, resp.status_code)
        targets = resp.pyquery('ul.list-targets-wrapper li')
        self.assertEqual(1, targets.length)

    def test_list_aichi_goals(self):
        AichiGoalFactory.create_batch(2)
        resp = self.app.get(reverse('list_goals'))
        self.assertEqual(200, resp.status_code)

        goals = resp.pyquery('ul.list-goals-wrapper li')
        self.assertEqual(2, goals.length)


class CMSTest(BaseWebTest):
    def test_cms_homepage(self):
        cms_target = CMSTargetFactory(code='1')
        cms_goal = CMSGoalFactory(code='1', targets=(cms_target,))
        resp = self.app.get(reverse('cms_home'))
        self.assertEqual(200, resp.status_code)

        # Test Goal title and description
        title = resp.pyquery('h1.goal-title')
        title_expected = 'CMS Goal %s:' % (cms_goal.code)
        self.assertEqual(title_expected, title[0]
                         .text_content().rstrip().strip())
        description = resp.pyquery('h1.goal-desc')
        self.assertEqual(cms_goal.description, description[0]
                         .text_content().rstrip().strip())

        # Test Target title and description
        title = resp.pyquery('div.section h2')
        title_expected = 'CMS Target %s' % (cms_target.code)
        self.assertEqual(title_expected, title[0]
                         .text_content().rstrip().strip())
        description = resp.pyquery('p.target-description')
        self.assertEqual(cms_target.description, description[0]
                         .text_content().rstrip().strip())

    def test_list_cms_targets_without_goal(self):
        CMSTargetFactory.create_batch(2)
        resp = self.app.get(reverse('list_cms_targets'))
        self.assertEqual(200, resp.status_code)
        targets = resp.pyquery('ul.list-targets-wrapper li')
        self.assertEqual(2, targets.length)

    def test_list_cms_targets_with_goal(self):
        CMSTargetFactory()
        cms_target = CMSTargetFactory()
        cms_goal = CMSGoalFactory(targets=(cms_target,))
        resp = self.app.get(
            reverse('list_cms_targets', kwargs={'code': cms_goal.code}))
        self.assertEqual(200, resp.status_code)
        targets = resp.pyquery('ul.list-targets-wrapper li')
        self.assertEqual(1, targets.length)

    def test_list_cms_goals(self):
        CMSGoalFactory.create_batch(2)
        resp = self.app.get(reverse('list_cms_goals'))
        self.assertEqual(200, resp.status_code)

        goals = resp.pyquery('ul.list-goals-wrapper li')
        self.assertEqual(2, goals.length)


class RamsarTest(BaseWebTest):
    def test_ramsar_homepage(self):
        ramsar_target = RamsarTargetFactory(code='1')
        ramsar_goal = RamsarGoalFactory(code='1', targets=(ramsar_target,))
        resp = self.app.get(reverse('ramsar_home'))
        self.assertEqual(200, resp.status_code)

        # Test Goal title and description
        title = resp.pyquery('h1.goal-title')
        title_expected = 'Ramsar Goal %s:' % (ramsar_goal.code)
        self.assertEqual(title_expected, title[0]
                         .text_content().rstrip().strip())
        description = resp.pyquery('h1.goal-desc')
        self.assertEqual(ramsar_goal.description, description[0]
                         .text_content().rstrip().strip())

        # Test Target title and description
        title = resp.pyquery('div.section h2')
        title_expected = 'Ramsar Target %s' % (ramsar_target.code)
        self.assertEqual(title_expected, title[0]
                         .text_content().rstrip().strip())
        description = resp.pyquery('p.target-description')
        self.assertEqual(ramsar_target.description, description[0]
                         .text_content().rstrip().strip())

    def test_list_ramsar_targets_without_goal(self):
        RamsarTargetFactory.create_batch(2)
        resp = self.app.get(reverse('list_ramsar_targets'))
        self.assertEqual(200, resp.status_code)
        targets = resp.pyquery('ul.list-targets-wrapper li')
        self.assertEqual(2, targets.length)

    def test_list_ramsar_targets_with_goal(self):
        RamsarTargetFactory()
        ramsar_target = RamsarTargetFactory()
        ramsar_goal = RamsarGoalFactory(targets=(ramsar_target,))
        resp = self.app.get(
            reverse('list_ramsar_targets', kwargs={'code': ramsar_goal.code}))
        self.assertEqual(200, resp.status_code)
        targets = resp.pyquery('ul.list-targets-wrapper li')
        self.assertEqual(1, targets.length)

    def test_list_ramsar_goals(self):
        RamsarGoalFactory.create_batch(2)
        resp = self.app.get(reverse('list_ramsar_goals'))
        self.assertEqual(200, resp.status_code)

        goals = resp.pyquery('ul.list-goals-wrapper li')
        self.assertEqual(2, goals.length)
