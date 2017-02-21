from django.contrib import admin
from tct.models import *

admin.site.register(Link)
admin.site.register(Scale)

admin.site.register(AichiGoal)
admin.site.register(AichiTarget)

admin.site.register(CMSGoal)
admin.site.register(CMSTarget)

admin.site.register(RamsarGoal)
admin.site.register(RamsarTarget)


class AichiIndicatorAdmin(admin.ModelAdmin):
    fields = ('title',)


admin.site.register(AichiIndicator, AichiIndicatorAdmin)
admin.site.register(NationalAction)
admin.site.register(NationalObjective)


class EuAichiStrategyAdmin(admin.ModelAdmin):
    pass
    # TODO
    # list_display = ('eu_target', 'get_targets')


admin.site.register(EuAichiStrategy, EuAichiStrategyAdmin)


class EuIndicatorToAichiStrategyAdmin(admin.ModelAdmin):
    list_display = ('eu_indicator', 'get_targets_code_stringify')


admin.site.register(EuIndicatorToAichiStrategy,
                    EuIndicatorToAichiStrategyAdmin)
admin.site.register(NationalStrategy)
admin.site.register(EuAction)


class EuIndicatorAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'indicator_type', 'get_indicators')
    list_filter = ('indicator_type',)


admin.site.register(EuIndicator, EuIndicatorAdmin)


class EuTargetAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'get_indicators')


admin.site.register(EuTarget, EuTargetAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Region, RegionAdmin)
admin.site.register(TCTPage)
admin.site.register(NavbarLink)
