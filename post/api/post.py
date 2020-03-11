from typing import Any

from rest_framework import status  # type: ignore
from rest_framework.exceptions import NotFound, ParseError  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore

from post.api.utils import APIUtils
from post.models import Post
from post.serializers import PostListSerializer, PostSerializer


class PostAPI(APIView):
    def get_object(self, category_id: int) -> Post:
        """
        Get a post object.
        """
        try:
            return Post.objects.get(pk=category_id, is_active=True)
        except Exception:
            raise NotFound

    def post_detail(self, post_id: int) -> Response:
        """
        Get a post.
        """
        post = self.get_object(post_id)
        serializer = PostListSerializer(post)

        return Response(serializer.data)

    def post_list(self) -> Response:
        """
        Get a list of whole posts which are active.
        """
        posts = Post.objects.filter(is_active=True)
        serializer = PostListSerializer(posts, many=True)

        return Response(serializer.data)

    def get(self, request: Any, **parameter: Any) -> Response:
        post_id = parameter.get('post_id')

        if post_id:
            return self.post_detail(post_id)
        else:
            return self.post_list()

    def post(self, request: Any) -> Response:
        """
        Create a post.
        """
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            if not request.data.get('category'):
                raise ParseError(detail='Category number is a required field')

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def put(self, request: Any, post_id: int) -> Response:
        """
        Update the post's data.
        """
        APIUtils.validate(request.data)

        post = self.get_object(post_id)
        serializer = PostSerializer(post, request.data, partial=True)

        if serializer.is_valid():
            serializer.update(post, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return ParseError(detail=serializer.errors)

    def delete(self, request: Any, post_id: int) -> Response:
        """
        Set a post disabled.
        """
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
