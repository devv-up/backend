from rest_framework import serializers

from user.models import User

from .category import *  # noqa 401
from .comment import *  # noqa 401
from .post import *  # noqa 401
from .tag import *  # noqa 401


class TempUserSerializer(serializers.ModelSerializer):
    """
    This class will be used until the UserSerializer from
    the user app is created.
    """
    class Meta:
        model = User
        fields = '__all__'
