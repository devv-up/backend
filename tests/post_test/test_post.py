import pytest


@pytest.mark.django_db
class TestPost:
    pytestmark = pytest.mark.django_db

    def test_create_post(self, api_client, post_data, users, categories, tags):
        response = api_client.post('/posts', post_data)

        assert response.status_code == 201

    def test_create_post_without_category_no(self, api_client, users, tags, bad_post_data):
        response = api_client.post('/posts', bad_post_data)

        assert response.status_code == 400

    def test_list_posts(self, api_client, posts):
        response = api_client.get('/posts')

        assert response.status_code == 200
        assert len(response.data) > 1

    def test_detail_post(self, api_client, posts, dummy_id):
        response = api_client.get(f'/posts/{dummy_id}')

        assert response.status_code == 200
        assert response.data.get('id') == dummy_id

    def test_detail_missing_post(self, api_client):
        response = api_client.get('/posts/65535')

        assert response.status_code == 404

    def test_update_post(self, api_client, posts, dummy_id, title_data):
        before_update = api_client.get(f'/posts/{dummy_id}')
        response = api_client.put(f'/posts/{dummy_id}', data=title_data)

        assert response.status_code == 201
        assert response.data.get('id') == dummy_id
        assert response.data.get('title') == title_data.get('title')
        assert before_update.data.get('title') != title_data.get('title')

    def test_update_post_with_bad_access(self, api_client, posts, dummy_id, bad_post_data):
        response = api_client.put(f'/posts/{dummy_id}', data=bad_post_data)

        assert response.status_code == 403

    def test_delete_post(self, api_client, posts, dummy_id):
        before_delete = api_client.get(f'/posts/{dummy_id}')
        response = api_client.delete(f'/posts/{dummy_id}')
        after_delete = api_client.get(f'/posts/{dummy_id}')

        assert before_delete.status_code == 200
        assert response.status_code == 204
        assert after_delete.status_code == 404

    def test_post_on_category_filtering(self, api_client,
                                        users, categories, tags,
                                        post_preset_data):
        post1_data = {
            **post_preset_data,
            'author': users[0].id,
            'category': categories[0].id,
            'tags': [tags[0].id]
        }
        post2_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[1].id,
            'tags': [tags[1].id]
        }
        post3_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[0].id,
            'tags': [tags[0].id, tags[1].id, tags[2].id]
        }

        post1 = api_client.post('/posts', post1_data).data
        post2 = api_client.post('/posts', post2_data).data
        post3 = api_client.post('/posts', post3_data).data
        assert post1 != post2 and post1 != post3 and post2 != post3

        category_no = categories[0].id
        response = api_client.get(f'/posts?category={category_no}')

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0].get('id') != response.data[1].get('id')
        assert response.data[0].get('category').get('id') == category_no
        assert response.data[1].get('category').get('id') == category_no

    def test_post_on_a_tag_filtering(self, api_client,
                                     users, categories, tags,
                                     post_preset_data):
        post1_data = {
            **post_preset_data,
            'author': users[0].id,
            'category': categories[0].id,
            'tags': [tags[0].id]
        }
        post2_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[1].id,
            'tags': [tags[0].id, tags[1].id]
        }
        post3_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[0].id,
            'tags': [tags[0].id, tags[1].id, tags[2].id]
        }

        post1 = api_client.post('/posts', post1_data).data
        post2 = api_client.post('/posts', post2_data).data
        post3 = api_client.post('/posts', post3_data).data
        assert post1 != post2 and post1 != post3 and post2 != post3

        tag_no = tags[1].id
        response = api_client.get(f'/posts?tags={tag_no}')

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0].get('id') != response.data[1].get('id')

        result = 0
        for tag in response.data[0].get('tags'):
            if tag_no == tag.get('id'):
                result += 1
        assert result == 1

        result = 0
        for tag in response.data[1].get('tags'):
            if tag_no == tag.get('id'):
                result += 1
        assert result == 1

    def test_post_on_two_tag_filtering(self, api_client,
                                       users, categories, tags,
                                       post_preset_data):
        post1_data = {
            **post_preset_data,
            'author': users[0].id,
            'category': categories[0].id,
            'tags': [tags[0].id]
        }
        post2_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[1].id,
            'tags': [tags[0].id, tags[1].id]
        }
        post3_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[0].id,
            'tags': [tags[0].id, tags[1].id, tags[2].id]
        }

        post1 = api_client.post('/posts', post1_data).data
        post2 = api_client.post('/posts', post2_data).data
        post3 = api_client.post('/posts', post3_data).data
        assert post1 != post2 and post1 != post3 and post2 != post3

        (tag_no1, tag_no2) = (tags[0].id, tags[1].id)
        response = api_client.get(f'/posts?tags={tag_no1}&tags={tag_no2}')

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0].get('id') != response.data[1].get('id')

        result = 0
        for tag in response.data[0].get('tags'):
            if tag_no1 == tag.get('id'):
                result += 1
            elif tag_no2 == tag.get('id'):
                result += 1
        assert result == 2

        result = 0
        for tag in response.data[1].get('tags'):
            if tag_no1 == tag.get('id'):
                result += 1
            elif tag_no2 == tag.get('id'):
                result += 1
        assert result == 2

    def test_post_on_two_option_filtering(self, api_client,
                                          users, categories, tags,
                                          post_preset_data):
        post1_data = {
            **post_preset_data,
            'author': users[0].id,
            'category': categories[0].id,
            'tags': [tags[0].id]
        }
        post2_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[1].id,
            'tags': [tags[0].id, tags[1].id]
        }
        post3_data = {
            **post_preset_data,
            'author': users[1].id,
            'category': categories[0].id,
            'tags': [tags[0].id, tags[1].id, tags[2].id]
        }

        post1 = api_client.post('/posts', post1_data).data
        post2 = api_client.post('/posts', post2_data).data
        post3 = api_client.post('/posts', post3_data).data
        assert post1 != post2 and post1 != post3 and post2 != post3

        (category_no, tag_no) = (categories[0].id, tags[1].id)
        response = api_client.get(f'/posts?category={category_no}&tags={tag_no}')

        assert response.status_code == 200
        assert len(response.data) == 1

        assert category_no == response.data[0].get('category').get('id')

        result = 0
        for tag in response.data[0].get('tags'):
            if tag_no == tag.get('id'):
                result += 1
        assert result == 1
