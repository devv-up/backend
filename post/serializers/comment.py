from typing import Any

from rest_framework import serializers

from post.models import Comment, Post
from user.models import User


class CommentSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(source='created_date')
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.filter(is_active=True),
        source='parent_comment',
        required=False
    )

    class Meta:
        model = Comment
        depth = 1
        fields = ('id', 'content', 'createdDate', 'parentComment',
                  'author', 'is_active')


class CommentCreateSerializer(serializers.ModelSerializer):
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.filter(is_active=True),
        source='parent_comment',
        required=False
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        create_body = kwargs.pop('create_body', False)
        super().__init__(*args, **kwargs)

        if create_body:
            self.fields.pop('id')
            self.fields['content'] = serializers.CharField(
                required=True,
                help_text='The content of the comment',
            )
            self.fields['post'] = serializers.PrimaryKeyRelatedField(
                required=True,
                queryset=Post.objects.filter(is_active=True),
                help_text='The post ID of the comment',
            )
            self.fields['parentComment'] = serializers.PrimaryKeyRelatedField(
                required=False,
                queryset=Comment.objects.filter(is_active=True),
                help_text='The parent comment ID of the comment',
            )
            self.fields['author'] = serializers.PrimaryKeyRelatedField(
                required=False,
                queryset=User.objects.filter(is_active=True),
                help_text='The author ID of the comment',
            )

    class Meta:
        model = Comment
        ref_name = None
        fields = ('id', 'content', 'post', 'parentComment',
                  'author')


class CommentPutBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        ref_name = None
        fields = ('content',)
