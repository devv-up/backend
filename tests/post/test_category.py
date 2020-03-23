import pytest


class TestCategory:
    pytestmark = pytest.mark.django_db

    def test_list_categories(self, api_client, categories):
        response = api_client.get('/posts/categories')
        assert response.status_code == 200
        assert len(response.data) > 1
