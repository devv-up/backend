import pytest

from post.models import Post
from tests.post.jwt_token import get_jwt_token_of


class TestPost:
    pytestmark = pytest.mark.django_db

    def test_create_post(self, api_client, users, categories):
        token = f'JWT {get_jwt_token_of(users[0])}'
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
        response = api_client.post('/posts', data=post_data,
                                   HTTP_AUTHORIZATION=token, format='json', secure=True)
        assert response.status_code == 201

        # Create a post with tag titles that already exist.
        before_creating = api_client.get('/posts/tags', secure=True)

        response = api_client.post('/posts', data=post_data,
                                   HTTP_AUTHORIZATION=token, format='json', secure=True)
        assert response.status_code == 201

        after_creating = api_client.get('/posts/tags', secure=True)
        assert len(before_creating.data) == len(after_creating.data)

        # Create a post without a category ID and tag titles.
        bad_post_data = {
            'title': 'test_title',
            'location': 'test_location',
            'capacity': 10,
            'timeOfDay': 1,
            'author': 1,
        }
        response = api_client.post('/posts', data=bad_post_data,
                                   HTTP_AUTHORIZATION=token, format='json', secure=True)
        assert response.status_code == 400

        # Cause an error of creating post after creating tags successfully
        # in order to test transaction.
        before_transaction = api_client.get('/posts/tags', secure=True)

        post_data['tags'] = ['tag3', 'tag4']
        post_data['title'] = '1'*100
        response = api_client.post('/posts', data=post_data,
                                   HTTP_AUTHORIZATION=token, format='json', secure=True)
        assert response.status_code == 400

        after_transaction = api_client.get('/posts/tags', secure=True)
        assert before_transaction.data == after_transaction.data

    def test_list_posts(self, api_client, many_posts, users):
        # Pagination
        response = api_client.get('/posts', secure=True)
        assert response.status_code == 200
        assert len(response.data) > 1

        # Pagination by specific number per page
        response = api_client.get('/posts?page=1&pageSize=30', secure=True)
        assert response.status_code == 200
        assert len(response.data) == 30

    def test_detail_post(self, api_client, posts, users):
        response = api_client.get('/posts/1', secure=True)
        assert response.status_code == 200
        assert response.data['id'] == 1

        # Get a post that doesn't exist.
        response = api_client.get('/posts/65535', secure=True)
        assert response.status_code == 404

    def test_update_post(self, api_client, posts, tags, users):
        token = f'JWT {get_jwt_token_of(users[0])}'
        before_update = api_client.get('/posts/1', secure=True)

        data = {
            'title': 'after',
            'tags': [tags[0].title, tags[1].title]
        }
        response = api_client.patch('/posts/1', data=data,
                                    HTTP_AUTHORIZATION=token, format='json', secure=True)

        updated_post = Post.objects.get(id=1)
        assert response.status_code == 200
        assert updated_post.id == 1
        assert updated_post.title == 'after'
        assert before_update.data['title'] != 'after'

        # Prevent updating the created date of the post.
        before_update = api_client.get('/posts/1', secure=True)

        bad_post_data = {
            'title': 'test_title',
            'location': 'test_location',
            'capacity': 10,
            'timeOfDay': 1,
            'createdDate': '2020-02-02',
        }
        response = api_client.patch('/posts/1', data=bad_post_data,
                                    HTTP_AUTHORIZATION=token, format='json', secure=True)
        after_update = api_client.get('/posts/1', secure=True)
        assert before_update.data['createdDate'] == after_update.data['createdDate']

        # Update the tags of the post.
        before_update = api_client.get('/posts/1', secure=True)

        tags = {'tags': ['tag1', 'tag2']}
        response = api_client.patch('/posts/1', data=tags,
                                    HTTP_AUTHORIZATION=token, format='json', secure=True)
        assert response.status_code == 200

        after_update = api_client.get('/posts/1', secure=True)
        assert before_update.data['tags'][0]['title'] != after_update.data['tags'][0]['title']

        # Update the post without any data.
        response = api_client.patch('/posts/1', HTTP_AUTHORIZATION=token, secure=True)
        assert response.status_code == 400

    def test_delete_post(self, api_client, posts, users):
        token = f'JWT {get_jwt_token_of(users[0])}'
        response = api_client.delete('/posts/1', HTTP_AUTHORIZATION=token, secure=True)
        after_delete = api_client.get('/posts/1', secure=True)

        assert response.status_code == 204
        assert after_delete.status_code == 404
