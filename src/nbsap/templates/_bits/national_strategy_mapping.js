$(".chzn-select").chosen();
$(function() {
    function forbidChoicesIntersection(selector1, selector2) {
        $(selector1).on('change', function() {
            if (this.value && $(selector2).value) {
                $("option", this).each(function() {
                    var option2 = $(selector2).find('option[value=' + this.value + ']');
                    if (this.selected) {
                        option2.hide();
                    } else {
                        option2.show();
                    }
                });
                $(selector2).trigger('chosen:updated');
            }
        }).change();
    }

    function forbidCrossChoicesIntersection(name, nameOther) {
        var selectorTargets = 'select[name=' + name + ']';
        var selectorOtherTargets = 'select[name=' + nameOther + ']';

        forbidChoicesIntersection(selectorTargets, selectorOtherTargets);
        forbidChoicesIntersection(selectorOtherTargets, selectorTargets);
    }
    forbidCrossChoicesIntersection('aichi_targets', 'other_targets');

    showObjectiveCodeValue('nat_objective',
        '.objective_text',
        "{% url 'objective_title' pk=1 %}");

    showTargetCodeValue('aichi_targets',
        '.target_text',
        "{% url 'aichi_target_title' pk=1 %}");

    showTargetCodeValue('other_targets',
        '.other_target_text',
        "{% url 'aichi_target_title' pk=1 %}");

    showTargetCodeValue('eu_targets',
        '.eu_target_text',
        "{% url 'eu_target_title' pk=1 %}");

    showActionCodeValue('eu_actions',
        '.actions_text',
        "{% url 'action_title' pk=1 %}");
});
