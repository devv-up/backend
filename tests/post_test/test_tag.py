import pytest
from rest_framework.test import APIClient

from post.models import Tag


class _Fixtures:
    @pytest.fixture
    def api_client(self) -> APIClient:
        return APIClient()

    @pytest.fixture
    def tag_id(self) -> int:
        return 1

    @pytest.fixture
    def title(self) -> str:
        return 'test_title'

    @pytest.fixture
    def title_data(self, title) -> dict:
        return {'title': title}

    @pytest.fixture
    def tags(self, title) -> None:
        return Tag.objects.bulk_create(
            [Tag(title=f'{title} {i+1}')
                for i in range(3)]
        )


@pytest.mark.django_db
class TestTag(_Fixtures):
    pytestmark = pytest.mark.django_db

    def test_create_tag(self, api_client, title_data):
        response = api_client.post('/tag/', title_data)

        assert response.status_code == 201

    def test_create_the_same_title_tag(self, api_client, title_data):
        response1 = api_client.post('/tag/', title_data)
        response2 = api_client.post('/tag/', title_data)

        assert response1.status_code == 201
        assert response2.status_code == 400

    def test_create_tag_without_title(self, api_client):
        response = api_client.post('/tag/')

        assert response.status_code == 400

    def test_list_tags(self, api_client, tags):
        response = api_client.get('/tags/')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_tag(self, api_client, tags, tag_id):
        response = api_client.get(f'/tag/{tag_id}/')

        assert response.status_code == 200
        assert response.data.get('id') == tag_id

    def test_detail_missing_tag(self, api_client):
        response = api_client.get('/tag/65535/')

        assert response.status_code == 404

    def test_update_tag(self, api_client, tags, tag_id, title_data):
        before_update = api_client.get(f'/tag/{tag_id}/')
        response = api_client.put(f'/tag/{tag_id}/', data=title_data)

        assert response.status_code == 200
        assert response.data.get('id') == tag_id
        assert response.data.get('title') == title_data.get('title')
        assert before_update.data.get('title') != title_data.get('title')

    def test_delete_tag(self, api_client, tags, tag_id, title_data):
        before_delete = api_client.get(f'/tag/{tag_id}/')
        response = api_client.delete(f'/tag/{tag_id}/')
        after_delete = api_client.get(f'/tag/{tag_id}/')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
