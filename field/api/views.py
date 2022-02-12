from rest_framework import viewsets

from field.api.serializers import FieldSerializer
from field.models import Field


class FieldRESTView(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()
