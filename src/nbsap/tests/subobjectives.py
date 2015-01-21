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
            'language': 'en',
            'title': nat_subobj.title_en,
            'description': nat_subobj.description_en,
        }
        url = reverse('edit_national_objective', kwargs={'parent': nat_obj.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-objective-add']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=2,
                                    title_en=nat_subobj.title_en,
                                    description_en__contains=nat_subobj.description_en,
                                    parent=nat_obj)

    def test_edit_subobjective(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory(parent=nat_obj)
        data = {
            'language': 'en',
            'title': 'Title edited',
            'description': 'Description edited',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_subobj.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=2,
                                    title_en=data['title'],
                                    description_en__contains=data['description'],
                                    parent=nat_obj)

    def test_edit_subobjective_with_encodings(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory(parent=nat_obj)
        data = {
            'language': 'en',
            'title': 'Title edited',
            'description': 'Description edited',
        }
        url = reverse('edit_national_objective', kwargs={'pk': nat_subobj.pk})
        resp = self.app.get(url, user='staff')
        form = resp.forms['national-objective-edit']
        self.populate_fields(form, data)
        form.submit().follow()
        self.assertObjectInDatabase('NationalObjective', pk=2,
                                    title_en=data['title'],
                                    description_en__contains=data['description'],
                                    parent=nat_obj)

    def test_delete_subobjective(self):
        nat_obj = NationalObjectiveFactory()
        nat_subobj = NationalObjectiveFactory(parent=nat_obj)
        url = reverse('delete_national_objective', kwargs={'pk': nat_subobj.pk})
        self.app.post(url, user='staff').follow()
        with self.assertRaises(AssertionError):
            self.assertObjectInDatabase('NationalObjective', pk=2)
