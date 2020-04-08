from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response

from common.querytools import get_one
from post.models import Comment
from post.serializers import CommentSerializer


class CommentAPI(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        """
        Create a comment.

        A post ID in request data must be required.
        """
        allowed_fields = [
            'id', 'content', 'post', 'parentComment', 'author'
        ]
        serializer = CommentSerializer(data=request.data, fields=allowed_fields)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ParseError(detail=serializer.errors)

    def update(self, request: Request, comment_id: int) -> Response:
        """
        Update data of the comment.

        A specific comment ID must be required by uri resources.
        """
        if request.data.get('content') is None:
            raise ParseError(detail='The content field must be required.')

        comment = get_one(Comment, id=comment_id, is_active=True)
        comment_data = {'content': request.data['content']}
        serializer = CommentSerializer(comment, data=comment_data, partial=True)

        if serializer.is_valid():
            serializer.update(comment, validated_data=request.data)
            return Response(serializer.data)
        raise ParseError(detail=serializer.errors)

    def destroy(self, request: Request, comment_id: int) -> Response:
        """
        Make the comment disabled.

        A specific comment ID must be required by uri resources.
        """
        comment = get_one(Comment, id=comment_id, is_active=True)
        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        deleted_comment = CommentSerializer(comment).data
        return Response(deleted_comment, status=status.HTTP_204_NO_CONTENT)
