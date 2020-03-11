from rest_framework import serializers  # type: ignore

from post.models import Category, Comment, Post, Tag
from user.models import User


class TempUserSerializer(serializers.ModelSerializer):
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


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'location', 'capacity',
                  'date', 'time_of_day', 'author', 'category', 'tags')


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        depth = 1
        fields = ('id', 'title', 'content', 'location', 'capacity',
                  'date', 'time_of_day', 'created_date', 'author', 'category', 'tags')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'parent_comment', 'author')


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        depth = 1
        fields = ('id', 'content', 'created_date', 'post', 'parent_comment', 'author')
