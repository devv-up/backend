from typing import Any, Optional

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get_option_filtered_queryset(self, request: Request) -> 'QuerySet[Post]':
        queryset: 'QuerySet[Post]' = Post.objects.all()

        if 'category' in request.GET:
            category_no = request.GET['category']
            queryset = queryset.filter(category=category_no)

        if 'tags' in request.GET:
            tags = request.GET['tags']
            for tag in tags:
                queryset = queryset.filter(tags=tag)

        if 'startDate' in request.GET:
            start_date = request.GET['startDate']
            queryset = queryset.filter(date__gte=start_date)

        if 'endDate' in request.GET:
            end_date = request.GET['endDate']
            queryset = queryset.filter(date__lte=end_date)

        if 'timeOfDay' in request.GET:
            time_of_day = request.GET['timeOfDay']
            queryset = queryset.filter(time_of_day=time_of_day)

        if 'location' in request.GET:
            location = request.GET['location']
            queryset = queryset.filter(location__contains=location)

        return queryset

    def post_detail(self, post_id: int) -> Response:
        """
        Get a post.
        """
        post = self.get_object(post_id)
        serializer = PostListSerializer(post)

        return Response(serializer.data)

    def post_list(self, request: Request) -> Response:
        """
        Get a list of whole posts which are active.
        """
        queryset = self.get_option_filtered_queryset(request)

        posts = queryset.filter(is_active=True)
        serializer = PostListSerializer(posts, many=True)

        return Response(serializer.data)

    def get(self, request: Request, **parameter: Optional[Any]) -> Response:
        post_id = parameter.get('post_id')

        if post_id:
            return self.post_detail(post_id)
        else:
            return self.post_list(request)

    def post(self, request: Request) -> Response:
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

    def put(self, request: Request, post_id: int) -> Response:
        """
        Update the post's data.
        """
        APIUtils.validate(request.data)

        post = self.get_object(post_id)
        serializer = PostSerializer(post, request.data, partial=True)

        if serializer.is_valid():
            serializer.update(post, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        raise ParseError(detail=serializer.errors)

    def delete(self, request: Request, post_id: int) -> Response:
        """
        Set a post disabled.
        """
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
