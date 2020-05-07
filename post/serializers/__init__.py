from rest_framework import serializers

from post.serializers.category import *  # noqa 401
from post.serializers.comment import *  # noqa 401
from post.serializers.post import *  # noqa 401
from post.serializers.tag import *  # noqa 401
from user.models import User


class TempUserSerializer(serializers.ModelSerializer):
    """
    This class will be used until the UserSerializer from
    the user app is created.
    """
    class Meta:
        model = User
        fields = '__all__'
