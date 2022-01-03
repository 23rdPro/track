from rest_framework import viewsets

from field.models import Field
from field.serializers import FieldSerializer


class FieldRESTView(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()
