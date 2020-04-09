from typing import Any, Dict, List, Literal, Optional, Tuple, Type

from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import Info
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class _SchemaView:
    schema: Literal[None]
    public: bool
    generator_class = Type[OpenAPISchemaGenerator]
    authentication_classes = Tuple[str]
    permission_classes = Tuple[str]
    renderer_classes = Tuple[Any, ...]  # TODO

    def get(
        # XXX format is unused?
        self, request: Request, version: str = ...,
        format: Optional[Any] = ...) -> Response: ...

    @classmethod
    def apply_cache(cls, view: Any, cache_timeout: int,
                    cache_kwargs: Dict[str, Any]) -> APIView: ...

    @classmethod
    def as_cached_view(cls, cache_timeout: int = ...,
                       cache_kwargs: Dict[str, Any] = ..., **initkwargs: Any) -> APIView: ...

    @classmethod
    def without_ui(cls, cache_timeout: int = ...,
                   cache_kwargs: Dict[str, Any] = ...) -> APIView: ...

    @classmethod
    def with_ui(cls, renderer: str = ..., cache_timeout: int = ...,
                cache_kwargs: Dict[str, Any] = ...) -> APIView: ...


def get_schema_view(
    info: Optional[Info] = ...,
    url: Optional[str] = ...,
    patterns: Optional[Any] = ...,  # TODO
    urlconf: Optional[Any] = ...,  # TODO
    public: bool = ...,
    validators: Optional[List[str]] = ...,
    generator_class: Optional[Type[OpenAPISchemaGenerator]] = ...,
    authentication_classes: Optional[Tuple[str]] = ...,
    permission_classes: Optional[Tuple[str]] = ...,
) -> _SchemaView: ...
