import pytest


@pytest.mark.django_db
class TestTag:
    pytestmark = pytest.mark.django_db

    def test_create_tag(self, api_client):
        response = api_client.post('/posts/tags', data={'title': 'creating'})
        assert response.status_code == 201

    def test_create_the_same_title_tag(self, api_client):
        response1 = api_client.post('/posts/tags', data={'title': 'duplicates'})
        response2 = api_client.post('/posts/tags', data={'title': 'duplicates'})

        assert response1.status_code == 201
        assert response2.status_code == 400

    def test_create_tag_without_title(self, api_client):
        response = api_client.post('/posts/tags')
        assert response.status_code == 400

    def test_list_tags(self, api_client, tags):
        response = api_client.get('/posts/tags')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_tag(self, api_client, tags):
        response = api_client.get('/posts/tags/1')

        assert response.status_code == 200
        assert response.data['id'] == 1

    def test_detail_missing_tag(self, api_client):
        response = api_client.get('/posts/tags/65535')
        assert response.status_code == 404

    def test_update_tag_request(self, api_client, tags):
        response = api_client.put('/posts/tags/1', data={'title': 'updating'})
        assert response.status_code == 405

    def test_delete_tag(self, api_client, tags):
        before_delete = api_client.get('/posts/tags/1')
        response = api_client.delete('/posts/tags/1')
        after_delete = api_client.get('/posts/tags/1')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
