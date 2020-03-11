from django.http import QueryDict
from rest_framework.exceptions import AuthenticationFailed  # type: ignore


class APIUtils:
    vulnerable_fields = (
        'id',
        'author',
    )

    @classmethod
    def validate(cls, data: QueryDict) -> bool:
        vulnerable = [key for key in data if key in cls.vulnerable_fields]
        if vulnerable:
            raise AuthenticationFailed

        return True
