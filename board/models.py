from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Board(models.Model):
    title = models.CharField(max_length=30, db_index=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=75)
    meeting_capacity = models.IntegerField()
    meeting_date = models.DateTimeField()
    meeting_times_of_day = models.IntegerField()

    author = models.ForeignKey('member.Member', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comments = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    comment_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE)

    def __str__(self):
        return self.comments


class Tag(models.Model):
    title = models.CharField(max_length=30)

    board_tags = models.ManyToManyField(Board)

    def __str__(self):
        return self.title


class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    photo_info = models.IntegerField(null=True)

    def __str__(self):
        return self.photo_name
