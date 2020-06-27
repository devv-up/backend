from rest_framework import serializers

from post.models import Comment
from user.serializers import UserDetailsSerializer


class CommentSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(source='created_date')
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.filter(is_active=True),
        source='parent_comment',
        required=False
    )
    author = UserDetailsSerializer(read_only=True)

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
