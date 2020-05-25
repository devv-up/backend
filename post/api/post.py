from typing import List, Optional, Type, Union

from django.core.paginator import Paginator
from django.db import transaction
from django.db.models.query import QuerySet
from django.http.request import QueryDict
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from common.querytools import filter_exists, get_one
from post.models import Post, Tag
from post.serializers import (PostCreateSerializer, PostDetailSerializer, PostPatchSerializer,
                              PostSerializer)


class PostAPI(viewsets.ViewSet):
    def __init__(self) -> None:
        self.action = None
        super().__init__()

    def get_permissions(self) -> List[BasePermission]:
        permission_classes: List[Union[Type[AllowAny], Type[IsAuthenticated]]] = list()

        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
        except ValueError:
            raise ParseError(detail='Page or page size should be integer.')

        paginated_posts = Paginator(posts, page_size).get_page(no)
        serializer = PostSerializer(paginated_posts, many=True)

        return Response(serializer.data)

    @transaction.atomic
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

    def retrieve(self, request: Request, post_id: int = None) -> Response:
        """
        Get a post object.

        A specific post ID must be required by uri resources.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    @transaction.atomic
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

    def destroy(self, request: Request, post_id: int) -> Response:
        """
        Make the post disabled.

        A specific post ID must be required by uri resources.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
