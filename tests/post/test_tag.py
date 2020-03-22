import pytest


class TestTag:
    pytestmark = pytest.mark.django_db

    def test_list_tags(self, api_client, tags):
        response = api_client.get('/posts/tags')
        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_tag(self, api_client, tags):
        response = api_client.get('/posts/tags/1')
        assert response.status_code == 200
        assert response.data['id'] == 1

        # Get a tag that doesn't exist.
        response = api_client.get('/posts/tags/65535')
        assert response.status_code == 404
