from typing import Any, List

import pytest
from model_mommy import mommy
from rest_framework.test import APIClient

from post.models import Category, Post, Tag
from user.models import User


@pytest.fixture
def api_client():
    api_client = APIClient()
    return api_client


@pytest.fixture
def category_id() -> int:
    return 1


@pytest.fixture
def tag_id() -> int:
    return 1


@pytest.fixture
def post_id() -> int:
    return 1


@pytest.fixture
def title_data() -> dict:
    return {'title': 'test_title'}


@pytest.fixture
def bad_data() -> dict:
    return {'id': 1, 'author': 65535}


@pytest.fixture
def post_data() -> dict:
    data: dict[str, Any] = {
        'title': 'test_title',
        'content': 'test_content',
        'location': 'test_location',
        'capacity': 10,
        'date': '2020-01-01',
        'time_of_day': 1,
        'author': 1,
        'category': 1,
        'tags': [1, 2],
    }
    return data


@pytest.fixture
def users() -> List[User]:
    return [mommy.make(User) for i in range(3)]


@pytest.fixture
def categories() -> List[Category]:
    return [mommy.make(Category) for i in range(3)]


@pytest.fixture
def tags() -> List[Tag]:
    return [mommy.make(Tag) for i in range(3)]


@pytest.fixture
def posts() -> List[Post]:
    return [mommy.make(Post) for i in range(3)]
