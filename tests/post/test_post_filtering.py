import pytest

PRESET_DATA = {
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

TIME_OF_DAY = {
    'MORNING': 0,
    'AFTERNOON': 1,
    'EVENING': 2,
}


class TestPostFiltering:
    pytestmark = pytest.mark.django_db

    def count_tags_of(self, result, *title_filters):
        tags = [tag for tag in result['tags'] if tag['title'] in title_filters]
        return len(tags)

    def set_posts_with(self, api_client, *post_data):
        api_client.post('/posts', post_data[0], format='json')
        api_client.post('/posts', post_data[1], format='json')
        api_client.post('/posts', post_data[2], format='json')

    def test_post_on_category_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**PRESET_DATA} for i in range(3)]

        post1_data['category'] = categories[0].id
        post2_data['category'] = categories[1].id
        post3_data['category'] = categories[0].id
        self.set_posts_with(api_client, post1_data, post2_data, post3_data)

        category_title = categories[0].title
        response = api_client.get(f'/posts?category={category_title}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['id'] != second_result['id']
        assert first_result['category']['title'] == category_title
        assert second_result['category']['title'] == category_title

    def test_post_on_tag_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**PRESET_DATA} for i in range(3)]

        post1_data['tags'] = [tags[0].title]
        post2_data['tags'] = [tags[0].title, tags[1].title]
        post3_data['tags'] = [tags[0].title, tags[1].title, tags[2].title]
        self.set_posts_with(api_client, post1_data, post2_data, post3_data)

        tag_title = tags[1].title
        response = api_client.get(f'/posts?tags={tag_title}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['id'] != second_result['id']

        number_of_tags = self.count_tags_of(first_result, tag_title)
        assert number_of_tags == 1

        number_of_tags = self.count_tags_of(second_result, tag_title)
        assert number_of_tags == 1

        # Filter the posts by more than one tag.
        tag_title1, tag_title2 = tags[0].title, tags[1].title
        response = api_client.get(f'/posts?tags={tag_title1},{tag_title2}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['id'] != second_result['id']

        number_of_tags = self.count_tags_of(first_result, tag_title1, tag_title2)
        assert number_of_tags == 2

        number_of_tags = self.count_tags_of(second_result, tag_title1, tag_title2)
        assert number_of_tags == 2

        # This type of tag filtering is not supported.
        response = api_client.get(f'/posts?tags={tag_title1}&tags={tag_title2}')
        assert response.status_code == 400

    def test_post_on_category_tag_filtering(self, api_client, users, categories, tags):
        post1_data = {
            **PRESET_DATA,
            'category': categories[0].id,
            'tags': [tags[0].title]
        }
        post2_data = {
            **PRESET_DATA,
            'category': categories[1].id,
            'tags': [tags[0].title, tags[1].title]
        }
        post3_data = {
            **PRESET_DATA,
            'category': categories[0].id,
            'tags': [tags[0].title, tags[1].title, tags[2].title]
        }
        self.set_posts_with(api_client, post1_data, post2_data, post3_data)

        category_title, tag_title = categories[0].title, tags[1].title
        response = api_client.get(f'/posts?category={category_title}&tags={tag_title}')
        assert response.status_code == 200
        assert len(response.data) == 1

        result = response.data[0]
        assert category_title == result['category']['title']

        number_of_tags = self.count_tags_of(result, tag_title)
        assert number_of_tags == 1

    def test_post_on_date_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**PRESET_DATA} for i in range(3)]

        post1_data['date'] = '2020-01-01'
        post2_data['date'] = '2020-02-02'
        post3_data['date'] = '2020-03-03'
        self.set_posts_with(api_client, post1_data, post2_data, post3_data)

        start_date, end_date = '2020-01-01', '2020-02-02'
        response = api_client.get(f'/posts?startDate={start_date}&endDate={end_date}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result['date'] >= start_date and first_result['date'] <= end_date
        assert second_result['date'] >= start_date and second_result['date'] <= end_date

    def test_post_on_time_of_day_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**PRESET_DATA} for i in range(3)]

        post1_data['timeOfDay'] = TIME_OF_DAY['MORNING']
        post2_data['timeOfDay'] = TIME_OF_DAY['AFTERNOON']
        post3_data['timeOfDay'] = TIME_OF_DAY['AFTERNOON']
        self.set_posts_with(api_client, post1_data, post2_data, post3_data)

        time_of_day = TIME_OF_DAY['AFTERNOON']
        response = api_client.get(f'/posts?timeOfDay={time_of_day}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert first_result.get('timeOfDay') == time_of_day
        assert second_result.get('timeOfDay') == time_of_day

    def test_post_on_location_filtering(self, api_client, users, categories, tags):
        post1_data, post2_data, post3_data = [{**PRESET_DATA} for i in range(3)]

        post1_data['location'] = 'location1'
        post2_data['location'] = 'seoul'
        post3_data['location'] = 'test_location3'
        self.set_posts_with(api_client, post1_data, post2_data, post3_data)

        location = 'location'
        response = api_client.get(f'/posts?location={location}')
        assert response.status_code == 200
        assert len(response.data) == 2

        first_result, second_result = response.data[0], response.data[1]
        assert location in first_result['location']
        assert location in second_result['location']
