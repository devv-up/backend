import pytest


class TestPost:
    pytestmark = pytest.mark.django_db

    def test_create_post(self, api_client, users, categories):
        post_data = {
            'title': 'test_title',
            'content': 'test_content',
            'location': 'test_location',
            'capacity': 10,
            'date': '2020-01-01',
            'timeOfDay': 1,
            'author': 1,
            'category': 1,
            'tags': ['tag1', 'tag2'],
        }
        response = api_client.post('/posts', data=post_data, format='json')
        tags_before = api_client.get('/posts/tags')
        assert response.status_code == 201

        # Create a post with tag titles that already exist.
        response = api_client.post('/posts', data=post_data, format='json')
        tags_after = api_client.get('/posts/tags')
        assert response.status_code == 201
        assert len(tags_before.data) == len(tags_after.data)

        # Create a post without a category ID and tag titles.
        bad_post_data = {
            'title': 'test_title',
            'location': 'test_location',
            'capacity': 10,
            'timeOfDay': 1,
            'author': 1,
        }
        response = api_client.post('/posts', data=bad_post_data, format='json')
        assert response.status_code == 400

        # Cause an error of creating post after successfully creating tags
        # in order to test transaction.
        before_transaction = api_client.get('/posts/tags')
        post_data['tags'] = ['tag3', 'tag4']
        post_data['title'] = '1234567890123456789012345678901234567890123456\
                                78901234567890123456789012345678901234567890'
        response = api_client.post('/posts', data=post_data, format='json')
        after_transaction = api_client.get('/posts/tags')
        assert response.status_code == 400
        assert before_transaction.data == after_transaction.data

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

    def test_update_post(self, api_client, posts, tags):
        data = {
            'title': 'after',
            'tags': [tags[0].title, tags[1].title]
        }
        before_update = api_client.get('/posts/1')
        response = api_client.patch('/posts/1', data=data, format='json')

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
            'author': 65535,
        }
        response = api_client.patch('/posts/1', data=bad_post_data, format='json')
        assert response.status_code == 403

        # Update the created date of the post.
        bad_post_data = {
            'title': 'test_title',
            'location': 'test_location',
            'capacity': 10,
            'timeOfDay': 1,
            'createdDate': '2020-02-02',
        }
        before_update = api_client.get('/posts/1')
        response = api_client.patch('/posts/1', data=bad_post_data, format='json')
        after_update = api_client.get('/posts/1')
        assert before_update.data['createdDate'] == after_update.data['createdDate']

        # Update the tags of the post.
        tags = {
            'tags': ['tag1', 'tag2']
        }
        before_update = api_client.get('/posts/1')
        response = api_client.patch('/posts/1', data=tags, format='json')
        after_update = api_client.get('/posts/1')
        assert response.status_code == 201
        assert before_update.data['tags'][0]['title'] != after_update.data['tags'][0]['title']

    def test_delete_post(self, api_client, posts):
        response = api_client.delete('/posts/1')
        after_delete = api_client.get('/posts/1')

        assert response.status_code == 204
        assert after_delete.status_code == 404
