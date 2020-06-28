from django.db import models

from user.models import User

# Create your models here.


class Modifiable(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Category(models.Model):
    """
    A category model which defines purposes of posts.
    ex) Project, Meet-up, etc.
    """
    title = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'Category(title="{self.title}")'


class Post(Modifiable):
    """
    A post model which has simple information.
    meeting_time_of_day have integer value
    >>> 0=morning, 1=afternoon, 2=evening
    """
    title = models.CharField(max_length=50)
    content = models.TextField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    date = models.DateField()
    time_of_day = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self) -> str:
        return f'Post(id={self.id}, title="{self.title}")'


class Comment(Modifiable):
    """
    A Comment model which has the depth up to 2 levels
    by possessing another comment's id.
    """
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.PROTECT, null=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'Comment(id={self.id})'


class Tag(models.Model):
    """
    A Tag model which defines properties of posts.
    ex) Frontend, JavaScript, React, Backend, Node.js, Python, Spring, etc.
    """
    title = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f'Tag(title="{self.title}")'
