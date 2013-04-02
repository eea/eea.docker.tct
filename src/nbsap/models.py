from django.db import models

class Scale(models.Model):
    name = models.CharField(max_length=30)

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
    description = models.TextField()
    sensitivity = models.CharField("Sensitivity (can it be used to make assessment by 2015?)",
                                   max_length=3,
                                   choices=LEVEL_CHOICES)
    scale = models.ForeignKey(Scale)
    validity = models.CharField("Scientific Validity",
                                   max_length=3,
                                   choices=LEVEL_CHOICES)
    ease_of_communication = models.CharField("How easy can it be communicated?",
                                   max_length=3,
                                   choices=LEVEL_CHOICES)
    sources = models.CharField("Data Sources",
                            max_length=250)
    requirements = models.TextField()
    measurer = models.CharField("Who's responsible for measuring?",
                            max_length=250)
    conventions = models.CharField("Other conventions/processes using indicator",
                            max_length=250)
    links = models.TextField()

    def __unicode__(self):
        return self.title

class AichiTarget(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    indicators = models.ForeignKey(AichiIndicator, related_name="relevant_target")
    other_indicators = models.ForeignKey(AichiIndicator, related_name="other_targets")

    def __unicode__(self):
        return self.title

class AichiGoal(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    targets = models.ForeignKey(AichiTarget)

    def __unicode__(self):
        return self.title

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
    title = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('self',
                                null=True,
                                blank=True,
                                related_name='children')

    def __unicode__(self):
        return self.title

class EuTarget(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actions = models.ManyToManyField(EuAction)

    def __unicode__(self):
        return self.title
