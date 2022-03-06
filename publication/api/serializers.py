from rest_framework import serializers

from publication.models import Publication


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publication
        fields = ['author', 'title', 'description', 'upload_pdf']
