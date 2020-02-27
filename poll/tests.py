
import pytest

from poll.models import Poll

# Create your tests here.


@pytest.mark.django_db
def test_poll() -> None:
    p = Poll.objects.create()
    p.Name = "tst"
    p.save()
