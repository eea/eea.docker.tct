# -*- coding: utf-8 -*-
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
        """ Test the view of national objective """
        response = self.client.get('/administration/objectives/1')
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertIn("In principle, the entire wealth of biodiversity", content)
        self.assertEqual(response.context['objective'].title,
                         "Identify and monitor priority components of biodiversity in Belgium")

    def test_edit_national_objective(self):
        """ Test editing national objective """
        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': 'My new description'
        }

        response = self.client.get('/administration/objectives/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/1/edit', mydata)
        edited_object = models.NationalObjective.objects.all().filter(id=1)[0]
        self.assertEqual(edited_object.title, mydata['title'])
        self.assertEqual(edited_object.description, mydata['description'])

    def test_edit_with_encodings_national_objective(self):
        """ Test editing encodings in national objective """
        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF'
        }

        response = self.client.get('/administration/objectives/1/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/1/edit', mydata)
        edited_object = models.NationalObjective.objects.all().filter(id=1)[0]
        self.assertEqual(edited_object.title, mydata['title'])
        self.assertEqual(edited_object.description_en, mydata['description'])

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
        added_object = models.NationalObjective.objects.all().filter(code='16')[0]
        self.assertEqual(added_object.title, mydata['title'])
        self.assertEqual(added_object.description, mydata['description'])

        # clean the mess by deleting the objective
        response = self.client.get('/administration/objectives/%s/delete' % (str(added_object.id)))

    def test_add_with_encodings_national_objective(self):
        """ Test national objective adding with encodings """
        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF'
        }
        response = self.client.get('/administration/objectives/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/add/', mydata)
        added_object = models.NationalObjective.objects.all().filter(code='16')[0]
        self.assertEqual(added_object.title, mydata['title'])
        self.assertEqual(added_object.description, mydata['description'])

        # clean the mess by deleting the objective
        response = self.client.get('/administration/objectives/%s/delete' % (str(added_object.id)))

    def test_delete_national_objective(self):
        """ Test national objective deleting """

        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': 'My new description'
        }

        response = self.client.post('/administration/objectives/add/', mydata)
        _object = models.NationalObjective.objects.all().filter(code='16')[0]
        response = self.client.get('/administration/objectives/%s/delete' % (str(_object.id)))

        objects = models.NationalObjective.objects.all()
        if len(objects) != 100:
            # delete operation not working properly
            self.assertEqual(1,2)

    def test_404_when_add_after_empty_database(self):
        """ Test 404 page when adding objective after table is empty """

        # clean all objectives
        objectives = models.NationalObjective.objects.all()
        for objective in objectives:
            objective.delete()

        objectives = models.NationalObjective.objects.all()
        self.assertEqual(len(objectives), 0)

        # test empty-proper-message on national strategy homepage
        response = self.client.get("/objectives")
        self.assertEqual(response.status_code, 200)
        self.assertIn('No objectives found.', response.content)

        # add an sample objective
        mydata = {
            'language': 'en',
            'title': 'My new title',
            'description': 'My new description'
        }
        response = self.client.post('/administration/objectives/add/', mydata)

        # test successfull adding
        objectives = models.NationalObjective.objects.all()
        self.assertEqual(len(objectives), 1)
        objective = objectives[0]
        self.assertEqual(objective.title, mydata['title'])
        self.assertEqual(objective.description, mydata['description'])

        # test view of newly added objective
        response = self.client.get('/administration/objectives/%s' % str(objective.id))
        self.assertIn(mydata['title'], response.content)
        self.assertIn(mydata['description'], response.content)

        # cleanup the mess
        response = self.client.get('/administration/objectives/%s/delete' % (str(objective.id)))

    def tearDown(self):
         self.user.delete()
