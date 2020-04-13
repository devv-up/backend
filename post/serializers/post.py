from typing import Any, Dict, TypeVar

from django.db import models
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from post.api.comment import CommentSerializer
from post.models import Category, Comment, Post, Tag

T = TypeVar('T', bound=models.Model)


class PostSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')

    class Meta:
        model = Post
        depth = 1
        fields = ('id', 'title', 'content', 'location',
                  'capacity', 'date', 'timeOfDay', 'createdDate',
                  'author', 'category', 'tags')


class PostDetailSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')
    comments = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=CommentSerializer(many=True))
    def get_comments(self, obj: Post) -> Dict[str, Any]:
        comments = Comment.objects.filter(post=obj.id, is_active=True)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    class Meta:
        model = Post
        depth = 1
        fields = ('id', 'title', 'content', 'location',
                  'capacity', 'date', 'timeOfDay', 'createdDate',
                  'author', 'category', 'tags', 'comments')


class PostCreateSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        required=True
    )

    class Meta:
        model = Post
        ref_name = None
        fields = ('id', 'title', 'content', 'location',
                  'capacity', 'date', 'timeOfDay', 'author',
                  'category', 'tags')


class PostPatchSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    capacity = serializers.CharField(required=False)
    date = serializers.DateField(required=False)

    timeOfDay = serializers.IntegerField(
        source='time_of_day',
        required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )

    def update(self, instance: T, validated_data: Dict[str, Any]) -> Post:
        time_of_day = validated_data.get('timeOfDay')
        if time_of_day is not None:
            validated_data.update(time_of_day=time_of_day)
        return super().update(instance, validated_data)

    class Meta:
        model = Post
        ref_name = None
        fields = ('id', 'title', 'content', 'location',
                  'capacity', 'date', 'timeOfDay', 'tags')


class PostQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(
        required=False,
        help_text='A page number within the paginated result set.\n\n ex) page=1',
    )
    pageSize = serializers.IntegerField(
        required=False,
        help_text='Number of results to return per page.\n\n ex) pageSize=30',
    )
    category = serializers.CharField(
        required=False,
        help_text='The Category title.\n\n ex) category=project',
    )
    tags = serializers.CharField(
        required=False,
        help_text='The Tag titles.\n\n ex) tags=python,django',
    )
    startDate = serializers.DateField(
        required=False,
        help_text='The Start date.\n\n ex) startDate=2020-01-01',
    )
    endDate = serializers.DateField(
        required=False,
        help_text='The End date.\n\n ex) endDate=2020-02-02',
    )
    timeOfDay = serializers.IntegerField(
        required=False,
        help_text='The time of day of studies or projects.\n\n ex) timeOfDay=1',
    )
    location = serializers.CharField(
        required=False,
        help_text='The location of studies or projects.\n\n ex) location=seoul',
    )

    class Meta:
        fields = ('page',
                  'pageSize',
                  'category',
                  'tags',
                  'startDate',
                  'endDate',
                  'timeOfDay',
                  'location')
