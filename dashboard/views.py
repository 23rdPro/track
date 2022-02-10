from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from dashboard.models import Dashboard


class DashboardListView(LoginRequiredMixin, ListView):
    context_object_name = 'dashboards'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Dashboard.objects.filter(user=user).select_related('field')

    def get_context_data(self, **kwargs):
        context = super(DashboardListView, self).get_context_data(**kwargs)
        context['guide_attributes'] = ['Articles', 'PDFs', 'Online Classes', 'Videos', 'Questions']
        context['level_attributes'] = ['basic level', 'advanced level']
        return context

    def get_template_names(self):
        if not self.get_queryset():
            return 'dashboard_alert.html'
        return 'dashboard/list.html'
