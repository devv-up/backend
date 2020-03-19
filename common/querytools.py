from typing import Any, Dict, Type, TypeVar, Union

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
from rest_framework.exceptions import NotFound

T = TypeVar('T', bound=models.Model)


def get_one(model: Type[T], *args: Any, **kwargs: Any) -> T:
    """
        Example:
        >>> get_one(Category, title="test")
    """
    try:
        return model.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        raise NotFound


def filter(s: Union[Type[T], 'QuerySet[T]'],
           options: Dict[str, Any],
           **kwargs: str) -> 'QuerySet[T]':
    """
        Example:
        >>> filter(Post, request.GET, date__gte='startDate', date__lte='endDate', ....)
    """
    if isinstance(s, QuerySet):
        qs = s
    else:
        qs = s.objects.all()
    filters = {}
    for k, v in kwargs.items():
        if v in options:
            filters[k] = options[v]
    return qs.filter(**filters)
