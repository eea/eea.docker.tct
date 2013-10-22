# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import NationalObjectiveFactory
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

# pattern = r"\s*[,;/\\]\s*"

# # class NationalObjectiveTestCase(TestCase):


# #     def test_404_when_add_after_empty_database_in_nationalstrategy(self):
# #         """ Test 404 page in homepage National Strategy when adding objective after table is empty """

# #         # clean all objectives
# #         objectives = models.NationalObjective.objects.all()
# #         for objective in objectives:
# #             objective.delete()

# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 0)

# #         # test empty-proper-message on national strategy homepage
# #         response = self.client.get("/objectives")
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('No objectives found.', response.content)

# #         # add an sample objective
# #         mydata = {
# #             'language': 'en',
# #             'title': 'My new title',
# #             'description': 'My new description'
# #         }
# #         response = self.client.post('/administration/objectives/add/', mydata)

# #         # test successfull adding
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 1)
# #         objective = objectives[0]
# #         self.assertEqual(objective.title, mydata['title'])
# #         self.assertEqual(objective.description, mydata['description'])

# #         # test view of newly added objective
# #         response = self.client.get('/administration/objectives/%s' % str(objective.id))
# #         self.assertIn(mydata['title'], response.content)
# #         self.assertIn(mydata['description'], response.content)

# #         # cleanup the mess
# #         response = self.client.get('/administration/objectives/%s/delete' % (str(objective.id)))

# #     def test_404_when_add_after_empty_database_in_implementation(self):
# #         """ Test 404 page in homepage Implementation when adding objective after table is empty """

# #         # clean all objectives
# #         objectives = models.NationalObjective.objects.all()
# #         for objective in objectives:
# #             objective.delete()

# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 0)

# #         # test empty-proper-message on national strategy homepage
# #         response = self.client.get("/implementation")
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('No objectives found.', response.content)

# #         # add an sample objective
# #         mydata = {
# #             'language': 'en',
# #             'title': 'My new title',
# #             'description': 'My new description'
# #         }
# #         response = self.client.post('/administration/objectives/add/', mydata)

# #         # test successfull adding
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 1)
# #         objective = objectives[0]
# #         self.assertEqual(objective.title, mydata['title'])
# #         self.assertEqual(objective.description, mydata['description'])

# #         # test view of newly added objective
# #         response = self.client.get('/administration/objectives/%s' % str(objective.id))
# #         self.assertIn(mydata['title'], response.content)
# #         self.assertIn(mydata['description'], response.content)

# #         # cleanup the mess
# #         response = self.client.get('/administration/objectives/%s/delete' % (str(objective.id)))

# #     def test_nat_strategy_empty_database_no_code(self):
# #         """ Test the <empty database, no code given> use case """
# #         # clean all objectives
# #         objectives = models.NationalObjective.objects.all()
# #         for objective in objectives:
# #             objective.delete()

# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 0)

# #         response = self.client.get('/objectives')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('No objectives found.', response.content)

# #     def test_nat_strategy_empty_database_wrong_code(self):
# #         """ Test the <empty database, wrong code given> use case """
# #         # clean all objectives
# #         objectives = models.NationalObjective.objects.all()
# #         for objective in objectives:
# #             objective.delete()

# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 0)

# #         # test a wrong code
# #         response = self.client.get('/objectives/100')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('No objectives found.', response.content)

# #     def test_nat_strategy_full_database_no_code(self):
# #         """ Test the <full database, no code given> use case """
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertNotEqual(len(objectives), 0)

# #         # test no code given
# #         response = self.client.get('/objectives')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('In principle, the entire wealt', response.content)

# #     def test_nat_strategy_pate_full_database_good_code(self):
# #         """ Test the <full database, good code given> use case """
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertNotEqual(len(objectives), 0)

# #         # test a good code
# #         response = self.client.get('/objectives/5')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('s biodiversity touches upon ', response.content)

# #     def test_nat_strategy_page_full_database_wrong_code(self):
# #         """ Test the <full database, wrong code given> use case """
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertNotEqual(len(objectives), 0)

# #         # test a good code
# #         response = self.client.get('/objectives/100')
# #         self.assertEqual(response.status_code, 404)

# #     def test_implementation_page_empty_database_no_code(self):
# #         """ Test the <empty database, no code given> use case """
# #         # clean all objectives
# #         objectives = models.NationalObjective.objects.all()
# #         for objective in objectives:
# #             objective.delete()

# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 0)

# #         response = self.client.get('/implementation')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('No objectives found.', response.content)

# #     def test_implementation_page_empty_database_wrong_code(self):
# #         """ Test the <empty database, wrong code given> use case """
# #         # clean all objectives
# #         objectives = models.NationalObjective.objects.all()
# #         for objective in objectives:
# #             objective.delete()

# #         objectives = models.NationalObjective.objects.all()
# #         self.assertEqual(len(objectives), 0)

# #         # test a wrong code
# #         response = self.client.get('/implementation/100')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('No objectives found.', response.content)

# #     def test_implementation_page_full_database_no_code(self):
# #         """ Test the <full database, no code given> use case """
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertNotEqual(len(objectives), 0)

# #         # test no code given
# #         response = self.client.get('/implementation')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('One of its program is the Monito', response.content)

# #     def test_implementation_page_full_database_good_code(self):
# #         """ Test the <full database, good code given> use case """
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertNotEqual(len(objectives), 0)

# #         # test a good code
# #         response = self.client.get('/implementation/5')
# #         self.assertEqual(response.status_code, 200)
# #         self.assertIn('rawing up of preparations for the m', response.content)

# #     def test_implementation_page_full_database_wrong_code(self):
# #         """ Test the <full database, wrong code given> use case """
# #         objectives = models.NationalObjective.objects.all()
# #         self.assertNotEqual(len(objectives), 0)

# #         # test a good code
# #         response = self.client.get('/implementation/100')
# #         self.assertEqual(response.status_code, 404)


# #     def tearDown(self):
# #          self.user.delete()
