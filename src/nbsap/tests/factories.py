# -*- coding: utf-8 -*-
import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserFactory(factory.DjangoModelFactory):

    FACTORY_FOR = User

    username = 'johndoe'
    email = 'jd@domain.com'
    password = make_password('johndoe')

    is_staff = True
    is_superuser = True


class NationalObjectiveFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.NationalObjective'
    FACTORY_DJANGO_GET_OR_CREATE = ('code', 'title_en', 'description_en')

    code = 1
    title_en = 'obj1_title_en'
    description_en = 'obj1_description_en'


class NationalActionFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.NationalAction'
    FACTORY_DJANGO_GET_OR_CREATE = ('code', 'title', 'description')

    code = 1
    title = 'action1_title'
    description = 'action1__description'


