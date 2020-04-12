from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from django.http.response import HttpResponseBase
from drf_yasg.inspectors.base import FieldInspector, FilterInspector, PaginatorInspector
from drf_yasg.inspectors.view import SwaggerAutoSchema
from drf_yasg.openapi import Parameter, Response, Schema, SchemaRef
from rest_framework.serializers import Serializer


class no_body:
    ...


class unset:
    ...


_T = TypeVar("_T")
_VIEW = TypeVar("_VIEW", bound=Callable[..., HttpResponseBase])
_SerializerOrClass = Union[Serializer, Type[Serializer]]
_SchemaOrRef = Union[Schema, SchemaRef]


def swagger_auto_schema(
    method: Optional[str] = ...,
    methods: Optional[List[str]] = ...,
    auto_schema: Optional[Type[SwaggerAutoSchema]] = ...,
    request_body: Optional[Union[_SchemaOrRef, _SerializerOrClass]] = ...,
    query_serializer: Optional[_SerializerOrClass] = ...,
    manual_parameters: Optional[List[Parameter]] = ...,
    operation_id: Optional[str] = ...,
    operation_description: Optional[str] = ...,
    operation_summary: Optional[str] = ...,
    # TODO would prefer to have a more precise type for 'dict'
    security: Optional[List[Dict[str, Any]]] = ...,
    deprecated: Optional[bool] = ...,
    responses: Optional[
        Dict[Union[int, str], Union[_SchemaOrRef, Response, _SerializerOrClass, str, None]]
    ] = ...,
    field_inspectors: Optional[List[Type[FieldInspector]]] = ...,
    filter_inspectors: Optional[List[Type[FilterInspector]]] = ...,
    paginator_inspectors: Optional[List[Type[PaginatorInspector]]] = ...,
    tags: Optional[List[str]] = ...,
    **extra_overrides: Any
) -> Callable[[_VIEW], _VIEW]: ...


def swagger_serializer_method(serializer_or_field: Any) -> Callable[[_VIEW], _VIEW]: ...
