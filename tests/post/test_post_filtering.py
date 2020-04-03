import pytest
from model_bakery.recipe import Recipe

from post.models import Post

TIME_OF_DAY = {
    'MORNING': 0,
    'AFTERNOON': 1,
    'EVENING': 2,
}


@pytest.fixture
def posts(categories, tags):
    post1 = Recipe(
        Post,
        category=categories[0],
        tags=[tags[0]],
        date='2020-01-01',
        time_of_day=TIME_OF_DAY['MORNING'],
        location='location1',
    ).make()

    post2 = Recipe(
        Post,
        category=categories[1],
        tags=[tags[0], tags[1]],
        date='2020-02-02',
        time_of_day=TIME_OF_DAY['AFTERNOON'],
        location='seoul',
    ).make()

    post3 = Recipe(
        Post,
        category=categories[0],
        tags=[tags[0], tags[1], tags[2]],
        date='2020-03-03',
        time_of_day=TIME_OF_DAY['AFTERNOON'],
        location='test_location3',
    ).make()

    return [post1, post2, post3]


class TestPostFiltering:
    pytestmark = pytest.mark.django_db

    def __count_tags_of(self, result, *title_filters):
        tags = [tag for tag in result['tags'] if tag['title'] in title_filters]
        return len(tags)

    def test_post_on_category_filtering(self, api_client, posts, categories):
        category_title = categories[0].title
        response = api_client.get(f'/posts?category={category_title}')
        assert response.status_code == 200
        assert len(response.data) == 2

        ids = set()
        for data in response.data:
            ids.add(data['id'])
            assert data['category']['title'] == category_title
        assert len(ids) == len(response.data)

    def test_post_on_tag_filtering(self, api_client, posts, tags):
        tag_title = tags[1].title
        response = api_client.get(f'/posts?tags={tag_title}')
        assert response.status_code == 200
        assert len(response.data) == 2

        ids = set()
        for result in response.data:
            ids.add(result['id'])
            number_of_tags = self.__count_tags_of(result, tag_title)
            assert number_of_tags == 1
        assert len(ids) == len(response.data)

        # Filter the posts by more than one tag.
        tag_title1, tag_title2 = tags[0].title, tags[1].title
        response = api_client.get(f'/posts?tags={tag_title1},{tag_title2}')
        assert response.status_code == 200
        assert len(response.data) == 2

        ids = set()
        for result in response.data:
            ids.add(result['id'])
            number_of_tags = self.__count_tags_of(result, tag_title1, tag_title2)
            assert number_of_tags == 2
        assert len(ids) == len(response.data)

        # This type of tag filtering is not supported.
        response = api_client.get(f'/posts?tags={tag_title1}&tags={tag_title2}')
        assert response.status_code == 400

    def test_post_on_category_tag_filtering(self, api_client, posts, categories, tags):
        category_title, tag_title = categories[0].title, tags[1].title
        response = api_client.get(f'/posts?category={category_title}&tags={tag_title}')
        assert response.status_code == 200
        assert len(response.data) == 1

        result = response.data[0]
        assert category_title == result['category']['title']

        number_of_tags = self.__count_tags_of(result, tag_title)
        assert number_of_tags == 1

    def test_post_on_date_filtering(self, api_client, posts):
        start_date, end_date = '2020-01-01', '2020-02-02'
        response = api_client.get(f'/posts?startDate={start_date}&endDate={end_date}')
        assert response.status_code == 200
        assert len(response.data) == 2

        for result in response.data:
            assert result['date'] >= start_date and result['date'] <= end_date

    def test_post_on_time_of_day_filtering(self, api_client, posts):
        time_of_day = TIME_OF_DAY['AFTERNOON']
        response = api_client.get(f'/posts?timeOfDay={time_of_day}')
        assert response.status_code == 200
        assert len(response.data) == 2

        for result in response.data:
            assert result.get('timeOfDay') == time_of_day

    def test_post_on_location_filtering(self, api_client, posts):
        location = 'location'
        response = api_client.get(f'/posts?location={location}')
        assert response.status_code == 200
        assert len(response.data) == 2

        for result in response.data:
            assert location in result['location']
