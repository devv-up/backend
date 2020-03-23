from typing import Any, Dict, List

from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.models import Tag
from post.serializers import PostListSerializer, PostSerializer


class PostAPI(APIView):
    def create_tags_with(self, titles: List[str]) -> List[Tag]:
        """
        Create tags before creating a post.
        If the same title tags exists,
        the tag objects will be returned.
        """
        tags: List[Tag] = list()
        for title in titles:
            if Tag.objects.filter(title=title).exists():
                tags.append(Tag.objects.get(title=title))
            else:
                tags.append(Tag.objects.create(title=title))
        return tags

    def get(self, request: Request, post_id: int = None) -> Response:
        """
        Get a post object or the list of posts.

        Basically, this function returns a response that includes data of
        whole posts unless a specific post ID is given
        by uri resources.

        If the request has any vaild parameters in the query string,
        A response that includes a filtered category object by parameters
        will be returned.
        """
        if post_id:
            post = APIUtils.get('Post', id=post_id)
            serializer = PostListSerializer(post)
            return Response(serializer.data)
        else:
            posts = APIUtils.get_list_of('Post', request)
            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data)

    @transaction.atomic
    def post(self, request: Request) -> Response:
        """
        Create a post.
        A category ID in request data must be required.
        """
        key_filter = ('tags', 'tagTitles')
        post_data: Dict[str, Any] = {k: v for k, v in request.data.items()
                                     if k not in key_filter}

        tag_titles = request.data.get('tagTitles')
        if tag_titles:
            tags = self.create_tags_with(tag_titles)
            post_data.update(tags=[tag.id for tag in tags])

        serializer = PostSerializer(data=post_data)
        if serializer.is_valid():
            if not request.data.get('category'):
                raise ParseError(detail='A category number must be required')

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    @transaction.atomic
    def patch(self, request: Request, post_id: int) -> Response:
        """
        Update data of the post.
        A specific post ID must be required by uri resources.
        """
        APIUtils.validate(request.data)

        key_filter = ('tags', 'tagTitles')
        patch_data: Dict[str, Any] = {k: v for k, v in request.data.items()
                                      if k not in key_filter}

        tag_titles = request.data.get('tagTitles')
        if tag_titles:
            tags = self.create_tags_with(tag_titles)
            patch_data.update(tags=[tag.id for tag in tags])

        post = APIUtils.get('Post', id=post_id)
        serializer = PostSerializer(post, patch_data, partial=True)

        if serializer.is_valid():
            serializer.update(post, patch_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, post_id: int) -> Response:
        """
        Make the post disabled.
        A specific post ID must be required by uri resources.
        """
        post = APIUtils.get('Post', id=post_id)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
