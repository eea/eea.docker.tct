from django.shortcuts import render, get_object_or_404
from django.http import Http404
from nbsap import models
from nbsap.utils import sort_by_code, get_adjacent_objects

from django.views.generic import TemplateView


class ListGoals(TemplateView):
    model = models.CMSGoal
    template_name = 'cms/list_goals.html'

    def get(self, request, *args, **kwargs):
        goals = self.model.objects.order_by(
            'code').all().prefetch_related('targets')
        return render(request, self.template_name, {
            'goals': goals,
        })


class ListTargets(TemplateView):
    goal_model = models.CMSGoal
    target_model = models.CMSTarget
    template_name = 'cms/list_targets.html'

    def get(self, request, *args, **kwargs):
        try:
            code = kwargs['code']
        except KeyError:
            code = None

        if code:
            current_goal = get_object_or_404(self.goal_model, code=code)
            targets = current_goal.targets.all()
        else:
            current_goal = None
            targets = self.target_model.objects.all()

        goals = self.goal_model.objects.order_by(
            'code').all().prefetch_related('targets')
        return render(request, self.template_name, {
            'current_goal': current_goal,
            'goals': goals,
            'targets': targets,
        })


class TargetDetails(TemplateView):
    goal_model = models.CMSGoal
    target_model = models.CMSTarget
    id_type = 'cms_target_id'
    template_name = 'cms/target_details.html'

    def get(self, request, *args, **kwargs):
        try:
            code = kwargs['code']
        except KeyError:
            code = None

        target_id = kwargs[self.id_type]

        target = get_object_or_404(self.target_model, pk=target_id)
        target.related_targets = target.aichi_targets.all()

        if not code:
            code = target.get_parent_goal().code

        goals = self.goal_model.objects.order_by(
            'code').all().prefetch_related('targets')
        current_goal = get_object_or_404(self.goal_model, code=code)
        all_targets = sort_by_code(self.target_model.objects.all())
        targets = sort_by_code(current_goal.targets.all())

        if target not in targets:
            raise Http404

        previous_target, next_target = get_adjacent_objects(
            all_targets, target)

        return render(request, self.template_name, {
            'goals': goals,
            'targets': targets,
            'all_targets': all_targets,
            'target': target,
            'previous_target': previous_target,
            'next_target': next_target,
            'target_code': code,
        })
