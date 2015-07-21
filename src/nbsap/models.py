import re
from django.db import models
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.conf import settings
from transmeta import TransMeta
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy as _

from nbsap.utils import RE_ACTION_CODE


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

    sensitivity = models.CharField(
        _('Sensitivity (can it be used to make assessment by 2015?)'),
        max_length=3,
        choices=LEVEL_CHOICES,
        blank=True)

    scales = models.ManyToManyField(
        Scale,
        verbose_name=_('Scale (global, regional, national, sub-national)'),
        blank=True,
        null=True)

    validity = models.CharField(_('Scientific Validity'),
                                max_length=3,
                                choices=LEVEL_CHOICES,
                                blank=True)

    ease_of_communication = models.CharField(
        _('How easy can it be communicated?'),
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

    conventions = models.CharField(
        _('Other conventions/processes using indicator'),
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
        return u'Target %s' % self.code

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

    @property
    def first_objective(self):
        try:
            return self.objective.get()
        except (NationalAction.DoesNotExists,
                NationalAction.MultipleObjectsReturned):
            return None


class EuAction(models.Model):
    __metaclass__ = Translatable

    code = models.CharField(max_length=16)
    title = models.TextField(verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    parent = models.ForeignKey('self',
                               null=True,
                               blank=True,
                               related_name='children')

    if settings.EU_STRATEGY and settings.NAT_STRATEGY:
        national_strategy = models.ManyToManyField(
            'NationalStrategy',
            null=True,
            blank=True,
            verbose_name="National strategy",
            related_name="eu_actions")

    class Meta:
        verbose_name_plural = 'EU actions'
        translate = ('description', 'title')

    def __unicode__(self):
        return 'Action %s' % self.code

    def get_target(self):
        if self.parent is None:
            return self.target.all()[0]
        else:
            return self.parent.target.all()[0]

    def subactions(self):
        return self.get_all_actions()[1:]

    def get_all_actions(self):
        #we should use https://github.com/django-mptt/django-mptt/
        r = []
        r.append(self)
        for ob in EuAction.objects.filter(parent=self).order_by('code'):
            r.extend(ob.get_all_actions())
        return r

    def get_next_code(self):
        if self.parent:
            codes = [a.code for a in self.parent.subactions()]
            if codes:
                max_letter = RE_ACTION_CODE.match(max(codes)).groups()[1]
                letter = chr(ord(max_letter) + 1)
            else:
                letter = 'a'
            return self.parent.code + letter

        codes = [int(RE_ACTION_CODE.match(code).groups()[0]) for code in
                 EuAction.objects.values_list('code', flat=True)]
        return str(max(codes) + 1)


class BaseIndicator(models.Model):
    def get_indicators(self):
        return mark_safe('-, <br>'.join(
            [unicode(obj) for obj in self.parent.all()]
        ))

    class Meta:
        abstract = True


class EuIndicator(BaseIndicator):
    __metaclass__ = Translatable

    TYPES = (
        ('sebi', 'SEBI'),
        ('csi', 'CSI'),
        ('aei', 'AEI'),
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
    parent = models.ManyToManyField('self', null=True, blank=True,
                                    symmetrical=False, related_name='parents')

    @property
    def subindicators(self):
        return self.parent

    @property
    def full_code(self):
        if self.indicator_type:
            return u'{0} {1}'.format(self.get_indicator_type_display().upper(),
                                     self.code)
        return self.code

    def __unicode__(self):
        return u'{0} {1}: {2}'.format(self.indicator_type.upper(),
                                      self.code,
                                      self.title)

    def get_indicators(self):
        return mark_safe('-, <br>'.join(
            [unicode(obj) for obj in self.parent.all()]
        ))

    def get_code_type(self):
        return u'{0} {1}'.format(self.indicator_type.upper(),
                                 self.code)

    get_indicators.short_description = 'relation'

    class Meta:
        verbose_name_plural = 'EU indicators'
        ordering = ['code']
        translate = ('title',)


class NationalIndicator(BaseIndicator):
    __metaclass__ = Translatable

    code = models.CharField(max_length=25,
                            null=True,
                            blank=True)
    title = models.TextField(max_length=512,
                             verbose_name="Title")
    url = models.URLField(null=True,
                          blank=True)
    subindicators = models.ManyToManyField('self', null=True, blank=True,
                                           symmetrical=False,
                                           related_name='parents')

    def __unicode__(self):
        return u'{0}: {1}'.format(self.code, self.title)

    def get_indicators(self):
        return mark_safe('-, <br>'.join(
            [unicode(obj) for obj in self.subindicators.all()]
        ))

    get_indicators.short_description = 'relation'

    class Meta:
        verbose_name_plural = 'National indicators'
        ordering = ['code']
        translate = ('title',)


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

    nat_indicators = models.ManyToManyField(
        NationalIndicator, related_name="nat_objectives", blank=True
    )

    other_nat_indicators = models.ManyToManyField(
        NationalIndicator, related_name="other_nat_objectives", blank=True
    )

    class Meta:
        translate = ('title', 'description',)

    def __unicode__(self):
        return self.title

    @staticmethod
    def _pre_save_objective_code_on_create(instance):
        """Logic executed before saving a new Objective instance.

        Set the next code for the objective.
        """
        if instance.parent:
            codes = [ob.code for ob in instance.parent.children.all() if ob]
            # if parent objective has children the increment the last childen's
            # code
            if codes:
                codes.sort(key=lambda x: [int(y) for y in x.split('.')])
                parts = codes[-1].split('.')
                parent_code = '.'.join(parts[:-1])
                last_code = parts[-1]
                instance.code = '{0}.{1}'.format(parent_code,
                                                 int(last_code) + 1)
            else:
                instance.code = '{0}.1'.format(instance.parent.code)

        else:
            codes = [ob.code for ob in
                     NationalObjective.objects.filter(parent=None).all()]
            # if empty national strategy table - reinitialize code values
            if len(codes) == 0:
                codes = ['0']

            codes.sort(key=lambda s: int(s))
            last_code = codes[-1]
            instance.code = '{0}'.format(int(last_code) + 1)

    @staticmethod
    def _pre_save_objective_code_on_edit(instance):
        """Logic executed before editing an Objective instance.

        Update the code for every child and sub-objective to match
        the parent objective.
        """
        for objective in instance.children.all():
            parts = objective.code.split('.')
            suffix_code = parts[-1]
            objective.code = '{0}.{1}'.format(instance.code, suffix_code)
            objective.save()

        # update the action code for each child action
        for action in instance.actions.all():
            action.code = instance.code
            action.save()

    @staticmethod
    def pre_save_objective_code(**kwargs):

        if kwargs['raw'] is True:
            return  # ignore when loading initial_data

        instance = kwargs['instance']

        if instance.code:
            NationalObjective._pre_save_objective_code_on_edit(instance)
        else:
            NationalObjective._pre_save_objective_code_on_create(instance)

    def get_all_objectives(self):
        #we should use https://github.com/django-mptt/django-mptt/
        r = []
        for ob in NationalObjective.objects.filter(parent=self):
            r.append(ob)
            r.extend(ob.get_all_objectives())
        return r

    def get_national_strategies(self):
        return self.objective_national_strategy.all()

    @property
    def national_strategy(self):
        ss = self.get_national_strategies()
        return ss and ss[0]

    @property
    def eu_objects(self):
        obj_eu_targets = {}
        if not self.national_strategy:
            return obj_eu_targets

        strategy = self.national_strategy
        eu_targets = strategy.eu_targets.all()
        eu_actions = strategy.eu_actions.all()
        for target in eu_targets:
            obj_eu_targets.setdefault(target, [])
            for action in target.actions.all():
                if action in eu_actions:
                    obj_eu_targets[target].append(action)
                obj_eu_targets[target] += [
                    subaction for subaction in action.children.all() if
                    subaction in eu_actions
                ]
        return obj_eu_targets

    def has_national_strategies(self):
        strategies = [s.eu_targets.all() for s in
                      self.get_national_strategies()]
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


class EuTarget(models.Model):
    __metaclass__ = Translatable

    code = models.CharField(max_length=16)
    title = models.TextField(max_length=512,
                             verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    actions = models.ManyToManyField(
        EuAction, related_name="target", blank=True,
    )
    indicators = models.ManyToManyField(
        EuIndicator, related_name="targets", blank=True,
    )
    other_indicators = models.ManyToManyField(
        EuIndicator, related_name="other_targets", blank=True,
    )

    if settings.EU_STRATEGY and settings.NAT_STRATEGY:
        national_strategy = models.ManyToManyField(
            'NationalStrategy',
            null=True,
            blank=True,
            verbose_name="National objectives",
            related_name="eu_targets")

    @staticmethod
    def _pre_save_target_code_on_create(instance):
        codes = [ob.code for ob in EuTarget.objects.filter().all()]
        if len(codes) == 0:
            codes = ['0']

        codes.sort(key=lambda s: int(s))
        last_code = codes[-1]
        instance.code = '{0}'.format(int(last_code) + 1)

    @staticmethod
    def _pre_save_target_code_on_edit(instance):
        if not instance.id:
            return

        # update the action code for each child action
        for action in instance.actions.all():
            action.code = instance.code
            action.save()

        # update the action code for each child action
        for indicator in instance.indicators.all():
            indicator.code = instance.code
            indicator.save()

    @staticmethod
    def pre_save_objective_code(**kwargs):

        if kwargs['raw'] is True:
            return  # ignore when loading initial_data

        instance = kwargs['instance']

        if instance.code:
            EuTarget._pre_save_target_code_on_edit(instance)
        else:
            EuTarget._pre_save_target_code_on_create(instance)

    def __unicode__(self):
        return 'Target {0}: {1}'.format(self.code, self.title)

    def get_indicators(self):
        return mark_safe(', <br>'.join(
            [unicode(obj) for obj in self.indicators.all()]
        ))

    get_indicators.short_description = 'EU Indicators'

    def get_indicators_short(self):
        return ', '.join(i.get_code_type() for i in self.indicators.all())

    def get_other_indicators_short(self):
        return ', '.join(i.get_code_type()
                         for i in self.other_indicators.all())

    class Meta:
        verbose_name_plural = 'EU targets'
        ordering = ['code']
        translate = ('title', 'description',)


class EuIndicatorToAichiStrategy(models.Model):
    eu_indicator = models.ForeignKey(
        EuIndicator,
        verbose_name="EU Biodiversity Indicator",
        related_name="eu_indicator_aichi_strategy")
    aichi_targets = models.ManyToManyField(
        AichiTarget,
        verbose_name="Aichi targets",
        related_name="eu_indicator_aichi_strategy")
    other_aichi_targets = models.ManyToManyField(
        AichiTarget,
        verbose_name="Other Aichi targets",
        related_name="eu_indicator_other_aichi_strategy",
        blank=True,
    )

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
    other_aichi_targets = models.ManyToManyField(
        AichiTarget, verbose_name="Other Aichi targets",
        related_name="eu_other_aichi_strategy", blank=True,
    )

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
    relevant_targets = models.ManyToManyField(
        AichiTarget, null=True, blank=True,
        verbose_name="Relevant AICHI Targets",
        related_name="relevant_targets_national_strategy",
    )
    other_targets = models.ManyToManyField(
        AichiTarget, null=True, blank=True,
        verbose_name="Other AICHI targets",
        related_name="other_targets_national_strategy",
    )

    def __unicode__(self):
        return 'Strategy' + unicode(self.objective)

    @property
    def goals_list(self):
        goals = [t.get_parent_goal() for t in self.targets_list]
        return [g for g in goals if g]

    @property
    def targets_list(self):
        ts = list(self.relevant_targets.all()) + list(self.other_targets.all())
        ts.sort(key=lambda t: t.code)
        return ts

    @property
    def eu_targets_list(self):
        return list(self.eu_targets.all())

    @property
    def targets_t(self):
        return ''.join(['t{0}'.format(t.code) for t in self.eu_targets_list])

    @property
    def targets_z(self):
        r = ''
        targets = self.eu_targets_list
        for target in EuTarget.objects.all():
            if target in targets:
                r += '1'
            else:
                r += '0'
        return r

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


pre_save.connect(NationalObjective.pre_save_objective_code,
                 sender=NationalObjective)
pre_save.connect(EuTarget.pre_save_objective_code, sender=EuTarget)
