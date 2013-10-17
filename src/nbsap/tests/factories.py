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

    code = factory.Sequence(lambda n: '%d' % n)
    title = factory.Sequence(lambda n: 'action%d_title_en' % n)
    description = factory.Sequence(lambda n: 'action%d_description_en' % n)


