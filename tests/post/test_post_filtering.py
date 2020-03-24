import pytest


class TestPostFiltering:
    pytestmark = pytest.mark.django_db
    preset_data = {
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

    def count_tags_of(self, result, *tag_id):
        tag_count = 0
        for tag in result['tags']:
            if tag_id[0] == tag['id']:
                tag_count += 1
            elif len(tag_id) > 1 and tag_id[1] == tag['id']:
                tag_count += 1
        return tag_count

    def test_post_on_category_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**self.preset_data} for i in range(3)]

        post1_data['category'] = categories[0].id
        post2_data['category'] = categories[1].id
        post3_data['category'] = categories[0].id

        post1 = api_client.post('/posts', post1_data, format='json').data
        post2 = api_client.post('/posts', post2_data, format='json').data
        post3 = api_client.post('/posts', post3_data, format='json').data
        assert post1 != post2 and post1 != post3 and post2 != post3

        category_id = categories[0].id
        response = api_client.get(f'/posts?category={category_id}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['id'] != second_result['id']
        assert first_result['category']['id'] == category_id
        assert second_result['category']['id'] == category_id

    def test_post_on_tag_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**self.preset_data} for i in range(3)]

        post1_data['tags'] = [tags[0].title]
        post2_data['tags'] = [tags[0].title, tags[1].title]
        post3_data['tags'] = [tags[0].title, tags[1].title, tags[2].title]

        post1 = api_client.post('/posts', post1_data, format='json').data
        post2 = api_client.post('/posts', post2_data, format='json').data
        post3 = api_client.post('/posts', post3_data, format='json').data
        assert post1 != post2 and post1 != post3 and post2 != post3

        tag_id = tags[1].id
        response = api_client.get(f'/posts?tags={tag_id}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['id'] != second_result['id']

        number_of_tags = self.count_tags_of(first_result, tag_id)
        assert number_of_tags == 1

        number_of_tags = self.count_tags_of(second_result, tag_id)
        assert number_of_tags == 1

        # Filter the posts by more than one tag.
        tag_id1, tag_id2 = tags[0].id, tags[1].id
        response = api_client.get(f'/posts?tags={tag_id1},{tag_id2}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['id'] != second_result['id']

        number_of_tags = self.count_tags_of(first_result, tag_id1, tag_id2)
        assert number_of_tags == 2

        number_of_tags = self.count_tags_of(second_result, tag_id1, tag_id2)
        assert number_of_tags == 2

        # This type of tag filtering is not supported.
        response = api_client.get(f'/posts?tags={tag_id1}&tags={tag_id2}')
        assert response.status_code == 400

    def test_post_on_category_tag_filtering(self, api_client, users, categories, tags):
        post1_data = {
            **self.preset_data,
            'category': categories[0].id,
            'tags': [tags[0].title]
        }
        post2_data = {
            **self.preset_data,
            'category': categories[1].id,
            'tags': [tags[0].title, tags[1].title]
        }
        post3_data = {
            **self.preset_data,
            'category': categories[0].id,
            'tags': [tags[0].title, tags[1].title, tags[2].title]
        }

        post1 = api_client.post('/posts', post1_data, format='json').data
        post2 = api_client.post('/posts', post2_data, format='json').data
        post3 = api_client.post('/posts', post3_data, format='json').data
        assert post1 != post2 and post1 != post3 and post2 != post3

        category_id, tag_id = categories[0].id, tags[1].id
        response = api_client.get(f'/posts?category={category_id}&tags={tag_id}')
        assert response.status_code == 200
        assert len(response.data) == 1

        result = response.data[0]
        assert category_id == result['category']['id']

        number_of_tags = self.count_tags_of(result, tag_id)
        assert number_of_tags == 1

    def test_post_on_date_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**self.preset_data} for i in range(3)]

        post1_data['date'] = '2020-01-01'
        post2_data['date'] = '2020-02-02'
        post3_data['date'] = '2020-03-03'

        post1 = api_client.post('/posts', post1_data, format='json').data
        post2 = api_client.post('/posts', post2_data, format='json').data
        post3 = api_client.post('/posts', post3_data, format='json').data
        assert post1 != post2 and post1 != post3 and post2 != post3

        start_date, end_date = '2020-01-01', '2020-02-02'
        response = api_client.get(f'/posts?startDate={start_date}&endDate={end_date}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['date'] >= start_date and first_result['date'] <= end_date
        assert second_result['date'] >= start_date and second_result['date'] <= end_date

    def test_post_on_time_of_day_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**self.preset_data} for i in range(3)]

        time_of_day = {
            'MORNING': 0,
            'AFTERNOON': 1,
            'EVENING': 2,
        }

        post1_data['timeOfDay'] = time_of_day['MORNING']
        post2_data['timeOfDay'] = time_of_day['AFTERNOON']
        post3_data['timeOfDay'] = time_of_day['AFTERNOON']

        post1 = api_client.post('/posts', post1_data, format='json').data
        post2 = api_client.post('/posts', post2_data, format='json').data
        post3 = api_client.post('/posts', post3_data, format='json').data
        assert post1 != post2 and post1 != post3 and post2 != post3

        time_of_day = time_of_day['AFTERNOON']
        response = api_client.get(f'/posts?timeOfDay={time_of_day}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result.get('timeOfDay') == time_of_day
        assert second_result.get('timeOfDay') == time_of_day

    def test_post_on_location_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**self.preset_data} for i in range(3)]

        post1_data['location'] = 'location1'
        post2_data['location'] = 'seoul'
        post3_data['location'] = 'test_location3'

        post1 = api_client.post('/posts', post1_data, format='json').data
        post2 = api_client.post('/posts', post2_data, format='json').data
        post3 = api_client.post('/posts', post3_data, format='json').data
        assert post1 != post2 and post1 != post3 and post2 != post3

        location = 'location'
        response = api_client.get(f'/posts?location={location}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert location in first_result['location']
        assert location in second_result['location']
