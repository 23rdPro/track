from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import viewsets

from field.models import Field
from field.serializers import FieldSerializer


class CreateFieldView(LoginRequiredMixin, CreateView):
    model = Field
    template_name = 'field/create.html'
    fields = ['field', 'aoc']
    success_url = reverse_lazy('dashboard:list')


class FieldRESTView(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()
