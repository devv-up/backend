from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from common.querytools import get_one
from common.responses import (APPLY_200_UPDATED, APPLY_201_CREATED, APPLY_204_DELETED,
                              APPLY_400_PARAMETER_ERROR, APPLY_404_NOT_FOUND)
from post.models import Comment
from post.serializers import (CommentCreateBodySerializer, CommentCreateSerializer,
                              CommentPatchBodySerializer, CommentSerializer)


class CommentAPI(viewsets.ViewSet):
    @swagger_auto_schema(request_body=CommentCreateBodySerializer,
                         responses={201: APPLY_201_CREATED.as_md(),
                                    400: APPLY_400_PARAMETER_ERROR.as_md()})
    def create(self, request: Request) -> Response:
        """
        Create a comment.

        A post ID in request data must be required.
        """
        comment_data = {**request.data}
        serializer = CommentCreateSerializer(data=comment_data)

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Successfully created.'}, status=status.HTTP_201_CREATED)

        raise ValidationError(detail=serializer.errors)

    @swagger_auto_schema(
        request_body=CommentPatchBodySerializer,
        responses={200: APPLY_200_UPDATED.as_md(),
                   400: APPLY_400_PARAMETER_ERROR.as_md(),
                   404: APPLY_404_NOT_FOUND.as_md()})
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
            return Response({'detail': 'Successfully updated.'})

        raise ValidationError(detail=serializer.errors)

    @swagger_auto_schema(
        responses={204: APPLY_204_DELETED.as_md(),
                   400: APPLY_400_PARAMETER_ERROR.as_md(),
                   404: APPLY_404_NOT_FOUND.as_md()})
    def destroy(self, request: Request, comment_id: int) -> Response:
        """
        Make the comment disabled.

        A specific comment ID must be required by uri resources.
        """
        comment = get_one(Comment, id=comment_id, is_active=True)
        serializer = CommentSerializer(comment)
        serializer.update(comment, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
