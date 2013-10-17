import factory
from django.contrib.auth.models import User


class StaffUserFactory(factory.DjangoModelFactory):

    FACTORY_FOR = User
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    username = 'staff'
    email = 'staff@domain.com'
    is_staff = True
    is_superuser = True


class NationalObjectiveFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.NationalObjective'

    code = factory.Sequence(lambda n: '%d' % n)
    title_en = factory.Sequence(lambda n: 'obj%d_title_en' % n)
    description_en = factory.Sequence(lambda n: 'obj%d_description_en' % n)


class NationalActionFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.NationalAction'
    FACTORY_DJANGO_GET_OR_CREATE = ('code', 'title', 'description')

    code = 1
    title = 'action1_title'
    description = 'action1__description'


