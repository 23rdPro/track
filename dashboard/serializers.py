from rest_framework import serializers

from dashboard.models import (
    Dashboard,

)
from field.serializers import FieldSerializer


class DashboardSerializer(serializers.HyperlinkedModelSerializer):
    field = FieldSerializer(many=True)
    publication = serializers.StringRelatedField(many=True)
    pk = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Dashboard
        fields = ['url', 'pk', 'field', 'publication']
