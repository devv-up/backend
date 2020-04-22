import pytest

from post.models import Comment


class TestComment:
    pytestmark = pytest.mark.django_db

    def test_create_comment(self, api_client, users, posts):
        response = api_client.post('/posts/comments', data={
            'content': 'creating',
            'post': 1,
            'author': 1,
        }, format='json')
        assert response.status_code == 201

        # Create a comment without a post ID
        response = api_client.post(
            '/posts/comments', data={'content': 'no_post_id'}, format='json')
        assert response.status_code == 400

    def test_update_comment(self, api_client, comments):
        content_before_update = Comment.objects.get(id=1).content
        response = api_client.put(
            '/posts/comments/1', data={'content': 'after'}, format='json')

        updated_comment = Comment.objects.get(id=1)
        assert response.status_code == 200
        assert updated_comment.id == 1
        assert updated_comment.content == 'after'
        assert updated_comment.content != content_before_update

        # Update the comment without any data.
        response = api_client.put('/posts/comments/1')
        assert response.status_code == 400

    def test_delete_comment(self, api_client, comments):
        response = api_client.delete('/posts/comments/1')
        comment = Comment.objects.get(id=1)

        assert response.status_code == 204
        assert comment.is_active is False
