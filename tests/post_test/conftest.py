import pytest
from rest_framework.test import APIClient

from post.models import Category, Tag


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
def categories(title) -> None:
    return Category.objects.bulk_create(
        [Category(title=f'{title} {i+1}')
            for i in range(3)]
    )


@pytest.fixture
def tags(title) -> None:
    return Tag.objects.bulk_create(
        [Tag(title=f'{title} {i+1}')
            for i in range(3)]
    )
