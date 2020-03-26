from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Category
from post.serializers import CategorySerializer


class CategoryAPI(APIView):
    def get(self, request: Request) -> Response:
        """
        Get the list of categories.
        """
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
