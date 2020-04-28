from rest_framework import serializers

from post.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class TagTitleSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)

    class Meta:
        ref_name = None
