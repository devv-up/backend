from typing import Optional

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User


class UserAPI(APIView):
    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        user = User.objects.get_by_natural_key()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request: Request, post_id: int) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, post_id: int) -> Response:
        return Response(status=status.HTTP_204_NO_CONTENT)
