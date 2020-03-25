from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import CommentSerializer


class CommentAPI(APIView):
    def post(self, request: Request) -> Response:
        """
        Create a comment.
        A post ID in request data must be required.
        """
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Request, comment_id: int) -> Response:
        """
        Update data of the comment.
        A specific comment ID must be required by uri resources.
        """
        APIUtils.validate(request.data)

        comment = APIUtils.get('Comment', id=comment_id)
        serializer = CommentSerializer(comment, request.data, partial=True)

        if serializer.is_valid():
            serializer.update(comment, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, comment_id: int) -> Response:
        """
        Make the comment disabled.
        A specific comment ID must be required by uri resources.
        """
        comment = APIUtils.get('Comment', id=comment_id)
        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
