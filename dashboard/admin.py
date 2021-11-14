from django.contrib import admin
from .models import (
    Dashboard,
    Field,
    Guide,
    AdvancedGuide,
    IntermediateGuide,
    StarterGuide
)


admin.site.register(Dashboard)
admin.site.register(Field)
admin.site.register(Guide)
admin.site.register(StarterGuide)
admin.site.register(IntermediateGuide)
admin.site.register(AdvancedGuide)
