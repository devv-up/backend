import pytest


@pytest.fixture
def user_post_data(users, posts):
    return {'user': users[0].id, 'post': posts[0].id}


class TestLike:
    pytestmark = pytest.mark.django_db

    def _like_a_post(self, api_client, data):
        response = api_client.post('/posts/likes', data=data, format='json')
        liked_post = api_client.get(f'/posts/{data["post"]}')
        return [response, liked_post]

    def test_create_like(self, api_client, user_post_data):
        response, liked_post = self._like_a_post(api_client, user_post_data)
        assert response.status_code == 201
        assert liked_post.data['likes'] == 1

        # Prevent requesting like to the same post.
        response, liked_post = self._like_a_post(api_client, user_post_data)
        assert response.status_code == 400
        assert liked_post.data['likes'] == 1

    def test_dislike(self, api_client, user_post_data):
        response, liked_post = self._like_a_post(api_client, user_post_data)
        response = api_client.delete('/posts/likes', data=user_post_data, format='json')
        disliked_post = api_client.get('/posts/1')
        assert response.status_code == 204
        assert liked_post.data['likes'] != disliked_post.data['likes']

        # Prevent requesting dislike to the same post.
        response = api_client.delete('/posts/likes', data=user_post_data, format='json')
        assert response.status_code == 404
