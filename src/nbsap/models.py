from django.db import models

class AichiGoal(models.Model):
    pass

class AichiTarget(models.Model):
    pass

class AichiIndicator(models.Model):
    pass

class NationalAction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.title

class NationalObjective(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    objectives = models.ForeignKey('self',
                                    null=True,
                                    blank=True)
    actions = models.ForeignKey(NationalAction,
                                null=True,
                                blank=True)

    def __unicode__(self):
        return self.title

class EuAction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    objectives = models.ForeignKey('self',
                                   null=True,
                                   blank=True)

    def __unicode__(self):
        return self.title

class EuTarget(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actions = models.ForeignKey(EuAction)

    def __unicode__(self):
        return self.title