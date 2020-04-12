from rest_framework import serializers

from user.models import User

from .category_serializers import *  # noqa 401
from .comment_serializers import *  # noqa 401
from .post_serializers import *  # noqa 401
from .tag_serializers import *  # noqa 401


class TempUserSerializer(serializers.ModelSerializer):
    """
    This class will be used until the UserSerializer from
    the user app is created.
    """
    class Meta:
        model = User
        fields = '__all__'
