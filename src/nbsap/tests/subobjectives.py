# -*- coding: utf-8 -*-
from django.test.client import Client
from django.utils import unittest
from django.test import TestCase
from django.contrib.auth.models import User

from nbsap import models

class NationalSubobjectiveTestCase(TestCase):
    fixtures = ['initial_data.json',]

    def setUp(self):
        # create a user to test with
        self.user = User.objects.create_user('admin', 'admin@admin.com', 'q')
        self.client = Client()
        # blind call to set user info on session
        call = self.client.post('/accounts/login/', {'username': 'admin',
                                                     'password': 'q'})
    def test_recursive_subobjectives(self):
        """ Test national subobjective operations recursively """
        mydata = {
                'objective': {
                        'language': 'en',
                        'title': 'My new objective title',
                        'description': 'My new objective description',
                },
                'subobjective': {
                        'language': 'en',
                        'title': 'My new subobjective title',
                        'description': 'My new subobjective description',
                }
        }

        def _recursive_add_subobjectives(object_id, depth=3):
            if depth == 0:
                return

            s_id = str(object_id)
            # get the current object
            _object = models.NationalObjective.objects.all().filter(id=object_id)[0]

            # add subobjective
            response = self.client.get('/administration/objectives/%s/add' % (s_id))
            self.assertEqual(response.status_code, 200)
            response = self.client.post('/administration/objectives/%s/add' % (s_id),
                                        mydata['subobjective'])

            # deep down
            _recursive_add_subobjectives(object_id+1, depth-1)

        def _recursive_check_subobjectives(object_id, depth=3):
            if depth == 0:
                return

            s_id = str(object_id)
            # get the current object
            _object = models.NationalObjective.objects.all().filter(id=object_id)[0]
            _code = _object.code

            # test the subobjective validity
            _subobj = _object.children.values()[0]

            _subobj_code = _subobj['code']
            self.assertEqual(_subobj_code, ".".join([_code, '1']))
            self.assertEqual(_subobj['title_en'], mydata['subobjective']['title'])
            self.assertEqual(_subobj['description_en'], mydata['subobjective']['description'])

            # test the subojective view page
            response = self.client.get('/administration/objectives/%s' % (_subobj['id']))
            self.assertEqual(response.status_code, 200)

            # deep down
            _recursive_check_subobjectives(object_id+1, depth-1)


        # add object
        response = self.client.get('/administration/objectives/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/add/', mydata['objective'])
        added_object = models.NationalObjective.objects.all().filter(code='16')[0]
        self.assertEqual(added_object.title, mydata['objective']['title'])
        self.assertEqual(added_object.description, mydata['objective']['description'])

        # recursively add subobjectives
        _recursive_add_subobjectives(added_object.id)
        _recursive_check_subobjectives(added_object.id)

        # clean the mess by deleting the objective
        response = self.client.get('/administration/objectives/%s/delete' % (added_object.id))

    def test_delete_national_subobjective(self):
        """ Test the delete operation of a national subobjective """
        mydata = {
                'objective': {
                        'language': 'en',
                        'title': 'My new objective title',
                        'description': 'My new objective description',
                },
                'subobjective': {
                        'language': 'en',
                        'title': 'My new subobjective title',
                        'description': 'My new subobjective description',
                }
        }

        # add object
        response = self.client.get('/administration/objectives/add/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/add/', mydata['objective'])
        added_object = models.NationalObjective.objects.all().filter(code='16')[0]
        obj_id = added_object.id
        s_id = str(obj_id)
        self.assertEqual(added_object.title, mydata['objective']['title'])
        self.assertEqual(added_object.description, mydata['objective']['description'])

        # add subobjective
        response = self.client.get('/administration/objectives/%s/add' % (s_id))
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/administration/objectives/%s/add' % (s_id),
                                    mydata['subobjective'])

        try:
            subobj = models.NationalObjective.objects.all().filter(id=obj_id+1)[0]
        except:
            # something went wrong in adding the subobjective
            self.assertEqual(1,2)

        # delete the subobjective
        response = self.client.get('/administration/objectives/%s/delete' % (str(obj_id+1)))

        try:
            subobj = models.NationalObjective.objects.all().filter(id=obj_id+1)[0]
        except:
            pass
        else:
            # something went wrong in deleting the subobjective
            self.assertEqual(1,2)

        # clean the mess by deleting the objective
        response = self.client.get('/administration/objectives/%s/delete' % (s_id))

    def test_edit_national_subobjective(self):
        """ Test the edit operation of a national subobjective """
        mydata = {
                'objective': {
                        'language': 'en',
                        'title': 'My new objective title',
                        'description': 'My new objective description',
                },
                'subobjective': {
                        'language': 'en',
                        'title': 'My new subobjective title',
                        'description': 'My new subobjective description',
                }
        }

        response = self.client.get('/administration/objectives/16/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/16/edit',
                                    mydata['subobjective'])
        _object = models.NationalObjective.objects.all().filter(id=16)[0]
        self.assertEqual(_object.title, mydata['subobjective']['title'])
        self.assertEqual(_object.description, mydata['subobjective']['description'])

    def test_edit_national_subobjective_with_encodings(self):
        """ Test the edit operation with encodings of a national subobjective """
        mydata = {
                'objective': {
                        'language': 'en',
                        'title': 'My new objective title',
                        'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
                },
                'subobjective': {
                        'language': 'en',
                        'title': 'My new subobjective title',
                        'description': u'ĂFKĐȘKŁFKOKR–KF:ŁĂȘĐKF–KFÂŁ:FJK–FFŁKJȘĂŁF',
                }
        }

        response = self.client.get('/administration/objectives/16/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/administration/objectives/16/edit',
                                    mydata['subobjective'])
        _object = models.NationalObjective.objects.all().filter(id=16)[0]
        self.assertEqual(_object.title, mydata['subobjective']['title'])
        self.assertEqual(_object.description, mydata['subobjective']['description'])


    def tearDown(self):
         self.user.delete()
