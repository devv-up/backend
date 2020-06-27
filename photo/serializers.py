from rest_framework import serializers

from .models import photo


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = photo
        fields = ('__all__')
