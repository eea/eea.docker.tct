# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from .base import BaseWebTest
from .factories import NationalObjectiveFactory
from .factories import StaffUserFactory


class NationalSubObjectiveTest(BaseWebTest):

    def setUp(self):
        StaffUserFactory()

    def test_add_subobjective(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory.build()
        data = {
            'language': 'en-us',
            'title': nat_subobj.title_default,
            'description': nat_subobj.description_default,
        }
        url = reverse('edit_national_objective', kwargs={'parent': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-objective-add']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase(
            'NationalObjective',
            {
                'pk': 2,
                'title_default': nat_subobj.title_default,
                'description_default__contains': nat_subobj.description_default,
                'parent': nat_obj,
            }
        )

    def test_edit_subobjective(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory(parent=nat_obj)
        data = {
            'language': 'en-us',
            'title': 'Title edited',
            'description': 'Description edited',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_subobj.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase(
            'NationalObjective',
            {
                'pk': 2,
                'title_default': data['title'],
                'description_default__contains': data['description'],
                'parent': nat_obj,
            }
        )

    def test_edit_subobjective_with_encodings(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory(parent=nat_obj)
        data = {
            'language': 'en-us',
            'title': 'Title edited',
            'description': 'Description edited',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_subobj.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase(
            'NationalObjective',
            {
                'pk': 2,
                'title_default': data['title'],
                'description_default__contains': data['description'],
                'parent': nat_obj,
            }
        )

    def test_delete_subobjective(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory(parent=nat_obj)
        url = reverse('delete_national_objective', kwargs={'pk': nat_subobj.pk})
        self.app.post(url, user='staff').follow()
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase(
                'NationalObjective',
                {
                    'pk': 2,
                }
            )
