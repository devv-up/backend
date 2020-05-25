import pytest


class TestTag:
    pytestmark = pytest.mark.django_db

    def test_list_tags(self, api_client, tags):
        response = api_client.get('/posts/tags', secure=True)
        assert response.status_code == 200
        assert len(response.data) > 1
