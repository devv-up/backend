from typing import List

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
def title() -> str:
    return 'test_title'


@pytest.fixture
def title_data(title) -> dict:
    return {'title': title}


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
