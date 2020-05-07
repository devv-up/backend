from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    This class will be used until the UserSerializer from
    the user app is created.
    """
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}
