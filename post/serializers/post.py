from typing import Any, Dict, TypeVar

from django.db import models
from rest_framework import serializers

from post.api.comment import CommentSerializer
from post.models import Comment, Post

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

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'location',
                  'capacity', 'date', 'timeOfDay', 'author',
                  'category', 'tags')


class PostPatchSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')

    def update(self, instance: T, validated_data: Dict[str, Any]) -> Post:
        time_of_day = validated_data.get('timeOfDay')
        if time_of_day is not None:
            validated_data.update(time_of_day=time_of_day)
        return super().update(instance, validated_data)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'location',
                  'capacity', 'date', 'timeOfDay', 'tags')


class PostQuerySerializer(serializers.Serializer):
    page = serializers.IntegerField(
        required=False,
        help_text='A page number within the paginated result set.\n\n ex) page=1',
    )
    perPage = serializers.IntegerField(
        required=False,
        help_text='Number of results to return per page.\n\n ex) perPage=30',
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
        fields = ('page', 'perPage', 'category', 'tags',
                  'startDate', 'endDate', 'timeOfDay', 'location')


class PostBodySerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        help_text='The title of the post',
    )
    content = serializers.CharField(
        required=True,
        help_text='The content of the post',
    )
    location = serializers.CharField(
        required=True,
        help_text='The location of the meeting',
    )
    capacity = serializers.IntegerField(
        required=True,
        help_text='The capacity of the meeting',
    )
    date = serializers.DateField(
        required=True,
        help_text='The start date of the meeting',
    )
    timeOfDay = serializers.IntegerField(
        required=True,
        help_text='Time of the day of the meeting',
    )
    author = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=User.objects.all(),
        help_text='The author ID of the post',
    )
    category = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Category.objects.all(),
        help_text='The category ID of the post',
    )
    tags = serializers.CharField(
        required=False,
        help_text='Tag titles of the post',
    )

    class Meta:
        ref_name = None
        fields = ('title', 'content', 'location', 'capacity', 'date',
                  'timeOfDay', 'author', 'category', 'tags')


class PostPatchBodySerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        help_text='The title of the post',
    )
    content = serializers.CharField(
        required=True,
        help_text='The content of the post',
    )
    location = serializers.CharField(
        required=True,
        help_text='The location of the meeting',
    )
    capacity = serializers.IntegerField(
        required=True,
        help_text='The capacity of the meeting',
    )
    date = serializers.DateField(
        required=True,
        help_text='The start date of the meeting',
    )
    timeOfDay = serializers.IntegerField(
        required=True,
        help_text='Time of the day of the meeting',
    )
    tags = serializers.CharField(
        required=False,
        help_text='Tag titles of the post',
    )

    class Meta:
        ref_name = None
        fields = ('title', 'content', 'location', 'capacity', 'date',
                  'timeOfDay', 'tags')
