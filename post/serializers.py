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


class CommentSerializer(serializers.ModelSerializer):
    createdDate = serializers.DateTimeField(source='created_date')
    parentComment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        source='parent_comment',
        required=False)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'post', 'createdDate',
                  'parentComment', 'author', 'is_active')


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


class PostSerializer(serializers.ModelSerializer):
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
