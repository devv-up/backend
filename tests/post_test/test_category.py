import pytest


@pytest.mark.django_db
class TestCategory:
    pytestmark = pytest.mark.django_db

    def test_create_category(self, api_client, title_data):
        response = api_client.post('/categories', title_data)

        assert response.status_code == 201

    def test_create_the_same_title_category(self, api_client, title_data):
        response1 = api_client.post('/categories', title_data)
        response2 = api_client.post('/categories', title_data)

        assert response1.status_code == 201
        assert response2.status_code == 400

    def test_create_category_without_title(self, api_client):
        response = api_client.post('/categories')

        assert response.status_code == 400

    def test_list_categories(self, api_client, categories):
        response = api_client.get('/categories')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_category(self, api_client, categories, category_id):
        response = api_client.get(f'/categories/{category_id}')

        assert response.status_code == 200
        assert response.data.get('id') == category_id

    def test_detail_missing_category(self, api_client):
        response = api_client.get('/categories/65535')

        assert response.status_code == 404

    def test_update_category(self, api_client, categories, category_id, title_data):
        before_update = api_client.get(f'/categories/{category_id}')
        response = api_client.put(f'/categories/{category_id}', data=title_data)

        assert response.status_code == 201
        assert response.data.get('id') == category_id
        assert response.data.get('title') == title_data.get('title')
        assert before_update.data.get('title') != title_data.get('title')

    def test_delete_category(self, api_client, categories, category_id):
        before_delete = api_client.get(f'/categories/{category_id}')
        response = api_client.delete(f'/categories/{category_id}')
        after_delete = api_client.get(f'/categories/{category_id}')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
