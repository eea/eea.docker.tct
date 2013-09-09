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

admin.site.register(NationalStrategy)

admin.site.register(SEBIIndicator)

admin.site.register(EuAction)
admin.site.register(EuIndicator)
admin.site.register(EuTarget)
