from django.contrib import admin

from board.models import Board, Category, Comment, Photo, Tag

admin.site.register(Category)
admin.site.register(Board)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Photo)
