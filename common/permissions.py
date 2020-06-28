from rest_framework.exceptions import PermissionDenied

from post.models import Modifiable
from user.models import User


def check_permission(user: User, model: Modifiable) -> None:
    if model.author is None:
        return None

    if model.author.id != user.id:
        raise PermissionDenied({'detail': 'Permission Denied.'})
