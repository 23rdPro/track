from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView
from rest_framework import viewsets

from dashboard.models import Dashboard
from field.models import Field
from field.serializers import FieldSerializer


class CreateFieldView(LoginRequiredMixin, CreateView):
    model = Field
    template_name = 'field/create.html'
    fields = ['field', 'aoc']
    success_url = reverse_lazy('dashboard:list')

    def get_template_names(self):
        qs_count = Dashboard.objects.filter(created_at__date=timezone.now()).count()
        if qs_count <= 4:
            return 'field/create.html'
        return 'dashboard_alert.html'


class FieldRESTView(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()
