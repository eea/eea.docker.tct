from django.contrib import admin
from nbsap.models import *

admin.site.register(Link)
admin.site.register(Scale)

admin.site.register(AichiGoal)
admin.site.register(AichiTarget)

class AichiIndicatorAdmin(admin.ModelAdmin):
    fields = ('title',)
admin.site.register(AichiIndicator, AichiIndicatorAdmin)


admin.site.register(NationalAction)
admin.site.register(NationalObjective)


class EuAichiStrategyAdmin(admin.ModelAdmin):
    list_display = ('eu_target', 'get_targets')
admin.site.register(EuAichiStrategy, EuAichiStrategyAdmin)

class EuIndicatorToAichiStrategyAdmin(admin.ModelAdmin):
    list_display = ('eu_indicator', 'get_targets')
admin.site.register(EuIndicatorToAichiStrategy, EuIndicatorToAichiStrategyAdmin)

admin.site.register(NationalStrategy)

admin.site.register(EuAction)

class EuIndicatorAdmin(admin.ModelAdmin):
    list_display = ('title', 'indicator_type', 'code', 'get_indicators')
    list_filter = ('indicator_type',)
admin.site.register(EuIndicator, EuIndicatorAdmin)

admin.site.register(EuTarget)
