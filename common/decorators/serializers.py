from datetime import datetime
from typing import Any, Callable, cast, Type, Dict, Optional, TypeVar, Iterable, OrderedDict

from django.db import models
from rest_framework import serializers

T = TypeVar('T', bound=serializers.Field)
U = TypeVar('U', bound=serializers.Serializer)
V = TypeVar('V', bound=models.Model)


def filtered_serializer(super_class: type,
                        fields: Iterable[str],
                        meta: Optional[Dict[str, Any]] = None,
                        ) -> Callable[[type], Type[U]]:
    """

    Args:
        super_class: the target serializer class to be filtered
        fields: allowed fields ( only these fields will be added in a new serializer class )
        meta:

    Returns:
        wrapping function returning a generated class or itself
        Note that it regenerates a class if the given class is not a subclass of
        `rest_framework.serializers.Serializer`

    Examples:
        >>> @serializer(test_model, {'depth': 1})
        >>> class TestSerializer:
        >>>     # required and db field
        >>>     test_field = required(int, 'help text for test_field')
        >>>     # not required and not db field
        >>>     test_field2 = field(int, 'help text for test_field2', False)
        >>>
        >>> @filtered_serializer(TestSerializer, ['test_field'], {'depth': 2})
        >>> class TestSerializer:
        >>>     # required and db field
        >>>     test_field2 = required(int, 'help text for test_field')
        >>>     # not required and not db field
        >>>     test_field3 = field(int, 'help text for test_field2', False)

    """
    assert issubclass(super_class, serializers.Serializer)
    field_set = set(fields)

    def wrap(origin: type) -> Type[U]:
        _fields = set()
        cls = type(f'{origin.__module__}.{origin.__name__}',
                   tuple([super_class]),
                   {})
        super_meta_class = getattr(cls, 'Meta')
        meta_class = type(f'{origin.__module__}.{origin.__name__}.Meta',
                          tuple([super_meta_class]),
                          {})
        declared_fields = getattr(cls, '_declared_fields')
        new_declared_fields = OrderedDict()
        for key, value in declared_fields.items():
            if key in field_set:
                _fields.add(key)
                new_declared_fields[key] = value

        for key, value in origin.__dict__.items():
            if isinstance(value, _Item):
                new_declared_fields[key] = value.origin
                if value.db_field:
                    _fields.add(key)

        setattr(cls, '_declared_fields', new_declared_fields)

        setattr(meta_class, 'fields', tuple(_fields))
        if meta is not None:
            for key, value in meta.items():
                setattr(meta, key, value)
        setattr(cls, 'Meta', meta_class)

        return cast(Type[U], cls)

    return wrap


def serializer(model: Type[V],
               meta: Optional[Dict[str, Any]] = None,
               ) -> Callable[[type], Type[U]]:
    """
    Args:
        model: the target model to update
        meta: additional fields for Meta class

    Returns:
        wrapping function returning a generated class or itself
        Note that it regenerates a class if the given class is not a subclass of
        `rest_framework.serializers.Serializer`

    Examples:
        >>> @serializer(test_model, {'depth': 1})
        >>> class TestSerializer:
        >>>     # required and db field
        >>>     test_field = required(int, 'help text for test_field')
        >>>     # not required and not db field
        >>>     test_field2 = field(int, 'help text for test_field2', False)
    """

    def wrap(origin: type) -> Type[U]:
        meta_class: Any
        inherited = [origin]
        if not issubclass(origin, serializers.Serializer):
            inherited.append(serializers.Serializer)
        if not hasattr(origin, 'Meta'):
            meta_class = type(f'{origin.__module__}.{origin.__name__}.Meta', tuple(), {
                'model': model
            })
        else:
            meta_class = getattr(origin, 'Meta')
            meta_class.model = model

        cls = type(f'{origin.__module__}.{origin.__name__}',
                   tuple(inherited),
                   dict(Meta=meta_class))
        _fields = set()
        declared_fields = getattr(cls, '_declared_fields')
        for key, value in origin.__dict__.items():
            if isinstance(value, _Item):
                declared_fields[key] = value.origin
                if value.db_field:
                    _fields.add(key)

        meta_class.fields = tuple(_fields)
        if meta is not None:
            for key, value in meta.items():
                setattr(meta_class, key, value)
        meta_class.model = model

        return cast(Type[U], cls)

    return wrap


def model_serializer(model: Type[V],
                     meta: Optional[Dict[str, Any]] = None,
                     fields: Optional[Iterable[str]] = None,
                     ) -> Callable[[type], Type[U]]:
    """
    Args:
        model: the target model to update
        meta: additional fields for Meta class
        fields: allowed fields, if it is :data:`None`, all fields are allowed.

    Returns:
        wrapping function returning a generated class or itself
        Note that it regenerates a class if the given class is not a subclass of
        `rest_framework.serializers.Serializer`

    Examples:
        >>> @model_serializer(test_model, {'depth': 1}, ['test_inherited_field'])
        >>> class TestSerializer:
        >>>     # required and db field
        >>>     test_field = required(int, 'help text for test_field')
        >>>     # not required and not db field
        >>>     test_field2 = field(int, 'help text for test_field2', False)
    """
    filtered_fields = set(fields or [])

    def wrap(origin: type) -> Type[U]:
        meta_class: Any
        inherited = [origin]
        if not issubclass(origin, serializers.ModelSerializer):
            inherited.append(serializers.ModelSerializer)
        if not hasattr(origin, 'Meta'):
            meta_class = type(f'{origin.__module__}.{origin.__name__}.Meta', tuple(), {
                'model': model
            })
        else:
            meta_class = getattr(origin, 'Meta')
            meta_class.model = model

        cls = type(f'{origin.__module__}.{origin.__name__}',
                   tuple(inherited),
                   dict(Meta=meta_class))
        _fields = set()
        _referenced = set()
        declared_fields = getattr(cls, '_declared_fields')
        for key, value in origin.__dict__.items():
            if isinstance(value, _Item):
                declared_fields[key] = value.origin
                if value.db_field:
                    _fields.add(key)
                if value.source:
                    _referenced.add(value.source)

        for f in model._meta.get_fields():
            if f.name not in _referenced and (fields is None or f.name in filtered_fields):
                _fields.add(f.name)

        meta_class.fields = tuple(_fields)
        if meta is not None:
            for key, value in meta.items():
                setattr(meta_class, key, value)
        meta_class.model = model

        return cast(Type[U], cls)

    return wrap


class Date:
    pass


class DateTime:
    pass


class Method:
    pass


FIELD_DICT: Dict[type, type] = {
    int: serializers.IntegerField,
    str: serializers.CharField,
    Date: serializers.DateField,
    datetime: serializers.DateTimeField,
    DateTime: serializers.DateTimeField,
    Method: serializers.SerializerMethodField
}


class _Item:
    def __init__(self, _db_field: bool, _origin: type, **kwargs: Any) -> None:
        if not issubclass(_origin, serializers.Field):
            if issubclass(_origin, models.Model):
                kwargs['queryset'] = _origin.objects.all()
                _origin = serializers.PrimaryKeyRelatedField
            else:
                _origin = FIELD_DICT[_origin]
        self.db_field = _db_field
        self.origin = _origin(**kwargs)
        self.source = getattr(self.origin, 'source', '')


def field(value_type: type, help_text: str, _db_field: bool = True, **kwargs: Any) -> _Item:
    kwargs['help_text'] = help_text
    return _Item(_db_field, value_type, **kwargs)


def required(value_type: type, help_text: str, _db_field: bool = True, **kwargs: Any) -> _Item:
    kwargs['required'] = True
    return field(value_type, help_text, _db_field, **kwargs)
