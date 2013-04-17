"""
Script to migrate data from markdown to HTML
Mihai Tabara @ Eau de web
17.04.2013
"""
from nbsap import models
import markdown2

def f():
    print 'Migrating National Objectives...'
    objectives = models.NationalObjective.objects.all()
    for obj in objectives:
        new_value = markdown2.markdown(obj.description_en)
        obj.description_en = unicode(new_value)
        new_value = markdown2.markdown(obj.description_fr)
        obj.description_fr = unicode(new_value)
        new_value = markdown2.markdown(obj.description_nl)
        obj.description_nl = unicode(new_value)
        obj.save()
    print 'Successfully migrated National Objectives'

    print 'Migrating National Actions...'
    actions = models.NationalAction.objects.all()
    for action in actions:
        new_value = markdown2.markdown(action.description_en)
        action.description_en = unicode(new_value)
        new_value = markdown2.markdown(action.description_fr)
        action.description_fr = unicode(new_value)
        new_value = markdown2.markdown(action.description_nl)
        action.description_nl = unicode(new_value)
        action.save()
    print 'Successfully migrated National Actions'
