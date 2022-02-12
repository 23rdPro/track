from rest_framework import serializers

from guide.models import BasicGuide, AdvancedGuide, Guide, Article


class BasicGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicGuide
        fields = ['title', 'description', 'link']


class AdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedGuide
        fields = ['title', 'description', 'link']


class ArticleSerializer(serializers.ModelSerializer):
    basic = BasicGuideSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['basic', 'advanced']


class PDFSerializer(serializers.ModelSerializer):
    basic = BasicGuideSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['basic', 'advanced']


class KlassSerializer(serializers.ModelSerializer):
    basic = BasicGuideSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['basic', 'advanced']


class VideoSerializer(serializers.ModelSerializer):
    basic = BasicGuideSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['basic', 'advanced']


class QuestionSerializer(serializers.ModelSerializer):
    basic = BasicGuideSerializer(many=True)
    advanced = AdvancedSerializer(many=True)

    class Meta:
        model = Article
        fields = ['basic', 'advanced']


class GuideSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(required=False)
    pdf = PDFSerializer(required=False)
    klass = KlassSerializer(required=False)
    video = VideoSerializer(required=False)
    question = QuestionSerializer(required=False)

    class Meta:
        model = Guide
        fields = ['article', 'pdf', 'klass', 'video', 'question']
