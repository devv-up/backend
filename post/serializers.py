from rest_framework import serializers

from common.serializers import FilteredSerializer
from post.models import Category, Comment, Post, Tag
from user.models import User


class TempUserSerializer(serializers.ModelSerializer):
    """
    This class will be used until the UserSerializer from
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


class CommentSerializer(FilteredSerializer):
    createdDate = serializers.DateTimeField(source='created_date')
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        source='parent_comment',
        required=False)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'createdDate',
                  'parentComment', 'author', 'is_active')


class PostSerializer(FilteredSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        depth = 1
        fields = ('id', 'title', 'content', 'location', 'capacity',
                  'date', 'timeOfDay', 'createdDate', 'author',
                  'category', 'tags', 'comments')
        read_only_fields = ['comments']
