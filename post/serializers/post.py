from typing import Any, Dict, TypeVar

from django.db import models
from rest_framework import serializers

from post.models import Comment, Post

from .comment import CommentSerializer

T = TypeVar('T', bound=models.Model)


class PostSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')

    class Meta:
        model = Post
        depth = 1
        fields = ('id',
                  'title',
                  'content',
                  'location',
                  'capacity',
                  'date',
                  'timeOfDay',
                  'createdDate',
                  'author',
                  'category',
                  'tags')


class PostDetailSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj: Post) -> Dict[str, Any]:
        comments = Comment.objects.filter(post=obj.id, is_active=True)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = Post
        depth = 1
        fields = ('id',
                  'title',
                  'content',
                  'location',
                  'capacity',
                  'date',
                  'timeOfDay',
                  'createdDate',
                  'author',
                  'category',
                  'tags',
                  'comments')


class PostCreateSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')

    class Meta:
        model = Post
        fields = ('id',
                  'title',
                  'content',
                  'location',
                  'capacity',
                  'date',
                  'timeOfDay',
                  'author',
                  'category',
                  'tags')


class PostPatchSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')

    def update(self, instance: T, validated_data: Dict[str, Any]) -> Post:
        time_of_day = validated_data.get('timeOfDay')
        if time_of_day is not None:
            validated_data.update(time_of_day=time_of_day)
        return super().update(instance, validated_data)

    class Meta:
        model = Post
        fields = ('id',
                  'title',
                  'content',
                  'location',
                  'capacity',
                  'date',
                  'timeOfDay',
                  'tags')
