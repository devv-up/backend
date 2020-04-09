from collections import OrderedDict
from types import ModuleType
from typing import Any, ClassVar, Dict, List, Literal, Optional, Tuple, Type, Union

from rest_framework.serializers import Serializer

# Alias for compatibility import
collections_abc: ModuleType

TYPE_OBJECT: Literal["object"] = "object"
TYPE_STRING: Literal["string"] = "string"
TYPE_NUMBER: Literal["number"] = "number"
TYPE_INTEGER: Literal["integer"] = "integer"
TYPE_BOOLEAN: Literal["boolean"] = "boolean"
TYPE_ARRAY: Literal["array"] = "array"
TYPE_FILE: Literal["file"] = "file"
_TYPE_any = Literal["object", "string", "number", "integer", "boolean", "array", "file"]

FORMAT_DATE: Literal["date"]
FORMAT_DATETIME: Literal["date-time"]
FORMAT_PASSWORD: Literal["password"]
FORMAT_BINARY: Literal["binary"]
FORMAT_BASE64: Literal["bytes"]
FORMAT_FLOAT: Literal["float"]
FORMAT_DOUBLE: Literal["double"]
FORMAT_INT32: Literal["int32"]
FORMAT_INT64: Literal["int64"]

FORMAT_EMAIL: Literal["email"]
FORMAT_IPV4: Literal["ipv4"]
FORMAT_IPV6: Literal["ipv6"]
FORMAT_URI: Literal["uri"]

FORMAT_UUID: Literal["uuid"]
FORMAT_SLUG: Literal["slug"]
FORMAT_DECIMAL: Literal["decimal"]
_FORMAT_any = Literal[
    "date",
    "date-time",
    "password",
    "binary",
    "bytes",
    "float",
    "double",
    "int32",
    "int64",
    "email",
    "ipv4",
    "ipv6",
    "uri",
    "uuid",
    "slug",
    "decimal",
]

IN_BODY: Literal["body"]
IN_PATH: Literal["path"]
IN_QUERY: Literal["query"]
IN_FORM: Literal["formData"]
IN_HEADER: Literal["header"]
_IN_any = Literal["body", "path", "query", "formData", "header"]

SCHEMA_DEFINITIONS: Literal["definitions"]

# Enum can only can only be applied to primitives and they must have uniform types
_EnumType = Union[List[str], List[int], List[bool], List[float]]


class SwaggerDict(OrderedDict[str, Any]):
    _extras__: Dict[str, Any] = ...
    def __getattr__(self, item: str) -> Any: ...
    def _insert_extras__(self) -> None: ...
    def as_odict(self) -> Any: ...


class Contact(SwaggerDict):
    name: Optional[str] = ...
    url: Optional[str] = ...
    email: Optional[str] = ...

    def __init__(
        self, name: Optional[str] = ..., url: Optional[str] = ...,
        email: Optional[str] = ..., **extra: Any
    ): ...


class License(SwaggerDict):
    name: str = ...
    url: Optional[str] = ...
    def __init__(self, name: str, url: Optional[str] = ..., **extra: Any): ...


class Info(SwaggerDict):
    title: str = ...
    _default_version: str = ...
    description: Optional[str] = ...
    terms_of_service: Optional[str] = ...
    contact: Optional[Contact] = ...
    license: Optional[License] = ...

    def __init__(
        self,
        title: str,
        default_version: str,
        description: Optional[str] = ...,
        terms_of_service: Optional[str] = ...,
        contact: Optional[Contact] = ...,
        license: Optional[License] = ...,
        **extra: Any
    ): ...


class Items(SwaggerDict):
    type: _TYPE_any = ...
    format: Optional[_FORMAT_any] = ...
    enum: Optional[_EnumType] = ...
    pattern: Optional[str] = ...
    items_: Optional['Items'] = ...

    def __init__(
        self,
        type: _TYPE_any = ...,  # Type is required
        format: Optional[_FORMAT_any] = ...,
        enum: Optional[_EnumType] = ...,
        pattern: Optional[str] = ...,
        items: Optional['Items'] = ...,
        **extra: Any
    ): ...


class Parameter(SwaggerDict):
    name: str = ...
    in_: _IN_any = ...
    description: Optional[str] = ...
    required: Optional[bool] = ...
    schema: Optional['_SchemaOrRef'] = ...
    type: Optional[_TYPE_any] = ...
    format: Optional[_FORMAT_any] = ...
    enum: Optional[_EnumType] = ...
    pattern: Optional[str] = ...
    items_: Optional[Items] = ...
    default: Optional[Any] = ...

    def __init__(
        self,
        name: str,
        in_: _IN_any,
        description: Optional[str] = ...,
        required: Optional[bool] = ...,
        schema: Optional['_SchemaOrRef'] = ...,
        type: Optional[_TYPE_any] = ...,
        format: Optional[_FORMAT_any] = ...,
        enum: Optional[_EnumType] = ...,
        pattern: Optional[str] = ...,
        items: Optional[Items] = ...,
        default: Optional[Any] = ...,
        **extra: Any
    ): ...


class Schema(SwaggerDict):
    OR_REF: ClassVar[Tuple[Type['Schema'], Type['SchemaRef']]] = ...

    title: Optional[str] = ...
    description: Optional[str] = ...
    type: Optional[_TYPE_any] = ...
    format: Optional[_FORMAT_any] = ...
    enum: Optional[_EnumType] = ...
    pattern: Optional[str] = ...
    properties: Optional[Any] = ...
    additional_properties: Optional[Any] = ...
    required: Optional[Any] = ...
    items_: Optional[Any] = ...
    default: Optional[Any] = ...
    read_only: Optional[bool] = ...

    def __init__(
        self,
        title: Optional[str] = ...,
        description: Optional[str] = ...,
        type: Optional[_TYPE_any] = ...,
        format: Optional[_FORMAT_any] = ...,
        enum: Optional[_EnumType] = ...,
        pattern: Optional[str] = ...,
        properties: Optional[Any] = ...,
        additional_properties: Optional[Any] = ...,
        required: Optional[List[str]] = ...,
        items: Optional[Any] = ...,
        default: Optional[Any] = ...,
        read_only: Optional[bool] = ...,
        **extra: Any
    ): ...


class _Ref(SwaggerDict):
    ref_name_re: Any = ...
    ref: Any = ...
    def __init__(self, resolver: Any, name: Any, scope: Any,
                 expected_type: Any, ignore_unresolved: bool = ...): ...

    def resolve(self, resolver: Any) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...


class SchemaRef(_Ref):
    def __init__(self, resolver: Any, schema_name: Any, ignore_unresolved: bool = ...): ...


_SerializerOrClass = Union[Serializer, Type[Serializer]]
_SchemaOrRef = Union[Schema, SchemaRef]


class Response(SwaggerDict):
    description: str = ...
    schema: Optional[Union[_SchemaOrRef, _SerializerOrClass]] = ...
    examples: Optional[Dict[str, Any]] = ...

    def __init__(
        self,
        description: str,
        schema: Optional[Union[_SchemaOrRef, _SerializerOrClass]] = ...,
        examples: Optional[Dict[str, Any]] = ...,
        **extra: Any
    ): ...
