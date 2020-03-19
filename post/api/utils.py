from typing import Any, Dict, List

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from rest_framework.exceptions import (AuthenticationFailed, NotFound,
                                       ParseError)
from rest_framework.request import Request

from post.models import Category, Comment, Post, Tag


class APIUtils:
    vulnerable_fields = (
        'id',
        'author',
        'category',
        'post',
        'parent_comment',
    )

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        vulnerable = [key for key in data if key in cls.vulnerable_fields]
        if vulnerable:
            raise AuthenticationFailed

        return True

    @staticmethod
    def filter_by(request: Request) -> 'QuerySet[Post]':
        """
        Returns filtered post queryset by given filtering options.
        """
        options = request.GET
        queryset: 'QuerySet[Post]' = Post.objects.all()

        filters = dict(
            date__gte=options.get('startDate'),
            date__lte=options.get('endDate'),
            category=options.get('category'),
            time_of_day=options.get('timeOfDay'),
            location__contains=options.get('location'),
        )
        queryset = queryset.filter(**{k: v for k, v in filters.items() if v is not None})

        if 'tags' in options:
            if len(options.getlist('tags')) > 1:
                raise ParseError(detail='This type of tag parameters are not supported.')
            else:
                tags: List[str] = options['tags'].split(',')
            for tag in tags:
                queryset = queryset.filter(tags=tag)

        return queryset

    @staticmethod
    def get(obj: str, id: int) -> Any:
        """
        Returns an object which is active.
        """
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

    @classmethod
    def get_list_of(cls, obj: str, *request: Request) -> 'QuerySet[Any]':
        """
        Gets list of objects which are active.
        """
        if obj == 'Category':
            return Category.objects.filter(is_active=True)
        elif obj == 'Comment':
            return Comment.objects.filter(is_active=True)
        elif obj == 'Post':
            post = cls.filter_by(request[0])
            return post.filter(is_active=True)
        elif obj == 'Tag':
            return Tag.objects.all()

        raise NotFound
