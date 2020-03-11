import pytest


@pytest.mark.django_db
class TestPost:
    pytestmark = pytest.mark.django_db

    def test_create_post(self, api_client, post_data, users, categories, tags):
        response = api_client.post('/posts', post_data)

        assert response.status_code == 201

    def test_create_post_without_category_no(self, api_client, users, tags, bad_post_data):
        response = api_client.post('/posts', bad_post_data)

        assert response.status_code == 400

    def test_list_posts(self, api_client, posts):
        response = api_client.get('/posts')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_post(self, api_client, posts, post_id):
        response = api_client.get(f'/posts/{post_id}')

        assert response.status_code == 200
        assert response.data.get('id') == post_id

    def test_detail_missing_post(self, api_client):
        response = api_client.get('/posts/65535')

        assert response.status_code == 404

    def test_update_post(self, api_client, posts, post_id, title_data):
        before_update = api_client.get(f'/posts/{post_id}')
        response = api_client.put(f'/posts/{post_id}', data=title_data)

        assert response.status_code == 201
        assert response.data.get('id') == post_id
        assert response.data.get('title') == title_data.get('title')
        assert before_update.data.get('title') != title_data.get('title')

    def test_update_post_with_bad_access(self, api_client, posts, post_id, bad_post_data):
        response = api_client.put(f'/posts/{post_id}', data=bad_post_data)

        assert response.status_code == 403

    def test_delete_post(self, api_client, posts, post_id):
        before_delete = api_client.get(f'/posts/{post_id}')
        response = api_client.delete(f'/posts/{post_id}')
        after_delete = api_client.get(f'/posts/{post_id}')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
