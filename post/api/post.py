from typing import Optional

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
        Returns a post object which is active.
        """
        try:
            return Post.objects.get(pk=category_id, is_active=True)
        except Exception:
            raise NotFound

    def get_option_filtered_queryset(self, request: Request) -> 'QuerySet[Post]':
        """
        Returns filtered post queryset by given filtering options.
        """
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
        Gets a detailed post.
        """
        post = self.get_object(post_id)
        serializer = PostListSerializer(post)

        return Response(serializer.data)

    def post_list(self, request: Request) -> Response:
        """
        Gets whole posts which are active.
        """
        queryset = self.get_option_filtered_queryset(request)

        posts = queryset.filter(is_active=True)
        serializer = PostListSerializer(posts, many=True)

        return Response(serializer.data)

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
            return self.post_detail(post_id)
        else:
            return self.post_list(request)

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

        post = self.get_object(post_id)
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
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        serializer.update(post, {'is_active': False})

        return Response(status=status.HTTP_204_NO_CONTENT)
