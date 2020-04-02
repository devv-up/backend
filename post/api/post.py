from typing import Any, Dict, List

from django.core.paginator import Page, Paginator
from django.db import transaction
from rest_framework import mixins, status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from common.querytools import filter_exists, get_one
from post.models import Comment, Post, Tag
from post.serializers import CommentSerializer, PostCreateSerializer, PostSerializer


def create_tags_with(titles: List[str]) -> List[Tag]:
    """
    Create tags before creating a post.
    If the same title tags exists,
    the tag objects will be returned.
    """
    tags: List[Tag] = list()
    for title in titles:
        tags.append(Tag.objects.get_or_create(title=title)[0])
    return tags


class PostListCreateAPI(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        APIView):
    def get(self, request: Request) -> Response:
        """
        Get the list of posts.

        Basically, this function returns a response that includes data of
        whole posts unless a specific post ID is given
        by uri resources.

        If the request has any vaild parameters in the query string,
        A response that includes a filtered category object by parameters
        will be returned.
        """
        posts = filter_exists(Post, request.GET.dict(),
                              date__gte='startDate',
                              date__lte='endDate',
                              time_of_day='timeOfDay',
                              location__contains='location',
                              category__title='category',
                              ).order_by('id')

        if 'tags' in request.GET.dict():
            if len(request.GET.getlist('tags')) > 1:
                raise ParseError(detail='This type of tag parameters are not supported.')

            tags: List[str] = request.GET['tags'].split(',')
            for tag in tags:
                posts = posts.filter(tags__title=tag)

        posts.filter(is_active=True)
        serializer = PostSerializer(posts, many=True)

        if 'page' in request.GET.dict():
            no = int(request.GET['page'])
            per_page = request.GET['perPage'] if 'perPage' in request.GET.dict() else 20
            paginated_posts: Page = Paginator(posts, per_page).get_page(no)
            serializer = PostSerializer(paginated_posts, many=True)

        return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request) -> Response:
        """
        Create a post.

        A category ID in request data must be required.
        """
        post_data: Dict[str, Any] = {k: v for k, v in request.data.items()
                                     if k not in 'tags'}

        tag_titles = request.data.get('tags')
        if tag_titles:
            tags = create_tags_with(tag_titles)
            post_data.update(tags=[tag.id for tag in tags])

        serializer = PostCreateSerializer(data=post_data)
        if serializer.is_valid():
            if not request.data.get('category'):
                raise ParseError(detail='A category number must be required')

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)


class PostAPI(mixins.RetrieveModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              APIView):
    def get(self, request: Request, post_id: int = None) -> Response:
        """
        Get a post object.

        Basically, this function returns a response that includes data of
        whole posts unless a specific post ID is given
        by uri resources.

        If the request has any vaild parameters in the query string,
        A response that includes a filtered category object by parameters
        will be returned.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostSerializer(post)
        post_data = serializer.data

        comments_of_post = Comment.objects.filter(post=post_id)
        comments = CommentSerializer(comments_of_post, many=True)
        post_data.update(comments=comments.data)

        return Response(post_data)

    @transaction.atomic
    def patch(self, request: Request, post_id: int) -> Response:
        """
        Update data of the post.

        A specific post ID must be required by uri resources.
        """
        patch_list = (
            'title', 'content', 'location', 'capacity',
            'date', 'timeOfDay',
        )
        patch_data: Dict[str, Any] = {k: v for k, v in request.data.items()
                                      if k in patch_list}

        tag_titles = request.data.get('tags')
        if tag_titles:
            tags = create_tags_with(tag_titles)
            patch_data.update(tags=[tag.id for tag in tags])

        if not patch_data:
            raise ParseError(detail='At least one field must be required to update the post.')

        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostCreateSerializer(post, patch_data, partial=True)

        if serializer.is_valid():
            serializer.update(post, patch_data)
            return Response(serializer.data)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, post_id: int) -> Response:
        """
        Make the post disabled.

        A specific post ID must be required by uri resources.
        """
        post = get_one(Post, id=post_id, is_active=True)
        serializer = PostCreateSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
