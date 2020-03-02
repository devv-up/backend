import pytest

from user.models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('hugebigdream@gmail.com', "choi", "taehoon", "1111")
    assert User.objects.count() == 1
