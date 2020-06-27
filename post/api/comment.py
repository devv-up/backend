from typing import List, Optional

from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.permissions import check_permission
from common.querytools import get_one
from post.models import Comment
from post.serializers import CommentCreateSerializer, CommentPutSerializer, CommentSerializer


class CommentAPI(viewsets.ViewSet):
    action: Optional[str] = None

    def get_permissions(self) -> List[BasePermission]:
        permission_classes = [AllowAny if self.action in ['list', 'retrieve'] else IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request: Request) -> Response:
        """
        Create a comment.

        A post ID in request data must be required.
        """
        comment_data = {**request.data}
        comment_data['author'] = request.user.id

        serializer = CommentCreateSerializer(data=comment_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Successfully created.'}, status=status.HTTP_201_CREATED)

        raise ValidationError(detail=serializer.errors)

    def update(self, request: Request, comment_id: int) -> Response:
        """
        Update data of the comment.

        A specific comment ID must be required by uri resources.
        """
        if request.data.get('content') is None:
            raise ParseError(detail='The content field must be required.')

        comment = get_one(Comment, id=comment_id, is_active=True)
        check_permission(request.user, comment)

        comment_data = {'content': request.data['content']}
        serializer = CommentPutSerializer(comment, data=comment_data, partial=True)

        if serializer.is_valid():
            serializer.update(comment, validated_data=request.data)
            return Response({'detail': 'Successfully updated.'})

        raise ValidationError(detail=serializer.errors)

    def destroy(self, request: Request, comment_id: int) -> Response:
        """
        Make the comment disabled.

        A specific comment ID must be required by uri resources.
        """
        comment = get_one(Comment, id=comment_id, is_active=True)
        check_permission(request.user, comment)

        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
