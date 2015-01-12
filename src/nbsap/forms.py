import re
from bs4 import BeautifulSoup

from django import forms
from django.conf import settings
from django.forms import widgets
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from tinymce.widgets import TinyMCE
from chosen import forms as chosenforms

from nbsap.models import (
    NationalStrategy, NationalObjective, NationalAction, EuTarget, AichiGoal,
    AichiTarget, EuAction
)
from nbsap.utils import remove_tags


RE_CODE = re.compile('(\d+\.)*\d+$')


def validate_code(value):
    if not RE_CODE.match(value):
        raise ValidationError(_('%(code)s is not a valid code. (Ex: 1.1)') %
                              {'code': value})


class TextCleanedHtml(forms.CharField):

    def to_python(self, value):
        value = super(TextCleanedHtml, self).to_python(value)
        return remove_tags(BeautifulSoup(value).prettify())


class NationalObjectiveForm(forms.Form):

    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}),
        required=False)

    def __init__(self, *args, **kwargs):

        self.objective = kwargs.pop('objective', None)
        self.parent_objective = kwargs.pop('parent_objective', None)
        lang = kwargs.pop('lang', None)

        super(NationalObjectiveForm, self).__init__(*args, **kwargs)

        if self.objective:
            title = getattr(self.objective, 'title_%s' % lang, None)
            description = getattr(self.objective,
                                  'description_%s' % lang, None)
            self.fields['title'].initial = title
            self.fields['description'].initial = description
            if 'code' in self.fields:
                self.fields['code'].initial = self.objective.code
        self.fields['language'].initial = lang

    def save(self):
        objective = self.objective or NationalObjective()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']
        code = self.cleaned_data.get('code', None)

        setattr(objective, 'title_%s' % lang, title)
        setattr(objective, 'description_%s' % lang, description)

        if self.parent_objective:
            objective.parent = self.parent_objective
        if code:
            objective.code = code
        objective.save()
        return objective


class NationalObjectiveEditForm(NationalObjectiveForm):

    code = forms.CharField(max_length=16, validators=[validate_code])

    def clean_code(self):
        code = self.cleaned_data['code']
        if code == self.objective.code:
            return code
        try:
            NationalObjective.objects.get(code=code)
            raise ValidationError('Code already exists.')
        except NationalObjective.DoesNotExist:
            pass
        return code


class EuTargetForm(forms.Form):

    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}),
        required=False)

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', None)

        super(EuTargetForm, self).__init__(*args, **kwargs)

        self.fields['language'].initial = lang

    def save(self):
        target = self.target or EuTarget()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']

        setattr(target, 'title_%s' % lang, title)
        setattr(target, 'description_%s' % lang, description)

        target.save()

        return target


class EuTargetEditForm(EuTargetForm):
    pass


class NationalActionForm(forms.Form):

    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea, required=False)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80,'rows': 25}))

    def __init__(self, *args, **kwargs):

        self.action = kwargs.pop('action', None)
        self.objective = kwargs.pop('objective')
        lang = kwargs.pop('lang', None)

        super(NationalActionForm, self).__init__(*args, **kwargs)

        title = getattr(self.action, 'title_%s' % lang, None)
        description = getattr(self.action, 'description_%s' % lang, None)

        self.fields['title'].initial = title
        self.fields['description'].initial = description
        self.fields['language'].initial = lang

    def save(self):
        action = self.action or NationalAction()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']

        setattr(action, 'title_%s' % lang, title)
        setattr(action, 'description_%s' % lang, description)
        setattr(action, 'code', self.objective.code)

        action.save()
        action.objective = [self.objective]
        action.save()
        return action


class AichiGoalForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}))
    title = forms.CharField(widget=widgets.Textarea)

    def __init__(self, *args, **kwargs):

        self.goal = kwargs.pop('goal', None)
        lang = kwargs.pop('lang', None)

        super(AichiGoalForm, self).__init__(*args, **kwargs)

        description = getattr(self.goal, 'description_%s' % lang, None)
        title = getattr(self.goal, 'title_%s' % lang, None)

        self.fields['description'].initial = description
        self.fields['language'].initial = lang
        self.fields['title'].initial = title

    def save(self):
        goal = self.goal or AichiGoal()
        lang = self.cleaned_data['language']
        description = self.cleaned_data['description']
        title = self.cleaned_data['title']

        setattr(goal, 'description_%s' % lang, description)
        setattr(goal, 'code', self.goal.code)
        setattr(goal, 'title_%s' % lang, title)
        goal.save()

     #   for ucode in self.cleaned_data['targets']:
     #       goal.targets.add(get_object_or_404(AichiTarget, code=ucode))
        goal.save()
        return goal


class NationalStrategyForm(forms.Form):

    def comp(self, title):
        code = title[1].split()[1]
        to_list = code.split('.')

        return [int(el) for el in to_list]

    def get_choices(self, string, mytype, isString=False):
        result = [(element.pk, "%s %s" % (string, element.code.upper()))
                  for element in mytype.objects.all()]

        if isString:
            return sorted(result, key=lambda x: x[1].split()[1])
        return sorted(result, key=self.comp)

    def get_element_by_pk(self, mytype, u_pk):
        return mytype.objects.filter(pk=int(u_pk)).all()[0]

    nat_objective = forms.ChoiceField(choices=[])
    aichi_goal = forms.ChoiceField(choices=[])
    aichi_target = forms.ChoiceField(choices=[])
    other_targets = chosenforms.ChosenMultipleChoiceField(choices=[],
                                                          required=False,
                                                          overlay="Select target...")

    if settings.EU_STRATEGY:
        eu_targets = chosenforms.ChosenMultipleChoiceField(choices=[],
                                                           required=False,
                                                           overlay="Select EU target...")
        eu_actions = chosenforms.ChosenMultipleChoiceField(choices=[],
                                                           required=False,
                                                           overlay="Select EU actions...")

    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.pop('strategy', None)
        super(NationalStrategyForm, self).__init__(*args, **kwargs)

        self.fields['nat_objective'].choices = self.get_choices('Objective',
                                                                NationalObjective)
        self.fields['aichi_goal'].choices = self.get_choices('Goal',
                                                             AichiGoal,
                                                             isString=True)
        self.fields['aichi_target'].choices = self.get_choices('Target',
                                                               AichiTarget)
        self.fields['other_targets'].choices = self.get_choices('Target',
                                                                AichiTarget)
        if settings.EU_STRATEGY:
            self.fields['eu_targets'].choices = self.get_choices('Target',
                                                                 EuTarget)
            self.fields['eu_actions'].choices = self.get_choices('Action',
                                                                 EuAction)

        if self.strategy:
            self.fields['nat_objective'].initial = self.strategy.objective.id
            self.fields['aichi_goal'].initial = self.strategy.relevant_target.get_parent_goal().pk
            self.fields['aichi_target'].initial = self.strategy.relevant_target.id
            self.fields['other_targets'].initial = [target.id for target in self.strategy.other_targets.all()]
            if settings.EU_STRATEGY:
                self.fields['eu_targets'].initial = [target.id for target in self.strategy.eu_targets.all()]
                self.fields['eu_actions'].initial = [action.id for action in self.strategy.eu_actions.all()]

    def save(self):
        strategy = self.strategy or NationalStrategy()
        nat_obj = self.get_element_by_pk(
            NationalObjective, self.cleaned_data['nat_objective'])
        aichi_targ = self.get_element_by_pk(
            AichiTarget, self.cleaned_data['aichi_target'])

        setattr(strategy, 'objective', nat_obj)
        setattr(strategy, 'relevant_target', aichi_targ)
        strategy.save()

        strategy.other_targets.clear()
        if settings.EU_STRATEGY:
            strategy.eu_targets.clear()
            strategy.eu_actions.clear()

        for ucode in self.cleaned_data['other_targets']:
            strategy.other_targets.add(get_object_or_404(AichiTarget,
                                                         code=ucode))
        if settings.EU_STRATEGY:
            for ucode in self.cleaned_data['eu_targets']:
                strategy.eu_targets.add(get_object_or_404(EuTarget, code=ucode))
            for ucode in self.cleaned_data['eu_actions']:
                strategy.eu_actions.add(get_object_or_404(EuAction, pk=ucode))

        strategy.save()
        return strategy


class NbsapPageForm(forms.Form):

    lang = forms.ChoiceField(choices=settings.LANGUAGES, label=_('Language'))
    title = forms.CharField(label=_('Title'))
    body = TextCleanedHtml(required=False, label=_('Body'),
                           widget=TinyMCE(attrs={'cols': 80, 'rows': 15}))

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop('lang', None)
        self.page = kwargs.pop('page')
        super(NbsapPageForm, self).__init__(*args, **kwargs)

        title = getattr(self.page, 'title_%s' % lang, None)
        body = getattr(self.page, 'body_%s' % lang, None)

        self.fields['title'].initial = title
        self.fields['body'].initial = body
        self.fields['lang'].initial = lang

    def save(self):
        lang = self.cleaned_data['lang']
        setattr(self.page, 'title_%s' % lang, self.cleaned_data['title'])
        setattr(self.page, 'body_%s' % lang, self.cleaned_data['body'])
        self.page.save()
        return self.page

