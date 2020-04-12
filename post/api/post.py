from typing import List

from django.core.paginator import Page, Paginator
from django.db import transaction
from django.db.models.query import QuerySet
from django.http.request import QueryDict
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from common.querytools import filter_exists, get_one
from post.models import Post, Tag
from post.serializers import (PostCreateSerializer, PostDetailSerializer, PostPatchSerializer,
                              PostSerializer)


class PostAPI(viewsets.ViewSet):
    def __create_tags_with(self, titles: List[str]) -> List[Tag]:
        """
        Create tags before creating a post.
        If the same title tags exists,
        the tag objects will be returned.
        """
        tags: List[Tag] = list()
        for title in titles:
            tags.append(Tag.objects.get_or_create(title=title)[0])
        return tags

    def __tag_filter(self, posts: 'QuerySet[Post]', params: QueryDict) -> 'QuerySet[Post]':
        if len(params.getlist('tags')) > 1:
            raise ParseError(detail='This type of tag parameters are not supported.')

        tags: List[str] = params['tags'].split(',')
        for tag in tags:
            posts = posts.filter(tags__title=tag)

        return posts

    def list(self, request: Request) -> Response:
        """
        Get the list of posts.

        If the request has any vaild parameters in the query string,
        A response that includes a filtered category object by parameters
        will be returned.
        """
        params = request.GET
        posts = filter_exists(Post, params.dict(),
                              date__gte='startDate',
                              date__lte='endDate',
                              time_of_day='timeOfDay',
                              location__contains='location',
                              category__title='category',
                              ).order_by('id')

        if 'tags' in params:
            posts = self.__tag_filter(posts, params=params)

        posts = posts.filter(is_active=True)
        serializer = PostSerializer(posts, many=True)

        if 'page' in params:
            try:
                no = int(params['page'])
                page_size = params.get('pageSize', 20)
                page_size = 50 if int(page_size) > 50 else page_size
            except ValueError:
                raise ParseError(detail='Page or page size should be integer.')

            paginated_posts: Page = Paginator(posts, page_size).get_page(no)
            serializer = PostSerializer(paginated_posts, many=True)

        else:
            raise ValidationError(detail='Page parameter must be required.')

        return Response(serializer.data)

    @transaction.atomic
    def create(self, request: Request) -> Response:
        """
        Create a post.

        A category ID in request data must be required.
        """
        post_data = {**request.data}
        tag_titles = request.data.get('tags')
        if tag_titles is not None:
            tags = self.__create_tags_with(tag_titles)
            post_data.update(tags=[tag.id for tag in tags])

        serializer = PostCreateSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

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
        if not request.data:
            raise ParseError(detail='At least one field must be required to update the post.')
        elif request.data.get('id') or request.data.get('pk'):
            raise ParseError(detail='Post ID cannot be updated.')
        elif request.data.get('category'):
            raise ParseError(detail='Category cannot be updated.')

        patch_data = {**request.data}

        tag_titles = request.data.get('tags')
        if tag_titles is not None:
            tags = self.__create_tags_with(tag_titles)
            patch_data.update(tags=[tag.id for tag in tags])

        post = get_one(Post, id=post_id, is_active=True)

        serializer = PostPatchSerializer(
            post, data=patch_data, partial=True)

        if serializer.is_valid():
            serializer.update(post, validated_data=patch_data)
            return Response(serializer.data)

        raise ParseError(detail=serializer.errors)

    def destroy(self, request: Request, post_id: int) -> Response:
        """
        Make the post disabled.

        A specific post ID must be required by uri resources.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
