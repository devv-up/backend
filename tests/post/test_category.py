import pytest


@pytest.mark.django_db
class TestCategory:
    pytestmark = pytest.mark.django_db

    def test_create_category(self, api_client):
        response = api_client.post('/posts/categories', data={'title': 'creating'})
        assert response.status_code == 201

    def test_create_the_same_title_category(self, api_client):
        response1 = api_client.post('/posts/categories', data={'title': 'duplicates'})
        response2 = api_client.post('/posts/categories', data={'title': 'duplicates'})

        assert response1.status_code == 201
        assert response2.status_code == 400

    def test_create_category_without_title(self, api_client):
        response = api_client.post('/posts/categories')
        assert response.status_code == 400

    def test_list_categories(self, api_client, categories):
        response = api_client.get('/posts/categories')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_category(self, api_client, categories):
        response = api_client.get('/posts/categories/1')

        assert response.status_code == 200
        assert response.data['id'] == 1

    def test_detail_missing_category(self, api_client):
        response = api_client.get('/posts/categories/65535')
        assert response.status_code == 404

    def test_update_category(self, api_client, categories):
        before_update = api_client.get('/posts/categories/1')
        response = api_client.put('/posts/categories/1', data={'title': 'after'})

        assert response.status_code == 201
        assert response.data['id'] == 1
        assert response.data['title'] == 'after'
        assert before_update.data['title'] != 'after'

    def test_delete_category(self, api_client, categories):
        before_delete = api_client.get('/posts/categories/1')
        response = api_client.delete('/posts/categories/1')
        after_delete = api_client.get('/posts/categories/1')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
