from django.contrib import admin
from .models import Dashboard


class DashboardAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'updated_at', 'field', 'pk']


admin.site.register(Dashboard, DashboardAdmin)

