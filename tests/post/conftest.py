from typing import List

from model_bakery import baker
import pytest
from rest_framework.test import APIClient

from post.models import Category, Comment, Post, Tag
from user.models import User


@pytest.fixture
def api_client():
    return APIClient()


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
def many_posts() -> List[Post]:
    return baker.make(Post, _quantity=100)


@pytest.fixture
def comments() -> List[Comment]:
    return baker.make(Comment, _quantity=3)
