from django.db import models  # noqa: F401


# Create your models here.
class Category(models.Model):
    """
    Category model which defines purposes of boards.
    ex) Project, Meet-up, etc.
    """

    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Board(models.Model):
    """
    Board model which has simple information.
    """

    title = models.CharField(max_length=30, db_index=True)
    content = models.TextField()
    meeting_location = models.CharField(max_length=75)
    meeting_capacity = models.IntegerField()
    meeting_date = models.DateTimeField()
    meeting_times_of_day = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comment model which has the depth up to 2 levels
    by possessing another comment's id.
    """
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    board = models.ForeignKey('Board', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Tag(models.Model):
    """
    Tag model which defines properties of boards.
    ex) Frontend, JavaScript, React, Backend, Node.js, Python, Spring, etc.
    """
    title = models.CharField(max_length=30)

    board_tags = models.ManyToManyField('Board')

    def __str__(self):
        return self.title
