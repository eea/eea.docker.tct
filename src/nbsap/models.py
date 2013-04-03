from django.db import models
from transmeta import TransMeta


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
                             max_length=250)

    question = models.CharField("Communication Question",
                                max_length=250)

    head_indicator = models.CharField("Headline Indicator",
                                      max_length=250)

    sub_indicator = models.CharField("Indicator Sub-topics",
                                     max_length=250)

    classification = models.CharField("Operational Classification",
                                      max_length=250)

    status = models.TextField("Status of development",
                              blank=True)

    sensitivity = models.CharField("Sensitivity (can it be used to make assessment by 2015?)",
                                   max_length=3,
                                   choices=LEVEL_CHOICES,
                                   blank=True)

    scales = models.ManyToManyField(Scale,
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
                               max_length=250,
                               blank=True)

    requirements = models.TextField(blank=True)

    measurer = models.TextField("Who's responsible for measuring?",
                                blank=True)

    conventions = models.CharField("Other conventions/processes using indicator",
                                   max_length=250,
                                   blank=True)

    links = models.TextField(blank=True)

    def __unicode__(self):
        return self.title


class AichiTarget(models.Model):
    __metaclass__ = TransMeta

    title = models.CharField(verbose_name="Title", max_length=250)
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
        return self.title

    class Meta:
        translate = ('title', 'description',)


class AichiGoal(models.Model):
    __metaclass__ = TransMeta

    code = models.CharField(max_length=1, primary_key=True)
    title = models.CharField(verbose_name="Title", max_length=250)
    description = models.TextField(verbose_name="Description")
    targets = models.ManyToManyField(AichiTarget)

    def __unicode__(self):
        return self.title

    class Meta:
        translate = ('title', 'description',)


class NationalAction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.title


class NationalObjective(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='children')
    actions = models.ForeignKey(NationalAction,
                                null=True,
                                blank=True)

    def __unicode__(self):
        return self.title


class EuAction(models.Model):
    __metaclass__ = TransMeta

    title = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='children')

    def __unicode__(self):
        return self.title

    class Meta:
        translate = ('title', 'description',)

class EuTarget(models.Model):
    __metaclass__ = TransMeta

    title = models.CharField(max_length=255)
    description = models.TextField()
    actions = models.ManyToManyField(EuAction)

    def __unicode__(self):
        return self.title

    class Meta:
        translate = ('title', 'description',)

