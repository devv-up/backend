from typing import Optional

from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Category
from post.serializers import CategorySerializer


class CategoryAPI(APIView):
    def get_object(self, category_id: int) -> Category:
        """
        Returns a category object which is active.
        """
        try:
            return Category.objects.get(pk=category_id, is_active=True)
        except Exception:
            raise NotFound

    def category_detail(self, category_id: int) -> Response:
        """
        Gets a detailed category.
        """
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def category_list(self) -> Response:
        """
        Gets whole categories which are active.
        """
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        """
        Gets a category object or a list of categories.
        Basically, this function returns a response that include data of
        whole categories unless a specific category id is given
        by uri resources.
        """
        category_id = url_resources.get('category_id')

        if category_id:
            return self.category_detail(category_id)
        else:
            return self.category_list()

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
        category = self.get_object(category_id)
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
        category = self.get_object(category_id)
        serializer = CategorySerializer(category)
        serializer.update(category, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
