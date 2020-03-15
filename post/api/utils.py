from typing import Any, Dict

from rest_framework.exceptions import AuthenticationFailed


class APIUtils:
    vulnerable_fields = (
        'id',
        'author',
        'parent_comment',
    )

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        vulnerable = [key for key in data if key in cls.vulnerable_fields]
        if vulnerable:
            raise AuthenticationFailed

        return True
