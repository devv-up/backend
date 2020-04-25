from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from post.models import Category
from post.serializers import CategorySerializer


class CategoryAPI(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        """
        Get the list of categories.
        """
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
