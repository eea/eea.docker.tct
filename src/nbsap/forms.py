from django import forms
from django.conf import settings
from django.forms import widgets
from tinymce.widgets import TinyMCE

from pagedown.widgets import PagedownWidget
from models import NationalObjective, NationalAction


class NationalObjectiveForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 25}),
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


class NationalActionForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    description = forms.CharField(widget=PagedownWidget)

    def __init__(self, *args, **kwargs):

        self.action = kwargs.pop('action', None)
        self.objective = kwargs.pop('objective')
        lang = kwargs.pop('lang', None)

        super(NationalActionForm, self).__init__(*args, **kwargs)

        description = getattr(self.action, 'description_%s' % lang, None)

        self.fields['description'].initial = description
        self.fields['language'].initial = lang

    def save(self):

        action = self.action or NationalAction()
        lang = self.cleaned_data['language']
        description = self.cleaned_data['description']

        setattr(action, 'description_%s' % lang, description)
        setattr(action, 'code', self.objective.code)

        action.save()
        action.objective = [self.objective]

        action.save()

        return action
