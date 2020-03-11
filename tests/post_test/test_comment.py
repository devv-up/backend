import pytest


@pytest.mark.django_db
class TestComment:
    pytestmark = pytest.mark.django_db

    def test_create_comment(self, api_client, users, posts, comment_data):
        response = api_client.post('/comments', comment_data)

        assert response.status_code == 201

    def test_create_comment_without_post_no(self, api_client, users, bad_comment_data):
        response = api_client.post('/comments', bad_comment_data)

        assert response.status_code == 400

    def test_list_commments(self, api_client, comments):
        response = api_client.get('/comments')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_comments(self, api_client, comments, comment_id):
        response = api_client.get(f'/comments/{comment_id}')

        assert response.status_code == 200
        assert response.data.get('id') == comment_id

    def test_detail_missing_comment(self, api_client):
        response = api_client.get('/comments/65535')

        assert response.status_code == 404

    def test_update_comment(self, api_client, comments, comment_id, content_data):
        before_update = api_client.get(f'/comments/{comment_id}')
        response = api_client.put(f'/comments/{comment_id}', data=content_data)

        assert response.status_code == 201
        assert response.data.get('id') == comment_id
        assert response.data.get('content') == content_data.get('content')
        assert before_update.data.get('content') != content_data.get('content')

    def test_update_comment_with_bad_access(self, api_client, comments, comment_id, bad_post_data):
        response = api_client.put(f'/comments/{comment_id}', data=bad_post_data)

        assert response.status_code == 403

    def test_delete_post(self, api_client, comments, comment_id):
        before_delete = api_client.get(f'/comments/{comment_id}')
        response = api_client.delete(f'/comments/{comment_id}')
        after_delete = api_client.get(f'/comments/{comment_id}')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
