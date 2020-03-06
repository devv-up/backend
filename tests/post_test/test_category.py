import pytest
from rest_framework.test import APIClient

from post.models import Category


class _Fixtures:
    @pytest.fixture
    def api_client(self) -> APIClient:
        return APIClient()

    @pytest.fixture
    def category_id(self) -> int:
        return 1

    @pytest.fixture
    def title(self) -> str:
        return 'test_title'

    @pytest.fixture
    def title_data(self, title) -> dict:
        return {'title': title}

    @pytest.fixture
    def categories(self, title) -> None:
        return Category.objects.bulk_create(
            [Category(title=f'{title} {i+1}')
                for i in range(3)]
        )


@pytest.mark.django_db
class TestCategory(_Fixtures):
    pytestmark = pytest.mark.django_db

    def test_create_category(self, api_client, title_data):
        response = api_client.post('/category/', title_data)

        assert response.status_code == 201

    def test_create_the_same_title_category(self, api_client, title_data):
        response1 = api_client.post('/category/', title_data)
        response2 = api_client.post('/category/', title_data)

        assert response1.status_code == 201
        assert response2.status_code == 400

    def test_create_category_without_title(self, api_client):
        response = api_client.post('/category/')

        assert response.status_code == 400

    def test_list_categories(self, api_client, categories):
        response = api_client.get('/categories/')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_category(self, api_client, categories, category_id):
        response = api_client.get(f'/category/{category_id}/')

        assert response.status_code == 200
        assert response.data.get('id') == category_id

    def test_detail_missing_category(self, api_client):
        response = api_client.get('/category/65535/')

        assert response.status_code == 404

    def test_update_category(self, api_client, categories, category_id, title_data):
        before_update = api_client.get(f'/category/{category_id}/')
        response = api_client.put(f'/category/{category_id}/', data=title_data)

        assert response.status_code == 200
        assert response.data.get('id') == category_id
        assert response.data.get('title') == title_data.get('title')
        assert before_update.data.get('title') != title_data.get('title')

    def test_delete_category(self, api_client, categories, category_id):
        before_delete = api_client.get(f'/category/{category_id}/')
        response = api_client.delete(f'/category/{category_id}/')
        after_delete = api_client.get(f'/category/{category_id}/')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
