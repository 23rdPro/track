from rest_framework import serializers

from guide.models import (
    StarterGuide,
    IntermediateGuide,
    AdvancedGuide,
    Guide,
    Article)


# todo write view > route to use link
class StarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarterGuide
        fields = [
            'title',
            'description',
            'link'
        ]


class IntermediateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntermediateGuide
        fields = ['title', 'description', 'link']


class AdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedGuide
        fields = ['title', 'description', 'link']


class ArticleSerializer(serializers.ModelSerializer):
    starter = StarterSerializer(many=True)
    intermediate = IntermediateSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['starter', 'intermediate', 'advanced']


class PDFSerializer(serializers.ModelSerializer):
    starter = StarterSerializer(many=True)
    intermediate = IntermediateSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['starter', 'intermediate', 'advanced']


class KlassSerializer(serializers.ModelSerializer):
    starter = StarterSerializer(many=True)
    intermediate = IntermediateSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['starter', 'intermediate', 'advanced']


class VideoSerializer(serializers.ModelSerializer):
    starter = StarterSerializer(many=True)
    intermediate = IntermediateSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['starter', 'intermediate', 'advanced']


class QuestionSerializer(serializers.ModelSerializer):
    starter = StarterSerializer(many=True)
    intermediate = IntermediateSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['starter', 'intermediate', 'advanced']


class GuideSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)
    pdf = PDFSerializer(required=False)
    klass = KlassSerializer(required=False)
    video = VideoSerializer(required=False)
    question = QuestionSerializer(required=False)

    class Meta:
        model = Guide
        fields = [
            'article',
            'pdf',
            'klass',
            'video',
            'question'
        ]
