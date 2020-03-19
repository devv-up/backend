import pytest


@pytest.mark.django_db
class TestTag:
    pytestmark = pytest.mark.django_db

    def test_create_tag(self, api_client, title_data):
        response = api_client.post('/posts/tags', title_data)
        assert response.status_code == 201

    def test_create_the_same_title_tag(self, api_client, title_data):
        response1 = api_client.post('/posts/tags', title_data)
        response2 = api_client.post('/posts/tags', title_data)

        assert response1.status_code == 201
        assert response2.status_code == 400

    def test_create_tag_without_title(self, api_client):
        response = api_client.post('/posts/tags')
        assert response.status_code == 400

    def test_list_tags(self, api_client, tags):
        response = api_client.get('/posts/tags')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_tag(self, api_client, tags, dummy_id):
        response = api_client.get(f'/posts/tags/{dummy_id}')

        assert response.status_code == 200
        assert response.data.get('id') == dummy_id

    def test_detail_missing_tag(self, api_client):
        response = api_client.get('/posts/tags/65535')
        assert response.status_code == 404

    def test_update_tag_request(self, api_client, tags, dummy_id, title_data):
        response = api_client.put(f'/posts/tags/{dummy_id}', data=title_data)
        assert response.status_code == 405

    def test_delete_tag(self, api_client, tags, dummy_id):
        before_delete = api_client.get(f'/posts/tags/{dummy_id}')
        response = api_client.delete(f'/posts/tags/{dummy_id}')
        after_delete = api_client.get(f'/posts/tags/{dummy_id}')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
