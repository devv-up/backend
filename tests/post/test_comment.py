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

        assert response.status_code == 201
        assert response.data['id'] == 1
        assert response.data['content'] == 'after'
        assert response.data['content'] != content_before_update

        # Update the author of the comment.
        unauthroized_data = {
            'content': 'trying_to_update_author_of_comment',
            'post': 2,
            'author': 2,
        }
        response = api_client.put('/posts/comments/1', data=unauthroized_data, format='json')
        assert response.status_code == 403

        # Update the parent comment of the comment.
        response = api_client.put(
            '/posts/comments/1', data={"parent_comment": 65535}, format='json')
        assert response.status_code == 403

    def test_delete_comment(self, api_client, comments):
        comments_length_before = len(Comment.objects.filter(is_active=True))
        response = api_client.delete('/posts/comments/1')
        comments_length_after = len(Comment.objects.filter(is_active=True))

        assert comments_length_before == 3
        assert response.status_code == 204
        assert comments_length_after == 2
