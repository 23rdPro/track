from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.views.generic import ListView

from dashboard.models import Dashboard


class DashboardListView(LoginRequiredMixin, ListView):
    paginate_by = 10

    def get_queryset(self):
        u = self.request.user
        qs = Dashboard.objects.filter(user=u).select_related('field')
        return qs

    def get_context_data(self, **kwargs):
        context = super(DashboardListView, self).get_context_data(**kwargs)
        dashboards = cache.get('dashboards')
        if dashboards is None:
            dashboards = self.get_queryset()
            cache.set('dashboards', dashboards)
        context['dashboards'] = dashboards
        context['guide_attributes'] = [
            'Articles', 'PDFs', 'Online Classes',
            'Videos', 'Questions'
        ]
        context['level_attributes'] = ['basic level', 'advanced level']
        return context

    def get_template_names(self):
        if not self.get_queryset().exists():
            return 'dashboard_alert.html'
        return 'dashboard/list.html'
