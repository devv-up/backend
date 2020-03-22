from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import CategorySerializer


class CategoryAPI(APIView):
    def get(self, request: Request, category_id: int = None) -> Response:
        """
        Get a category object or the list of categories.
        Basically, this function returns a response that includes data of
        whole categories unless a specific category ID is given
        by uri resources.
        """
        if category_id:
            category = APIUtils.get('Category', id=category_id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        else:
            categories = APIUtils.get_list_of('Category')
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
