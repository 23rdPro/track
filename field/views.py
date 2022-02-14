from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from dashboard.models import Dashboard
from field.models import Field


class CreateFieldView(LoginRequiredMixin, CreateView):
    model = Field
    fields = ['field', 'aoc']
    success_url = reverse_lazy('dashboard:list')

    def get_template_names(self):
        qs_count = Dashboard.objects.filter(
            created_at__date=timezone.now()).count()
        if qs_count <= 6:
            return 'field/create.html'
        return 'dashboard_alert.html'


class ListFieldView(LoginRequiredMixin, ListView):
    paginate_by = 25
    template_name = 'field/list.html'

    def get_queryset(self):
        u = self.request.user
        qs = Field.objects.filter(dashboard_field__user=u)
        return qs


class UpdateFieldView(LoginRequiredMixin, UpdateView):
    fields = ['field', 'aoc']
    success_url = reverse_lazy('dashboard:list')

    def get_queryset(self):
        u = self.request.user
        qs = Field.objects.filter(dashboard_field__user=u)
        return qs

    def get_template_names(self):
        num = Dashboard.objects.filter(created_at__date=timezone.now()).count()
        if num <= 60:
            return 'field/update.html'
        return 'dashboard_alert.html'


class DeleteFieldView(LoginRequiredMixin, DeleteView):
    model = Field
    success_url = reverse_lazy('dashboard:list')
