from django.test.client import Client
from django.utils import unittest
from django.test import TestCase
from django.contrib.auth.models import User

from nbsap import models

class NationalObjectiveTestCase(TestCase):
    fixtures = ['initial_data.json',]

    def setUp(self):
        # create a user to test with
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'q')
        self.client = Client()
        # blind call to set user info on session
        call = self.client.post('/accounts/login/', {'username': 'admin',
                                                     'password': 'q'})

    def test_list_national_objectives(self):
        """ National strategy objectives listing """
        response = self.client.get('/administration/objectives/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['objectives']), 15)

    def test_view_national_objective(self):
        """ Test the view of national objective 1 """
        response = self.client.get('/administration/objectives/1')
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertIn("In principle, the entire wealth of biodiversity", content)
        self.assertEqual(response.context['objective'].title,
                         "Identify and monitor priority components of biodiversity in Belgium")

    def test_edit_national_objective(self):
        """ Test editing national objective 1"""
        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': 'My new description'
        }

        response = self.client.get('/administration/objectives/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/1/edit', mydata)
        edited_object = models.NationalObjective.objects.all().filter(id=1)[0]
        self.assertEqual(edited_object.title, 'My new title')
        self.assertEqual(edited_object.description, 'My new description')

    def test_add_national_objective(self):
        """ Test national objective adding """
        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': 'My new description'
        }
        response = self.client.get('/administration/objectives/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/add/', mydata)
        edited_object = models.NationalObjective.objects.all().filter(id=101)[0]
        self.assertEqual(edited_object.title, 'My new title')
        self.assertEqual(edited_object.description, 'My new description')

    def test_delete_national_objective(self):
        """ Test national objective deleting """

        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': 'My new description'
        }

        response = self.client.post('/administration/objectives/add/', mydata)
        response = self.client.get('/administration/objectives/101/delete')
        deleted_ = models.NationalObjective.objects.all().filter(id=101)
        try:
            self.assertEqual(deleted_['title'], 'My new title')
        except:
            pass
        else:
            # delete operation not working properly
            self.assertEqual(1,2)

    def tearDown(self):
         self.user.delete()
