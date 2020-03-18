from typing import List

from model_bakery import baker
import pytest
from rest_framework.test import APIClient

from post.models import Category, Comment, Post, Tag
from user.models import User


@pytest.fixture
def api_client():
    api_client = APIClient()
    return api_client


@pytest.fixture
def dummy_id() -> int:
    return 1


@pytest.fixture
def title_data() -> dict:
    return {'title': 'test_title'}


@pytest.fixture
def content_data() -> dict:
    return {'content': 'test_content'}


@pytest.fixture
def unauthorised_data() -> dict:
    return {'id': 65535, 'author': 65535}


@pytest.fixture
def post_data() -> dict:
    return {
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


@pytest.fixture
def post_preset_data(users, categories, tags, post_data):
    post1_data = {
        **post_data,
        'author': users[0].id,
        'category': categories[0].id,
        'tags': [tags[0].id]
    }
    post2_data = {
        **post_data,
        'author': users[1].id,
        'category': categories[1].id,
        'tags': [tags[0].id, tags[1].id]
    }
    post3_data = {
        **post_data,
        'author': users[1].id,
        'category': categories[0].id,
        'tags': [tags[0].id, tags[1].id, tags[2].id]
    }
    return [post1_data, post2_data, post3_data]


@pytest.fixture
def bad_post_data() -> dict:
    return {
        'title': 'test_title',
        # 'content': 'test_content',
        'location': 'test_location',
        'capacity': 10,
        # 'date': '2020-01-01',
        'timeOfDay': 1,
        'author': 1,
        # 'category': 1,
        # 'tags': [1, 2],
    }


@pytest.fixture
def comment_data() -> dict:
    return {
        'content': 'test_content',
        'post': 1,
        'author': 1,
    }


@pytest.fixture
def bad_comment_data() -> dict:
    return {
        # 'content': 'test_content',
        'post': 1,
        # 'author': 1,
    }


@pytest.fixture
def time_of_day() -> dict:
    return {
        'MORNING': 0,
        'DAY': 1,
        'NIGHT': 2,
    }


@pytest.fixture
def users() -> List[User]:
    return baker.make(User, _quantity=3)


@pytest.fixture
def categories() -> List[Category]:
    return baker.make(Category, _quantity=3)


@pytest.fixture
def tags() -> List[Tag]:
    return baker.make(Tag, _quantity=3)


@pytest.fixture
def posts() -> List[Post]:
    return baker.make(Post, _quantity=3)


@pytest.fixture
def comments() -> List[Comment]:
    return baker.make(Comment, _quantity=3)
