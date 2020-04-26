from typing import List, Optional

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models.query import QuerySet
from django.http.request import QueryDict
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from common.querytools import filter_exists, get_one
from common.responses import (APPLY_200_UPDATED, APPLY_201_CREATED, APPLY_204_DELETED,
                              APPLY_400_PARAMETER_ERROR, APPLY_404_NOT_FOUND)
from post.models import Post, Tag
from post.serializers.post import (PostCreateBodySerializer, PostCreateSerializer,
                                   PostDetailSerializer, PostPatchBodySerializer,
                                   PostPatchSerializer, PostQuerySerializer, PostSerializer)


class PostAPI(viewsets.ViewSet):
    list_response = openapi.Response('**Success**', PostSerializer(many=True))
    retrieve_response = openapi.Response('**Success**', PostDetailSerializer)

    def _tag_filter(self, posts: 'QuerySet[Post]', params: QueryDict) -> 'QuerySet[Post]':
        if len(params.getlist('tags')) > 1:
            raise ParseError(detail='This type of tag parameters are not supported.')

        tags = params['tags'].split(',')
        for tag in tags:
            if tag.strip():
                posts = posts.filter(tags__title__icontains=tag.strip())

        return posts

    def _convert(self, tag_titles: Optional[List[str]]) -> Optional[List[int]]:
        if tag_titles is not None:
            tags = [Tag.objects.get_or_create(title=title.strip())[0]
                    for title in tag_titles if title.strip()]
            return [tag.id for tag in tags]
        return None

    @swagger_auto_schema(query_serializer=PostQuerySerializer,
                         responses={200: list_response,
                                    400: APPLY_400_PARAMETER_ERROR.as_md()})
    def list(self, request: Request) -> Response:
        """
        Get the list of posts.

        If the request has any vaild parameters in the query string,
        A response that includes a filtered category object by parameters
        will be returned.
        """
        params = request.GET
        posts = filter_exists(Post.objects.filter(is_active=True),
                              params.dict(),
                              date__gte='startDate',
                              date__lte='endDate',
                              time_of_day='timeOfDay',
                              location__icontains='location',
                              category__title__icontains='category',
                              ).order_by('id')

        if 'tags' in params:
            posts = self._tag_filter(posts, params=params)

        try:
            no = int(params.get('page', 1))
            page_size = min(int(params.get('pageSize', 20)), 50)
            if page_size <= 0:
                raise ParseError(detail='Page size should not be 0 or less.')
        except ValueError:
            raise ParseError(detail='Page or page size should be integer.')

        paginated_posts = Paginator(posts, page_size).get_page(no)
        serializer = PostSerializer(paginated_posts, many=True)

        return Response(serializer.data)

    @transaction.atomic
    @swagger_auto_schema(request_body=PostCreateBodySerializer,
                         responses={201: APPLY_201_CREATED.as_md(),
                                    400: APPLY_400_PARAMETER_ERROR.as_md()})
    def create(self, request: Request) -> Response:
        """
        Create a post.

        A category ID in request data must be required.
        """
        post_data = {**request.data}
        post_data['tags'] = self._convert(post_data.get('tags'))

        serializer = PostCreateSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Successfully created.'}, status=status.HTTP_201_CREATED)

        raise ValidationError(detail=serializer.errors)

    @swagger_auto_schema(responses={200: retrieve_response,
                                    400: APPLY_400_PARAMETER_ERROR.as_md(),
                                    404: APPLY_404_NOT_FOUND.as_md()})
    def retrieve(self, request: Request, post_id: int) -> Response:
        """
        Get a post object.

        A specific post ID must be required by uri resources.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    @transaction.atomic
    @swagger_auto_schema(request_body=PostPatchBodySerializer,
                         responses={200: APPLY_200_UPDATED.as_md(),
                                    400: APPLY_400_PARAMETER_ERROR.as_md(),
                                    404: APPLY_404_NOT_FOUND.as_md()})
    def partial_update(self, request: Request, post_id: int) -> Response:
        """
        Update data of the post.

        A specific post ID must be required by uri resources.
        """
        patch_data = {**request.data}

        if not patch_data:
            raise ParseError(detail='At least one field must be required to update the post.')
        elif 'id' in patch_data or 'pk' in patch_data:
            raise ParseError(detail='Post ID cannot be updated.')
        elif 'category' in patch_data:
            raise ParseError(detail='Category cannot be updated.')
        elif 'author' in patch_data:
            raise ParseError(detail='Author cannot be updated.')

        patch_data['tags'] = self._convert(patch_data.get('tags'))

        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostPatchSerializer(post, data=patch_data, partial=True)

        if serializer.is_valid():
            serializer.update(post, validated_data=patch_data)
            return Response({'detail': 'Successfully updated.'})

        raise ValidationError(detail=serializer.errors)

    @swagger_auto_schema(responses={204: APPLY_204_DELETED.as_md(),
                                    404: APPLY_404_NOT_FOUND.as_md()})
    def destroy(self, request: Request, post_id: int) -> Response:
        """
        Make the post disabled.

        A specific post ID must be required by uri resources.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
