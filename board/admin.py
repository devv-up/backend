from django.contrib import admin  # noqa: 401

from board.models import Board, Category, Comment, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Board)
admin.site.register(Comment)
admin.site.register(Tag)
