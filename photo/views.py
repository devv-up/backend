from typing import Any

from rest_framework import status
# Create your views here.
from rest_framework.parsers import FileUploadParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from photo.serializer import PhotoSerializer


class FileUploadView(APIView):
    parser_class = (FileUploadParser)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:

        photo_serializer = PhotoSerializer(data=request.data)

        if photo_serializer.is_valid():
            photo_serializer.save()
            return Response(photo_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(photo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
