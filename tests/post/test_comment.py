import pytest

from post.models import Comment
from tests.post.jwt_token import get_jwt_token_of


class TestComment:
    pytestmark = pytest.mark.django_db

    def test_create_comment(self, api_client, users, posts):
        token = f'JWT {get_jwt_token_of(users[0])}'
        response = api_client.post('/posts/comments', data={
            'content': 'creating',
            'post': 1,
            'author': 1,
        }, HTTP_AUTHORIZATION=token, format='json', secure=True)
        assert response.status_code == 201

        # Create a comment without a post ID
        response = api_client.post(
            '/posts/comments',
            data={'content': 'no_post_id'},
            HTTP_AUTHORIZATION=token,
            format='json',
            secure=True)
        assert response.status_code == 400

    def test_update_comment(self, api_client, comments, users):
        token = f'JWT {get_jwt_token_of(users[0])}'
        content_before_update = Comment.objects.get(id=1).content
        response = api_client.put(
            '/posts/comments/1',
            data={'content': 'after'},
            HTTP_AUTHORIZATION=token,
            format='json',
            secure=True)

        updated_comment = Comment.objects.get(id=1)
        assert response.status_code == 200
        assert updated_comment.id == 1
        assert updated_comment.content == 'after'
        assert updated_comment.content != content_before_update

        # Update the comment without any data.
        response = api_client.put('/posts/comments/1', HTTP_AUTHORIZATION=token, secure=True)
        assert response.status_code == 400

    def test_delete_comment(self, api_client, comments, users):
        token = f'JWT {get_jwt_token_of(users[0])}'
        response = api_client.delete('/posts/comments/1', HTTP_AUTHORIZATION=token, secure=True)
        comment = Comment.objects.get(id=1)

        assert response.status_code == 204
        assert not comment.is_active
