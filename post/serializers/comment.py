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

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'parentComment',
                  'author')


class CommentPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content')


class CommentCreateBodySerializer(serializers.Serializer):
    content = serializers.CharField(
        required=True,
        help_text='The content of the comment',
    )
    post = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Post.objects.all(),
        help_text='The post ID of the comment',
    )
    author = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=User.objects.all(),
        help_text='The author ID of the comment',
    )

    class Meta:
        ref_name = None
        fields = ('content', 'post', 'author')


class CommentBodySerializer(serializers.Serializer):
    content = serializers.CharField(
        required=True,
        help_text='The content of the comment',
    )

    class Meta:
        ref_name = None
        fields = ('content')
