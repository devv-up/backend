from rest_framework import serializers

from post.models import Like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        depth = 1
        fields = ('user', 'post')


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post')
