from rest_framework import serializers

from field.models import Field
from guide.api.serializers import GuideSerializer


class FieldSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    guide = GuideSerializer(required=False)
    # todo handle delete for un-submitted forms !signals

    class Meta:
        model = Field
        fields = ['url', 'pk', 'field', 'aoc', 'guide']
