from typing import Any

from rest_framework import serializers

from post.models import Category, Comment, Post, Tag
from user.models import User


class TempUserSerializer(serializers.ModelSerializer):
    """
    This serializer will be used until the UserSerializer from
    the user app is created.
    """
    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class CommentSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(source='created_date')
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        source='parent_comment',
        required=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(CommentSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'createdDate',
                  'parentComment', 'author', 'is_active')


class PostSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')
    comments = CommentSerializer(many=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(PostSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Post
        depth = 1
        fields = ('id', 'title', 'content', 'location', 'capacity',
                  'date', 'timeOfDay', 'createdDate', 'author',
                  'category', 'tags', 'comments')
        read_only_fields = ['comments']
