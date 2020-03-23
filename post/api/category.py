from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import CategorySerializer


class CategoryAPI(APIView):
    def get(self, request: Request) -> Response:
        """
        Get the list of categories.
        """
        categories = APIUtils.get_list_of('Category')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
