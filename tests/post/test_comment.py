import pytest


@pytest.mark.django_db
class TestComment:
    pytestmark = pytest.mark.django_db

    def test_create_comment(self, api_client, users, posts):
        response = api_client.post('/posts/comments', data={
            'content': 'creating',
            'post': 1,
            'author': 1,
        })
        assert response.status_code == 201

    def test_create_comment_without_post_id(self, api_client, users):
        response = api_client.post('/posts/comments', data={'content': 'no_post_id'})
        assert response.status_code == 400

    def test_list_commments(self, api_client, comments):
        response = api_client.get('/posts/comments')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_comments(self, api_client, comments):
        response = api_client.get('/posts/comments/1')

        assert response.status_code == 200
        assert response.data['id'] == 1

    def test_detail_missing_comment(self, api_client):
        response = api_client.get('/posts/comments/65535')
        assert response.status_code == 404

    def test_update_comment(self, api_client, comments):
        before_update = api_client.get('/posts/comments/1')
        response = api_client.put('/posts/comments/1', data={'content': 'after'})

        assert response.status_code == 201
        assert response.data['id'] == 1
        assert response.data['content'] == 'after'
        assert before_update.data['content'] != 'after'

    def test_update_comment_with_bad_access(self, api_client, comments):
        unauthroized_data = {
            'content': 'trying_to_update_author_of_comment',
            'post': 2,
            'author': 2,
        }
        response = api_client.put('/posts/comments/1', data=unauthroized_data)
        assert response.status_code == 403

    def test_update_parent_comment(self, api_client, comments):
        response = api_client.put('/posts/comments/1', data={"parent_comment": 65535})
        assert response.status_code == 403

    def test_delete_post(self, api_client, comments):
        before_delete = api_client.get('/posts/comments/1')
        response = api_client.delete('/posts/comments/1')
        after_delete = api_client.get('/posts/comments/1')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
