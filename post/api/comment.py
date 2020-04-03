from rest_framework import mixins, status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.querytools import get_one
from post.models import Comment
from post.serializers import CommentCreateSerializer, CommentSerializer


class CommentCreateAPI(mixins.CreateModelMixin, APIView):
    def post(self, request: Request) -> Response:
        """
        Create a comment.

        A post ID in request data must be required.
        """
        serializer = CommentCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)


class CommentAPI(mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 APIView):
    def put(self, request: Request, comment_id: int) -> Response:
        """
        Update data of the comment.

        A specific comment ID must be required by uri resources.
        """
        try:
            comment_data = {'content': request.data.get('content')}
        except Exception:
            raise ParseError(detail='The content field must be required.')

        comment = get_one(Comment, id=comment_id, is_active=True)
        serializer = CommentCreateSerializer(comment, comment_data, partial=True)

        if serializer.is_valid():
            serializer.update(comment, request.data)
            return Response(serializer.data)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, comment_id: int) -> Response:
        """
        Make the comment disabled.

        A specific comment ID must be required by uri resources.
        """
        comment = get_one(Comment, id=comment_id, is_active=True)
        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        deleted_comment = CommentSerializer(comment).data

        return Response(deleted_comment, status=status.HTTP_204_NO_CONTENT)
