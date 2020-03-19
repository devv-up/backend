from typing import Optional

from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from post.api.utils import APIUtils
from post.serializers import PostListSerializer, PostSerializer


class PostAPI(APIView):
    def get(self, request: Request, **url_resources: Optional[int]) -> Response:
        """
        Gets a post object or a list of posts.

        Basically, this function returns a response that include data of
        whole posts unless a specific post id is given
        by uri resources.

        If the request has any vaild parameters in the query string,
        A response object that includes a filtered category object
        by parameters will be returned.
        """
        post_id = url_resources.get('post_id')

        if post_id:
            post = APIUtils.get('Post', id=post_id)
            serializer = PostListSerializer(post)
            return Response(serializer.data)
        else:
            posts = APIUtils.get_list_of('Post', request)
            serializer = PostListSerializer(posts, many=True)
            return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Creates a post.
        A category number must be required.
        """
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            if not request.data.get('category'):
                raise ParseError(detail='A category number must be required')

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def patch(self, request: Request, post_id: int) -> Response:
        """
        Updates data of the post.
        The specific post ID must be required by uri resources.
        """
        APIUtils.validate(request.data)

        post = APIUtils.get('Post', id=post_id)
        serializer = PostSerializer(post, request.data, partial=True)

        if serializer.is_valid():
            serializer.update(post, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, post_id: int) -> Response:
        """
        Makes the post disabled.
        The specific post ID must be required by uri resources.
        """
        post = APIUtils.get('Post', id=post_id)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
