from typing import Optional

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import CategorySerializer


class CategoryAPI(APIView):
    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        """
        Gets a category object or a list of categories.
        Basically, this function returns a response that include data of
        whole categories unless a specific category id is given
        by uri resources.
        """
        category_id = url_resources.get('category_id')

        if category_id:
            category = APIUtils.get('Category', id=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        else:
            categories = APIUtils.get_list_of('Category')
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Creates a category.
        """
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Request, category_id: int) -> Response:
        """
        Updates the category title.
        The specific category ID must be required by uri resources.
        """
        category = APIUtils.get('Category', id=category_id)
        serializer = CategorySerializer(category, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, category_id: int) -> Response:
        """
        Makes the category disabled.
        The specific category ID must be required by uri resources.
        """
        category = APIUtils.get('Category', id=category_id)
        serializer = CategorySerializer(category)
        serializer.update(category, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
