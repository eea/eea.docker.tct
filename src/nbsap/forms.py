from django import forms
from django.conf import settings
from django.forms import widgets

from pagedown.widgets import PagedownWidget
from models import NationalObjective


class NationalObjectiveForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=PagedownWidget)
    description = forms.CharField(widget=PagedownWidget,
                                  required=False)

    def __init__(self, *args, **kwargs):

        self.objective = kwargs.pop('objective', None)
        self.parent_objective = kwargs.pop('parent_objective', None)
        lang = kwargs.pop('lang', None)

        super(NationalObjectiveForm, self).__init__(*args, **kwargs)

        if self.objective:
            title = getattr(self.objective, 'title_%s' % lang, None)
            description = getattr(self.objective, 'description_%s' % lang, None)

            self.fields['title'].initial = title
            self.fields['description'].initial = description
            self.fields['language'].initial = lang

    def save(self):

        objective = self.objective or NationalObjective()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']

        setattr(objective, 'title_%s' % lang, title)
        setattr(objective, 'description_%s' % lang, description)

        if self.parent_objective:
            objective.parent = self.parent_objective

        objective.save()

        return objective
