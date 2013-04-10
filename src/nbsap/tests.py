from django.test.client import Client
from django.utils import unittest

class NationalObjectiveTestCase(unittest.TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.c = Client(enforce_csrf_checks=True)
        self.c.post('/accounts/login/', {'username': 'admin111', 'password': 'q'})

    def test_simple(self):
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_national_objectives(self):
        """ National strategy objectives listing """
        response = self.c.get('/administration/objectives/')
        import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['objectives']), 15)