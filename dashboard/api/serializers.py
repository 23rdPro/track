from rest_framework import serializers

from dashboard.models import Dashboard
from field.api.serializers import FieldSerializer
from users.api.serializers import UserSerializer


class DashboardSerializer(serializers.HyperlinkedModelSerializer):
    field = FieldSerializer()
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Dashboard
        fields = ['url', 'pk', 'user', 'field']
