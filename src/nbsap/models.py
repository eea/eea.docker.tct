from django.db import models
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.conf import settings
from transmeta import TransMeta
from tinymce import models as tinymce_models

from django.utils.translation import ugettext_lazy as _


def getter_for_default_language(field_name):
    def getter(self):
        lang = settings.LANGUAGE_CODE
        return getattr(self, '%s_%s' % (field_name, lang))
    return getter


class Translatable(TransMeta):

    def __new__(cls, name, bases, attrs):
        new_class = TransMeta.__new__(cls, name, bases, attrs)
        for field in new_class._meta.translatable_fields:
            setattr(new_class, field + '_default',
                    property(getter_for_default_language(field)))
        return new_class


class Link(models.Model):
    title = models.CharField(max_length=512)
    url = models.URLField()

    def __unicode__(self):
        return self.title


class Scale(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title


class AichiIndicator(models.Model):

    LEVEL_CHOICES = (
        ('low', 'Low'),
        ('med', 'Medium'),
        ('hig', 'High'),
    )

    title = models.CharField(_('Operational Indicator'),
                             max_length=512)

    question = models.CharField(_('Communication Question'),
                                max_length=255)

    head_indicator = models.CharField(_('Headline Indicator'),
                                      max_length=255)

    sub_indicator = models.CharField(_('Indicator Sub-topics'),
                                     max_length=255)

    classification = models.CharField(_('Operational Classification'),
                                      max_length=255)

    status = models.TextField(_('Status of development'),
                              blank=True)

    sensitivity = models.CharField(_('Sensitivity (can it be used to make assessment by 2015?)'),
                                   max_length=3,
                                   choices=LEVEL_CHOICES,
                                   blank=True)

    scales = models.ManyToManyField(Scale,
                                    verbose_name=_('Scale (global, regional, national, sub-national)'),
                                    blank=True,
                                    null=True)

    validity = models.CharField(_('Scientific Validity'),
                                max_length=3,
                                choices=LEVEL_CHOICES,
                                blank=True)

    ease_of_communication = models.CharField(_('How easy can it be communicated?'),
                                             max_length=3,
                                             choices=LEVEL_CHOICES,
                                             blank=True)

    sources = models.CharField(_('Data Sources'),
                               max_length=255,
                               blank=True)

    requirements = models.TextField(_('Requirements'),
                                    blank=True)

    measurer = models.TextField(_('Who\'s responsible for measuring?'),
                                blank=True)

    conventions = models.CharField(_('Other conventions/processes using indicator'),
                                   max_length=255,
                                   blank=True)

    links = models.ManyToManyField(Link,
                                   verbose_name=_('Related Links'),
                                   blank=True,
                                   null=True)

    def __unicode__(self):
        return self.title


class AichiTarget(models.Model):
    __metaclass__ = Translatable

    code = models.CharField(max_length=16)
    description = models.TextField(verbose_name="Description")
    indicators = models.ManyToManyField(AichiIndicator,
                                        related_name="relevant_target",
                                        blank=True,
                                        null=True)
    other_indicators = models.ManyToManyField(AichiIndicator,
                                              related_name="other_targets",
                                              blank=True,
                                              null=True)

    def __unicode__(self):
        return 'Target %s' % self.code

    def get_parent_goal(self):
        return self.goals.all()[0]

    class Meta:
        ordering = ['code']
        translate = ('description',)


class AichiGoal(models.Model):

    __metaclass__ = Translatable

    code = models.CharField(max_length=1, primary_key=True)
    title = models.TextField(verbose_name="Title", max_length=512)
    description = tinymce_models.HTMLField(verbose_name="Description")
    targets = models.ManyToManyField(AichiTarget, related_name="goals")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['code']
        translate = ('title', 'description',)


class NationalAction(models.Model):
    __metaclass__ = Translatable

    code = models.CharField(max_length=16)
    title = models.TextField(verbose_name="Title", max_length=512, blank=True)
    description = tinymce_models.HTMLField(verbose_name="Description")

    class Meta:
        translate = ('title', 'description',)

    def __unicode__(self):
        return self.code


class NationalObjective(models.Model):

    __metaclass__ = Translatable

    code = models.CharField(max_length=16, unique=True)
    title = models.TextField(max_length=512,
                             verbose_name="Title")
    description = tinymce_models.HTMLField(verbose_name="Description")
    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='children')
    actions = models.ManyToManyField(NationalAction,
                                     null=True,
                                     blank=True,
                                     related_name="objective")
    class Meta:
        translate = ('title', 'description',)

    def __unicode__(self):
        return self.title

    @staticmethod
    def pre_save_objective_code_on_create(instance):
        """Logic executed before saving a new Objective instance.

        Set the next code for the objective.
        """
        if instance.parent:
            codes = [ ob.code for ob in instance.parent.children.all() if ob ]
            # if parent objective has children the increment the last childen's
            # code
            if codes:
                codes.sort(key=lambda x: [int(y) for y in x.split('.')])
                parts = codes[-1].split('.')
                parent_code = '.'.join(parts[:-1])
                last_code = parts[-1]
                instance.code = '{0}.{1}'.format(parent_code, int(last_code)+1)
            else:
                instance.code = '{0}.1'.format(instance.parent.code)

        else:
            codes = [ ob.code for ob in
                      NationalObjective.objects.filter(parent=None).all() ]
            # if empty national strategy table - reinitialize code values
            if len(codes) == 0:
                codes = ['0']

            codes.sort(key=lambda s: int(s))
            last_code = codes[-1]
            instance.code = '{0}'.format(int(last_code)+1)

    @staticmethod
    def pre_save_objective_code_on_edit(instance):
        """Logic executed before editing an Objective instance.

        Update the code for every child and sub-objective to match
        the parent objective.
        """
        for child in instance.children.all():
            parts = child.code.split('.')
            suffix_code = parts[-1]
            child.code = '{0}.{1}'.format(instance.code, suffix_code)
            child.save()

        # update the action code for each child action
        for action in instance.actions.all():
            action.code = instance.code
            action.save()

    @staticmethod
    def pre_save_objective_code(**kwargs):

        if kwargs['raw'] is True:
            return  #ignore when loading initial_data

        instance = kwargs['instance']

        if instance.code:
            NationalObjective.pre_save_objective_code_on_edit(instance)
        else:
            NationalObjective.pre_save_objective_code_on_create(instance)

    def get_all_objectives(self):
        #we should use https://github.com/django-mptt/django-mptt/
        r = []
        for ob in NationalObjective.objects.filter(parent=self):
            r.append(ob)
            r.extend(ob.get_all_objectives())
        return r

    def get_national_strategies(self):
        return self.objective_national_strategy.all()

    def has_national_strategies(self):
        strategies = [s.eu_targets.all() for s in self.get_national_strategies()]
        strategies = filter(lambda x: len(x) > 0, strategies)
        if len(strategies) > 0:
            return True
        else:
            return False

    def get_root_parent(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_root_parent()

    def get_parents(self):
        yield self
        if self.parent is not None:
            for obj in self.parent.get_parents():
                yield obj


class EuAction(models.Model):
    __metaclass__ = Translatable

    code = models.CharField(max_length=16)
    description = models.TextField(verbose_name="Description")
    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='children')

    class Meta:
        verbose_name_plural = 'EU actions'
        translate = ('description',)

    def __unicode__(self):
        return 'Action %s' % self.code

    def get_target(self):
        if self.parent is None:
            return self.target.all()[0]
        else:
            return self.parent.target.all()[0]

    def get_all_actions(self):
        #we should use https://github.com/django-mptt/django-mptt/
        r = []
        r.append(self)
        for ob in EuAction.objects.filter(parent=self):
            r.extend(ob.get_all_actions())
        return r


class EuIndicator(models.Model):
    __metaclass__ = Translatable

    TYPES = (
        ('eu', 'EU'),
        ('sebi', 'SEBI'),
    )

    code = models.CharField(max_length=25,
                            null=True,
                            blank=True)
    title = models.TextField(max_length=512,
                             verbose_name="Title")
    url = models.URLField(null=True,
                          blank=True)
    indicator_type = models.CharField(_('Indicator type'),
                                      max_length=4,
                                      choices=TYPES,
                                      blank=True)
    parent = models.ManyToManyField('self',
                                null=True,
                                blank=True,
                                related_name='children')

    def __unicode__(self):
        return '{0} {1}: {2}'.format(self.indicator_type.upper(),
                                     self.code,
                                     self.title)

    def get_indicators(self):
        return mark_safe(', <br>'.join([unicode(obj)
                for obj in self.parent.all()]))
    get_indicators.short_description = 'relation'

    class Meta:
        verbose_name_plural = 'EU indicators'
        ordering = ['code']
        translate = ('title',)


class EuTarget(models.Model):
    __metaclass__ = Translatable

    code = models.CharField(max_length=16)
    title = models.TextField(max_length=512,
                             verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    actions = models.ManyToManyField(EuAction,
                                     related_name="target")
    indicators = models.ManyToManyField(EuIndicator,
                                     related_name="indicator")

    def __unicode__(self):
        return 'Target {0}: {1}'.format(self.code, self.title)

    def get_indicators(self):
        return mark_safe(', <br>'.join([unicode(obj)
                for obj in self.indicators.all()]))
    get_indicators.short_description = 'EU Indicators'

    class Meta:
        verbose_name_plural = 'EU targets'
        ordering = ['code']
        translate = ('title', 'description',)


class EuIndicatorToAichiStrategy(models.Model):
    eu_indicator = models.ForeignKey(EuIndicator,
                                  verbose_name="EU Biodiversity Indicator",
                                  related_name="eu_indicator_aichi_strategy")
    aichi_targets = models.ManyToManyField(AichiTarget,
                                           verbose_name="Aichi targets",
                                           related_name="eu_indicator_aichi_strategy")

    def get_targets(self):
       return ', '.join([obj.code for obj in self.aichi_targets.all()])
    get_targets.short_description = 'AICHI targets'

    class Meta:
        verbose_name_plural = 'Mappings: EU indicators to Aichi'
        ordering = ['eu_indicator']


class EuAichiStrategy(models.Model):
    eu_target = models.ForeignKey(EuTarget,
                                  verbose_name="EU Biodiversity Target",
                                  related_name="eu_aichi_strategy")
    aichi_targets = models.ManyToManyField(AichiTarget,
                                           verbose_name="Aichi targets",
                                           related_name="eu_aichi_strategy")

    def get_targets(self):
       return ', '.join([obj.code for obj in self.aichi_targets.all()])
    get_targets.short_description = 'AICHI targets'

    class Meta:
        verbose_name_plural = ' Mappings: EU targets to Aichi'
        ordering = ['eu_target']


class NationalStrategy(models.Model):

    objective = models.ForeignKey(NationalObjective,
                                  verbose_name="National Objective",
                                  related_name="objective_national_strategy")
    relevant_target = models.ForeignKey(AichiTarget,
                                        verbose_name="Relevant AICHI target",
                                        related_name="relevant_target_national_strategy")
    other_targets = models.ManyToManyField(AichiTarget,
                                           null=True,
                                           blank=True,
                                           verbose_name="Other AICHI targets",
                                           related_name="other_targets_national_strategy")

    from django.conf import settings
    if settings.EU_STRATEGY:
        eu_targets = models.ManyToManyField(EuTarget,
                                            null=True,
                                            blank=True,
                                            verbose_name="EU targets",
                                            related_name="national_strategy")
        eu_actions = models.ManyToManyField(EuAction,
                                            null=True,
                                            blank=True,
                                            verbose_name="Eu related actions",
                                            related_name="national_strategy")

    class Meta:
        verbose_name_plural = ' Mappings: National strategy to AICHI&EU'


class NbsapPage(models.Model):

    __metaclass__ = Translatable

    handle = models.CharField(max_length=32)
    title = models.CharField(max_length=128, verbose_name='Title')
    body = models.TextField(blank=True, verbose_name='Body')

    class Meta:
        translate = ('title', 'body',)

    def __unicode__(self):
        return self.handle


class NavbarLink(models.Model):

    name = models.CharField(max_length=12)
    title = models.CharField(max_length=64, blank=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name


pre_save.connect(NationalObjective.pre_save_objective_code, sender=NationalObjective)
