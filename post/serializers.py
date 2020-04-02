from rest_framework import serializers

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


class PostCreateSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'location', 'capacity',
                  'date', 'timeOfDay', 'author', 'category', 'tags')


class PostSerializer(serializers.ModelSerializer):
    timeOfDay = serializers.IntegerField(source='time_of_day')
    createdDate = serializers.DateTimeField(source='created_date')

    class Meta:
        model = Post
        depth = 1
        fields = ('id', 'title', 'content', 'location', 'capacity',
                  'date', 'timeOfDay', 'createdDate', 'author', 'category', 'tags')


class CommentCreateSerializer(serializers.ModelSerializer):
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), source='parent_comment', required=False)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'parentComment', 'author')


class CommentSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(source='created_date')
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(), source='parent_comment')

    class Meta:
        model = Comment
        depth = 1
        fields = ('id', 'content', 'createdDate', 'parentComment', 'author', 'is_active')
