import factory

from nbsap import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


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


    @factory.post_generation
    def parent(self, create, extracted, **kwargs):
        if extracted:
            self.parent = extracted

    @factory.post_generation
    def actions(self, create, extracted, **kwargs):
        if extracted:
            for action in extracted:
                self.actions.add(action)

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the pre-save signal."""
        pre_save.disconnect(models.NationalObjective.pre_save_objective_code,
                            models.NationalObjective)
        obj = super(NationalObjectiveFactory, cls)._generate(create, attrs)
        pre_save.connect(models.NationalObjective.pre_save_objective_code,
                         models.NationalObjective)
        return obj


class NationalActionFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.NationalAction'

    code = factory.Sequence(lambda n: '%d' % n)
    title_en = factory.Sequence(lambda n: 'action%d_title_en' % n)
    description_en = factory.Sequence(lambda n: 'action%d_description_en' % n)


class AichiGoalFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.AichiGoal'

    code = factory.Sequence(lambda n: '%d' % n)
    title_en = factory.Sequence(lambda n: 'obj%d_title_en' % n)
    description_en = factory.Sequence(lambda n: 'obj%d_description_en' % n)

    @factory.post_generation
    def targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.targets.add(target)


class AichiTargetFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.AichiTarget'

    code = factory.Sequence(lambda n: '%d' % n)
    description_en = factory.Sequence(lambda n: 'action%d_description_en' % n)


class NationalStrategyFactory(factory.DjangoModelFactory):

    FACTORY_FOR = 'nbsap.NationalStrategy'

    objective = factory.SubFactory(NationalObjectiveFactory)
    relevant_target = factory.SubFactory(AichiTargetFactory)

    @factory.post_generation
    def other_targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.other_targets.add(target)
