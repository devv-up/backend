from typing import Type, TypeVar, Any, Dict, Union
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound
from django.db.models.query import QuerySet
T = TypeVar('T', bound=models.Model)


def get_one(model: Type[T], *args: Any, **kwargs: Any) -> T:
    try:
        return model.objects.get(*args, **kwargs)
    except ObjectDoesNotExist:
        raise NotFound


def filter(s: Union[Type[T], 'QuerySet[T]'],
           options: Dict[str, Any],
           **kwargs: str) -> 'QuerySet[T]':
    if isinstance(s, QuerySet):
        qs = s
    else:
        qs = s.objects.all()
    filters = {}
    for k, v in kwargs.items():
        if v in options:
            filters[k] = options[v]
    return qs.filter(**filters)
