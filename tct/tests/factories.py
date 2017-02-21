import factory
from tct import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save


class StaffUserFactory(factory.DjangoModelFactory):

    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'staff'
    email = 'staff@domain.com'
    is_staff = True
    is_superuser = True


class NationalObjectiveFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.NationalObjective

    code = factory.Sequence(lambda n: '%d' % n)
    title_default = factory.Sequence(lambda n: 'obj%d_title_default' % n)
    description_default = factory.Sequence(
        lambda n: 'obj%d_description_default' % n)

    @factory.post_generation
    def parent(self, create, extracted, **kwargs):
        if extracted:
            self.parent = extracted

    @factory.post_generation
    def actions(self, create, extracted, **kwargs):
        if extracted:
            for action in extracted:
                self.actions.add(action)

    @factory.post_generation
    def nat_indicators(self, create, extracted, **kwargs):
        if extracted:
            for nat_indicator in extracted:
                self.nat_indicators.add(nat_indicator)

    @factory.post_generation
    def other_nat_indicators(self, create, extracted, **kwargs):
        if extracted:
            for other_nat_indicator in extracted:
                self.other_nat_indicators.add(other_nat_indicator)

    @classmethod
    def _generate(cls, create, attrs):
        """Override the default _generate() to disable the pre-save signal."""
        pre_save.disconnect(models.NationalObjective.pre_save_objective_code,
                            models.NationalObjective)
        obj = super(NationalObjectiveFactory, cls)._generate(
            create, attrs)
        pre_save.connect(models.NationalObjective.pre_save_objective_code,
                         models.NationalObjective)
        return obj


class NationalActionFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.NationalAction

    code = factory.Sequence(lambda n: '%d' % n)
    title_default = factory.Sequence(lambda n: 'action%d_title_default' % n)
    description_default = factory.Sequence(
        lambda n: 'action%d_description_default' % n)


class AichiGoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.AichiGoal

    code = factory.Sequence(lambda n: '%d' % n)
    title_default = factory.Sequence(
        lambda n: 'aichi_goal_%d_title_default' % n)
    description_default = factory.Sequence(
        lambda n: 'aichi_goal_%d_description_default' % n)

    @factory.post_generation
    def targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.targets.add(target)


class AichiTargetFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.AichiTarget

    code = factory.Sequence(lambda n: '%d' % n)
    description_default = factory.Sequence(
        lambda n: 'aichi_target_%d_description_default' % n)


class CMSGoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CMSGoal

    code = factory.Sequence(lambda n: '%d' % n)
    title_default = factory.Sequence(
        lambda n: 'cms_goal_%d_title_default' % n)
    description_default = factory.Sequence(
        lambda n: 'cms_goal_%d_description_default' % n)

    @factory.post_generation
    def targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.targets.add(target)


class CMSTargetFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.CMSTarget

    code = factory.Sequence(lambda n: '%d' % n)
    description_default = factory.Sequence(
        lambda n: 'cms_target_%d_description_default' % n)


class RamsarGoalFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RamsarGoal

    code = factory.Sequence(lambda n: '%d' % n)
    title_default = factory.Sequence(
        lambda n: 'ramsar_goal_%d_title_default' % n)
    description_default = factory.Sequence(
        lambda n: 'ramsar_goal_%d_description_default' % n)

    @factory.post_generation
    def targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.targets.add(target)


class RamsarTargetFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.RamsarTarget

    code = factory.Sequence(lambda n: '%d' % n)
    description_default = factory.Sequence(
        lambda n: 'ramsar_target_%d_description_default' % n)


class NationalStrategyFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.NationalStrategy

    objective = factory.SubFactory(NationalObjectiveFactory)

    @factory.post_generation
    def relevant_targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.relevant_targets.add(target)

    @factory.post_generation
    def other_targets(self, create, extracted, **kwargs):
        if extracted:
            for target in extracted:
                self.other_targets.add(target)


class NationalIndicatorFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.NationalIndicator

    code = factory.Sequence(lambda n: '%d' % n)
    title_default = factory.Sequence(lambda n: 'indicator%d_title_default' % n)
    url = 'www.test.url.com'

    @factory.post_generation
    def subindicators(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.subindicators.add(extracted)


class RegionFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Region

    name = factory.Sequence(lambda n: 'region_%d' % n)
