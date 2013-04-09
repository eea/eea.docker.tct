from django.db import models
from django.db.models.signals import pre_save
from transmeta import TransMeta

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

    title = models.CharField("Operational Indicator",
                             max_length=512)

    question = models.CharField("Communication Question",
                                max_length=255)

    head_indicator = models.CharField("Headline Indicator",
                                      max_length=255)

    sub_indicator = models.CharField("Indicator Sub-topics",
                                     max_length=255)

    classification = models.CharField("Operational Classification",
                                      max_length=255)

    status = models.TextField("Status of development",
                              blank=True) #????

    sensitivity = models.CharField("Sensitivity (can it be used to make assessment by 2015?)",
                                   max_length=3,
                                   choices=LEVEL_CHOICES,
                                   blank=True)

    scales = models.ManyToManyField(Scale,
                                    verbose_name="Scale (global, regional, national, sub-national)",
                                    blank=True,
                                    null=True)

    validity = models.CharField("Scientific Validity",
                                max_length=3,
                                choices=LEVEL_CHOICES,
                                blank=True)

    ease_of_communication = models.CharField("How easy can it be communicated?",
                                             max_length=3,
                                             choices=LEVEL_CHOICES,
                                             blank=True)

    sources = models.CharField("Data Sources",
                               max_length=255,
                               blank=True)

    requirements = models.TextField(blank=True)

    measurer = models.TextField("Who's responsible for measuring?",
                                blank=True)

    conventions = models.CharField("Other conventions/processes using indicator",
                                   max_length=255,
                                   blank=True)

    links = models.ManyToManyField(Link,
                                   verbose_name="Related Links",
                                   blank=True,
                                   null=True)

    def __unicode__(self):
        return self.title


class AichiTarget(models.Model):
    __metaclass__ = TransMeta

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
        translate = ('description',)


class AichiGoal(models.Model):
    __metaclass__ = TransMeta

    code = models.CharField(max_length=1, primary_key=True)
    title = models.CharField(verbose_name="Title", max_length=512)
    description = models.TextField(verbose_name="Description")
    targets = models.ManyToManyField(AichiTarget,
                                     related_name="goals")

    def __unicode__(self):
        return self.title

    class Meta:
        translate = ('title', 'description',)


class NationalAction(models.Model):
    __metaclass__ = TransMeta

    code = models.CharField(max_length=16)
    description = models.TextField(verbose_name="Description")

    class Meta:
        translate = ('description',)

    def __unicode__(self):
        return self.code

class NationalObjective(models.Model):

    __metaclass__ = TransMeta

    code = models.CharField(max_length=16)
    title = models.CharField(max_length=512,
                             verbose_name="Title")
    description = models.TextField(verbose_name="Description")
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
    def pre_save_objective_code(**kwargs):

        if kwargs['raw'] is True:
            return  #ignore when loading initial_data

        instance = kwargs['instance']

        if instance.code:
            return  #ignore on edit

        if instance.parent:
            codes = [ ob.code for ob in instance.parent.children.all() if ob ]
            #if parent objective has children the increment the last childen's code
            if codes:
                codes.sort(key=lambda s: map(int, s.split('.')))
                parent_code, last_code = codes[-1].split('.')
                instance.code = '{0}.{1}'.format(parent_code, int(last_code)+1)
            else:
                instance.code = '{0}.1'.format(instance.parent.code)

        else:
            codes = [ ob.code for ob in
                              NationalObjective.objects.filter(parent=None).all() ]
            codes.sort(key=lambda s: int(s))
            last_code = codes[-1]
            instance.code = '{0}'.format(int(last_code)+1)

    def get_all_objectives(self):
        #we should use https://github.com/django-mptt/django-mptt/
        r = []
        for ob in NationalObjective.objects.filter(parent=self):
            r.append(ob)
            r.extend(ob.get_all_objectives())
        return r

class EuAction(models.Model):
    __metaclass__ = TransMeta

    code = models.CharField(max_length=16)
    description = models.TextField(verbose_name="Description")
    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='children')

    class Meta:
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


class EuTarget(models.Model):
    __metaclass__ = TransMeta

    code = models.CharField(max_length=16)
    title = models.CharField(max_length=512,
                             verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    actions = models.ManyToManyField(EuAction,
                                     related_name="target")

    def __unicode__(self):
        return 'Target %s' % self.code

    class Meta:
        translate = ('title', 'description',)


class EuAichiStrategy(models.Model):
    eu_target = models.ForeignKey(EuTarget,
                                  verbose_name="EU Biodiversity Target",
                                  related_name="eu_aichi_strategy")
    aichi_targets = models.ManyToManyField(AichiTarget,
                                           verbose_name="Aichi targets",
                                           related_name="eu_aichi_strategy")


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

pre_save.connect(NationalObjective.pre_save_objective_code, sender=NationalObjective)
