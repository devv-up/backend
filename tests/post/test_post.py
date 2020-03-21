import pytest


class TestPost:
    pytestmark = pytest.mark.django_db

    def test_create_post(self, api_client, users, categories, tags):
        post_data = {
            'title': 'test_title',
            'content': 'test_content',
            'location': 'test_location',
            'capacity': 10,
            'date': '2020-01-01',
            'timeOfDay': 1,
            'author': 1,
            'category': 1,
            'tags': [1, 2],
        }
        response = api_client.post('/posts', data=post_data)
        assert response.status_code == 201

        # Create a post without a category.
        bad_post_data = {
            'title': 'test_title',
            'location': 'test_location',
            'capacity': 10,
            'timeOfDay': 1,
            'author': 1,
        }
        response = api_client.post('/posts', data=bad_post_data)
        assert response.status_code == 400

    def test_list_posts(self, api_client, posts):
        response = api_client.get('/posts')
        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_post(self, api_client, posts):
        response = api_client.get('/posts/1')
        assert response.status_code == 200
        assert response.data['id'] == 1

        # Get a post that doesn't exist.
        response = api_client.get('/posts/65535')
        assert response.status_code == 404

    def test_update_post(self, api_client, posts):
        before_update = api_client.get('/posts/1')
        response = api_client.patch('/posts/1', data={'title': 'after'})

        assert response.status_code == 201
        assert response.data['id'] == 1
        assert response.data['title'] == 'after'
        assert before_update.data['title'] != 'after'

        # Update the author of the post.
        bad_post_data = {
            'title': 'test_title',
            'location': 'test_location',
            'capacity': 10,
            'timeOfDay': 1,
            'author': 1,
        }
        response = api_client.patch('/posts/1', data=bad_post_data)
        assert response.status_code == 403

    def test_delete_post(self, api_client, posts):
        before_delete = api_client.get('/posts/1')
        response = api_client.delete('/posts/1')
        after_delete = api_client.get('/posts/1')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404
