from typing import Any

from rest_framework import status  # type: ignore
from rest_framework.exceptions import NotFound, ParseError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from post.models import Category
from post.serializers import CategorySerializer


class CategoryAPI(APIView):
    def get_object(self, category_id: int) -> Category:
        """
        Get a category object.
        """
        try:
            return Category.objects.get(pk=category_id, is_active=True)
        except Exception:
            raise NotFound

    def category_detail(self, category_id: int) -> Response:
        """
        Get a category.
        """
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def category_list(self) -> Response:
        """
        Get a list of whole categories which are active.
        """
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

    def get(self, request: Any, **parameter: Any) -> Response:
        category_id = parameter.get('category_id')

        if category_id:
            return self.category_detail(category_id)
        else:
            return self.category_list()

    def post(self, request: Any) -> Response:
        """
        Create a category.
        """
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Any, category_id: int) -> Response:
        """
        Update the category title.
        """
        category = self.get_object(category_id)
        serializer = CategorySerializer(category, request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Any, category_id: int) -> Response:
        """
        Set a category disabled.
        """
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)
        serializer.update(category, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
