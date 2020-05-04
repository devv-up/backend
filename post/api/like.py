from django.db import transaction
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, ParseError, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from common.responses import (APPLY_201_CREATED, APPLY_204_DELETED, APPLY_400_PARAMETER_ERROR,
                              APPLY_404_NOT_FOUND)
from post.models import Like
from post.serializers.like import LikeCreateSerializer


class LikeAPI(viewsets.ViewSet):

    @transaction.atomic
    @swagger_auto_schema(query_serializer=LikeCreateSerializer,
                         responses={200: APPLY_201_CREATED.as_md(),
                                    400: APPLY_400_PARAMETER_ERROR.as_md()})
    def create(self, request: Request) -> Response:
        like_data = {**request.data}
        serializer = LikeCreateSerializer(data=like_data)

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(data={'detail': 'Successfully created.'},
                                status=status.HTTP_201_CREATED)
            except IntegrityError:
                raise ValidationError(detail='Only one like for a post is allowed per user')

        raise ValidationError(detail=serializer.errors)

    @swagger_auto_schema(responses={204: APPLY_204_DELETED.as_md(),
                                    400: APPLY_400_PARAMETER_ERROR.as_md(),
                                    404: APPLY_404_NOT_FOUND.as_md()})
    def destroy(self, request: Request) -> Response:
        """
        Make the comment disabled.

        A specific comment ID must be required by uri resources.
        """
        try:
            if not isinstance(request.data['user'], int):
                raise ParseError(detail='User ID must be integer.')
            elif not isinstance(request.data['post'], int):
                raise ParseError(detail='Post ID must be integer.')
        except KeyError:
            raise ParseError(detail='User ID or Post ID is required.')

        user, post = request.data['user'], request.data['post']
        like = Like.objects.filter(user=user, post=post)

        if like.exists():
            like.delete()
        else:
            raise NotFound(detail='Related post or user does not exist.')

        return Response(status=status.HTTP_204_NO_CONTENT)
