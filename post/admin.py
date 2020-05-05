from django.contrib import admin

from post.models import Category, Comment, Like, Post, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
