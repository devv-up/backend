from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound

from post.models import Category, Comment, Post, Tag


class APIUtils:

    @staticmethod
    def get(obj: str, id: int) -> Any:

        try:
            if obj == 'Category':
                return Category.objects.get(pk=id, is_active=True)
            elif obj == 'Comment':
                return Comment.objects.get(pk=id, is_active=True)
            elif obj == 'Post':
                return Post.objects.get(pk=id, is_active=True)
            elif obj == 'Tag':
                return Tag.objects.get(pk=id)

        except ObjectDoesNotExist:
            raise NotFound

        return None
