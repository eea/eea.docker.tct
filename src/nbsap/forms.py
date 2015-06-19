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
    AichiTarget, EuAction, EuIndicator, EuIndicatorToAichiStrategy,
    EuAichiStrategy, NationalIndicator
)
from nbsap.utils import remove_tags, RE_CODE, RE_DIGIT_CODE, RE_ACTION_CODE

MAPPING_ERROR = 'Cannot use the same {} Target for both Most relevant and Other'


def validate_code(value):
    if not RE_CODE.match(value):
        raise ValidationError(_('%(code)s is not a valid code. (Ex: 1.1)') %
                              {'code': value})


def validate_simple_digit_code(value):
    if not RE_DIGIT_CODE.match(value):
        raise ValidationError(_('%(code)s is not a valid code. (Ex: 1)') %
                              {'code': value})


def validate_action_code(value):
    if not RE_ACTION_CODE.match(value):
        raise ValidationError(_('%(code)s is not a valid code. (Ex: 1, 1a)') %
                              {'code': value})


class TextCleanedHtml(forms.CharField):
    def to_python(self, value):
        value = super(TextCleanedHtml, self).to_python(value)
        return remove_tags(BeautifulSoup(value).prettify())


class ChoicesMixin(object):
    def _get_choices(self, name, queryset, attr):
        return sorted(
            [(x.pk, name + ' ' + '-'.join([str(getattr(x, a)) for a in attr]))
             for x in queryset],
            key=lambda el: el[1].split()[1])


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


class NationalActionForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea, required=False)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}))

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


class EuTargetForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}),
        required=False)

    def __init__(self, *args, **kwargs):
        self.target = kwargs.pop('target', None)
        lang = kwargs.pop('lang', None)

        super(EuTargetForm, self).__init__(*args, **kwargs)

        if self.target:
            title = getattr(self.target, 'title_%s' % lang, None)
            description = getattr(self.target,
                                  'description_%s' % lang, None)
            self.fields['title'].initial = title
            self.fields['description'].initial = description
            if 'code' in self.fields:
                self.fields['code'].initial = self.target.code

        self.fields['language'].initial = lang

    def save(self):
        target = self.target or EuTarget()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']
        code = self.cleaned_data.get('code', None)

        setattr(target, 'title_%s' % lang, title)
        setattr(target, 'description_%s' % lang, description)

        if code:
            target.code = code
        target.save()

        return target


class EuTargetEditForm(EuTargetForm):
    code = forms.CharField(
        max_length=16, validators=[validate_simple_digit_code])

    def clean_code(self):
        code = self.cleaned_data['code']
        if code == self.target.code:
            return code
        try:
            EuTarget.objects.get(code=code)
            raise ValidationError('Code already exists.')
        except EuTarget.DoesNotExist:
            pass
        return code


class EuStrategyActivityForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea)
    description = TextCleanedHtml(
        widget=TinyMCE(attrs={'cols': 80, 'rows': 25}), required=False)

    def __init__(self, *args, **kwargs):
        self.activity = kwargs.pop('activity', None)
        self.target = kwargs.pop('target')
        self.parent = kwargs.pop('parent', None)
        lang = kwargs.pop('lang', None)

        super(EuStrategyActivityForm, self).__init__(*args, **kwargs)

        title = getattr(self.activity, 'title_%s' % lang, None)
        description = getattr(self.activity, 'description_%s' % lang, None)

        self.fields['title'].initial = title
        self.fields['description'].initial = description
        self.fields['language'].initial = lang
        if self.activity:
            self.fields['code'].initial = self.activity.code

    def save(self):
        activity = self.activity or EuAction()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        code = self.cleaned_data.get('code', None)
        description = self.cleaned_data['description']
        setattr(activity, 'title_%s' % lang, title)
        setattr(activity, 'description_%s' % lang, description)
        activity.parent = self.parent
        activity.code = code or activity.get_next_code(self.target)

        activity.save()
        if not self.parent:
            activity.target = [self.target]
            activity.save()

        for subaction in activity.subactions():
            subaction.update_code()
            subaction.save()
        activity.save()

        return activity


class EuStrategyActivityEditForm(EuStrategyActivityForm):
    code = forms.CharField(max_length=16, validators=[validate_action_code])

    def clean_code(self):
        code = self.cleaned_data['code']
        if code == self.activity.code:
            return code
        try:
            EuAction.objects.get(code=code)
            raise ValidationError('Code already exists.')
        except EuAction.DoesNotExist:
            pass
        return code


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
    def comp_rgx(self, title):
        match = RE_ACTION_CODE.match(title[1])
        if not match:
            return []
        groups = match.groups()
        ret_list = [int(groups[0])]
        ret_list.extend(groups[1:])
        return ret_list

    def comp(self, title):
        code = title[1].split()[1]
        to_list = code.split('.')

        return [int(el) for el in to_list]

    def get_choices(self, string, mytype, isString=False, use_regex=False):
        result = [(element.pk, "%s %s" % (string, element.code.upper()))
                  for element in mytype.objects.all()]

        if isString:
            return sorted(result, key=lambda x: x[1].split()[1])
        if use_regex:
            return sorted(result, key=self.comp_rgx)
        return sorted(result, key=self.comp)

    def get_element_by_pk(self, mytype, u_pk):
        return mytype.objects.filter(pk=int(u_pk)).all()[0]

    nat_objective = forms.ChoiceField(choices=[])
    aichi_goal = forms.ChoiceField(choices=[])
    aichi_target = forms.ChoiceField(choices=[])
    other_targets = chosenforms.ChosenMultipleChoiceField(
        choices=[], required=False, overlay="Select target...")

    if settings.EU_STRATEGY:
        eu_targets = chosenforms.ChosenMultipleChoiceField(
            choices=[], required=False, overlay="Select EU target...",
        )
        eu_actions = chosenforms.ChosenMultipleChoiceField(
            choices=[], required=False, overlay="Select EU actions...",
        )

    def clean(self):
        cleaned_data = super(NationalStrategyForm, self).clean()
        aichi_targets = [cleaned_data['aichi_target']]
        other_aichi_targets = cleaned_data['other_targets']

        if set(aichi_targets) & set(other_aichi_targets):
            raise ValidationError(_(MAPPING_ERROR.format('AICHI')))

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.pop('strategy', None)
        super(NationalStrategyForm, self).__init__(*args, **kwargs)

        self.fields['nat_objective'].choices = self.get_choices(
            'Objective', NationalObjective)
        self.fields['aichi_goal'].choices = self.get_choices('Goal',
                                                             AichiGoal,
                                                             isString=True)
        self.fields['aichi_target'].choices = (
            [('', '----')] + self.get_choices('Target', AichiTarget)
        )
        self.fields['other_targets'].choices = self.get_choices('Target',
                                                                AichiTarget)
        if settings.EU_STRATEGY:
            self.fields['eu_targets'].choices = self.get_choices('Target',
                                                                 EuTarget)
            self.fields['eu_actions'].choices = self.get_choices(
                'Action', EuAction, use_regex=True)

        if self.strategy:
            self.fields['nat_objective'].initial = self.strategy.objective.id
            self.fields['aichi_goal'].initial = (
                self.strategy.relevant_target and
                self.strategy.relevant_target.get_parent_goal().pk)
            self.fields['aichi_target'].initial = (
                self.strategy.relevant_target and
                self.strategy.relevant_target.id
            )
            self.fields['other_targets'].initial = [
                target.id for target in self.strategy.other_targets.all()]
            if settings.EU_STRATEGY:
                self.fields['eu_targets'].initial = [
                    target.id for target in self.strategy.eu_targets.all()]
                self.fields['eu_actions'].initial = [
                    action.id for action in self.strategy.eu_actions.all()]

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
                strategy.eu_targets.add(
                    get_object_or_404(EuTarget, code=ucode))
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


class EuIndicatorForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea, required=False)
    url = forms.CharField(required=False)
    indicator_type = forms.ChoiceField(choices=EuIndicator.TYPES)
    code = forms.CharField(
        max_length=16, validators=[validate_code])

    def __init__(self, *args, **kwargs):
        self.indicator = kwargs.pop('indicator', None)
        lang = kwargs.pop('lang', None)

        super(EuIndicatorForm, self).__init__(*args, **kwargs)

        if self.indicator:
            title = getattr(self.indicator, 'title_%s' % lang, None)
            self.fields['title'].initial = title
            self.fields['url'].initial = self.indicator.url
            self.fields['indicator_type'].initial = (
                self.indicator.indicator_type
            )
            if 'code' in self.fields:
                self.fields['code'].initial = self.indicator.code

        self.fields['language'].initial = lang

    def save(self):
        indicator = self.indicator or EuIndicator()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        code = self.cleaned_data.get('code', None)

        setattr(indicator, 'title_%s' % lang, title)
        indicator.url = self.cleaned_data['url']
        indicator.indicator_type = self.cleaned_data['indicator_type']

        if code:
            indicator.code = code
        indicator.save()

        return indicator


class NationalIndicatorForm(forms.Form):
    language = forms.ChoiceField(choices=settings.LANGUAGES)
    title = forms.CharField(widget=widgets.Textarea, required=True)
    code = forms.CharField(widget=widgets.Textarea, required=True)
    url = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.indicator = kwargs.pop('indicator', None)
        lang = kwargs.pop('lang', None)

        super(NationalIndicatorForm, self).__init__(*args, **kwargs)

        if self.indicator:
            title = getattr(self.indicator, 'title_%s' % lang, None)
            self.fields['title'].initial = title
            self.fields['url'].initial = self.indicator.url
            if 'code' in self.fields:
                self.fields['code'].initial = self.indicator.code

        self.fields['language'].initial = lang

    def clean_code(self):
        code = self.cleaned_data['code']
        if self.indicator and self.indicator.code == code:
            return code
        try:
            NationalIndicator.objects.get(code=code)
            raise ValidationError('Code already exists.')
        except NationalIndicator.DoesNotExist:
            pass
        return code

    def save(self):
        indicator = self.indicator or NationalIndicator()
        lang = self.cleaned_data['language']
        title = self.cleaned_data['title']
        code = self.cleaned_data.get('code', None)

        setattr(indicator, 'title_%s' % lang, title)
        indicator.url = self.cleaned_data['url']

        if code:
            indicator.code = code
        indicator.save()

        return indicator


class NationalIndicatorEditForm(NationalIndicatorForm, ChoicesMixin):
    def __init__(self, *args, **kwargs):
        super(NationalIndicatorEditForm, self).__init__(*args, **kwargs)

    def save(self):
        indicator = super(NationalIndicatorEditForm, self).save()
        return indicator


class EuIndicatorMapForm(forms.Form, ChoicesMixin):
    eu_targets = chosenforms.ChosenMultipleChoiceField(
        overlay="Select EU target...", required=False)
    other_eu_targets = chosenforms.ChosenMultipleChoiceField(
        overlay="Select EU target...", required=False)
    aichi_targets = chosenforms.ChosenMultipleChoiceField(
        overlay="Select Aichi target...", required=False)
    other_aichi_targets = chosenforms.ChosenMultipleChoiceField(
        overlay="Select Aichi target...", required=False)

    def __init__(self, *args, **kwargs):
        self.indicator = kwargs.pop('indicator', None)
        super(EuIndicatorMapForm, self).__init__(*args, **kwargs)
        target_choices = self._get_choices(
            'Target', EuTarget.objects.all(), ['code']
        )
        self.fields['eu_targets'].choices = target_choices
        self.fields['other_eu_targets'].choices = target_choices
        self.fields['eu_targets'].initial = (self.indicator.targets
                                             .values_list('pk', flat=True))
        self.fields['other_eu_targets'].initial = (
            self.indicator.other_targets.values_list('pk', flat=True)
        )
        aichi_target_choices = self._get_choices(
            'Target', AichiTarget.objects.all(), ['code']
        )
        self.fields['aichi_targets'].choices = aichi_target_choices
        self.fields['other_aichi_targets'].choices = aichi_target_choices

        try:
            initial = (
                EuIndicatorToAichiStrategy.objects
                .filter(eu_indicator=self.indicator)[0]
                .aichi_targets.values_list('pk', flat=True)
            )
            initial_other = (
                EuIndicatorToAichiStrategy.objects
                .filter(eu_indicator=self.indicator)[0]
                .other_aichi_targets.values_list('pk', flat=True)
            )
        except IndexError:
            initial = None
            initial_other = None
        self.fields['aichi_targets'].initial = initial
        self.fields['other_aichi_targets'].initial = initial_other

    def clean(self):
        cleaned_data = super(EuIndicatorMapForm, self).clean()
        eu_targets = cleaned_data['eu_targets']
        other_eu_targets = cleaned_data['other_eu_targets']
        aichi_targets = cleaned_data['aichi_targets']
        other_aichi_targets = cleaned_data['other_aichi_targets']

        errors = []
        if set(eu_targets) & set(other_eu_targets):
            errors.append(_(MAPPING_ERROR.format('EU')))
        if set(aichi_targets) & set(other_aichi_targets):
            errors.append(_(MAPPING_ERROR.format('AICHI')))

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    def save(self):
        self.indicator.targets = self.cleaned_data['eu_targets']
        self.indicator.other_targets = self.cleaned_data['other_eu_targets']
        self.indicator.save()
        try:
            ita = (EuIndicatorToAichiStrategy.objects
                   .filter(eu_indicator=self.indicator))[0]
        except IndexError:
            ita = EuIndicatorToAichiStrategy.objects.create(
                eu_indicator=self.indicator)

        ita.aichi_targets = self.cleaned_data['aichi_targets']
        ita.other_aichi_targets = self.cleaned_data['other_aichi_targets']
        ita.save()


class NationalIndicatorMapForm(forms.Form, ChoicesMixin):
    nat_objectives = chosenforms.ChosenMultipleChoiceField(
        overlay="Select National Objective...", required=False)
    other_nat_objectives = chosenforms.ChosenMultipleChoiceField(
        overlay="Select National Objective...", required=False)

    def __init__(self, *args, **kwargs):
        self.indicator = kwargs.pop('indicator', None)
        super(NationalIndicatorMapForm, self).__init__(*args, **kwargs)
        nat_objectives = self._get_choices(
            'Objective', NationalObjective.objects.all(), ['code']
        )
        self.fields['nat_objectives'].choices = nat_objectives
        self.fields['other_nat_objectives'].choices = nat_objectives
        self.fields['nat_objectives'].initial = (
            self.indicator.nat_objectives.values_list('pk', flat=True))
        self.fields['other_nat_objectives'].initial = (
            self.indicator.other_nat_objectives.values_list('pk', flat=True)
        )


    def clean(self):
        cleaned_data = super(NationalIndicatorMapForm, self).clean()
        nat_objectives = cleaned_data['nat_objectives']
        other_nat_objectives = cleaned_data['other_nat_objectives']
        errors = []
        if set(nat_objectives) & set(other_nat_objectives):
            errors.append(_(MAPPING_ERROR.format('OBJ')))

        if errors:
            raise ValidationError(errors)

        return cleaned_data

    def save(self):
        self.indicator.nat_objectives = self.cleaned_data['nat_objectives']
        self.indicator.other_nat_objectives = (
            self.cleaned_data['other_nat_objectives']
        )
        self.indicator.save()


class EuAichiStrategyForm(forms.Form, ChoicesMixin):
    eu_target = forms.ChoiceField()
    aichi_targets = chosenforms.ChosenMultipleChoiceField(
        overlay="Select target...")
    other_aichi_targets = chosenforms.ChosenMultipleChoiceField(
        overlay="Select target...", required=False)
    eu_indicators = chosenforms.ChosenMultipleChoiceField(
        overlay="Select indicator...", required=False)
    other_eu_indicators = chosenforms.ChosenMultipleChoiceField(
        overlay="Select indicator...", required=False)

    def __init__(self, *args, **kwargs):
        self.strategy = kwargs.pop('strategy', None)
        super(EuAichiStrategyForm, self).__init__(*args, **kwargs)

        target_choices = self._get_choices(
            'Target', AichiTarget.objects.all(), ['code'])
        indicator_choices = self._get_choices(
            'Indicator', EuIndicator.objects.all(), ['full_code'])

        self.fields['aichi_targets'].choices = target_choices
        self.fields['other_aichi_targets'].choices = target_choices
        self.fields['eu_indicators'].choices = indicator_choices
        self.fields['other_eu_indicators'].choices = indicator_choices

        if self.strategy:
            self.fields['aichi_targets'].initial = (
                self.strategy.aichi_targets
                .values_list('pk', flat=True)
            )
            self.fields['other_aichi_targets'].initial = (
                self.strategy.other_aichi_targets
                .values_list('pk', flat=True)
            )
            self.fields['eu_indicators'].initial = (
                self.strategy.eu_target.indicators
                .values_list('pk', flat=True)
            )
            self.fields['other_eu_indicators'].initial = (
                self.strategy.eu_target.other_indicators
                .values_list('pk', flat=True)
            )
            del self.fields['eu_target']
        else:
            existing_strategies = (EuAichiStrategy.objects
                                   .values_list('eu_target', flat=True))
            self.fields['eu_target'].choices = self._get_choices(
                'Target',
                EuTarget.objects.exclude(id__in=existing_strategies).all(),
                ['pk']
            )

    def clean(self):
        cleaned_data = super(EuAichiStrategyForm, self).clean()
        aichi_targets = cleaned_data['aichi_targets']
        other_aichi_targets = cleaned_data['other_aichi_targets']
        eu_indicators = cleaned_data['eu_indicators']
        other_eu_indicators = cleaned_data['other_eu_indicators']

        if set(aichi_targets) & set(other_aichi_targets):
            raise ValidationError(_(MAPPING_ERROR.format('AICHI')))

        if set(eu_indicators) & set(other_eu_indicators):
            raise ValidationError(_(MAPPING_ERROR.format('EU_INDICATORS')))

        return cleaned_data

    def save(self):
        if self.strategy:
            strategy = self.strategy
        else:
            strategy = EuAichiStrategy()
            strategy.eu_target = (EuTarget.objects
                                  .get(pk=self.cleaned_data['eu_target']))
            strategy.save()

        strategy.aichi_targets = (
            AichiTarget.objects
            .filter(pk__in=self.cleaned_data['aichi_targets'])
        )
        strategy.other_aichi_targets = (
            AichiTarget.objects
            .filter(pk__in=self.cleaned_data['other_aichi_targets'])
        )
        strategy.eu_target.indicators = (
            EuIndicator.objects
            .filter(pk__in=self.cleaned_data['eu_indicators'])
        )
        strategy.eu_target.other_indicators = (
            EuIndicator.objects
            .filter(pk__in=self.cleaned_data['other_eu_indicators'])
        )
        strategy.save()
