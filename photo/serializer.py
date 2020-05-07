from rest_framework import serializers

from photo.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Photo
        fields = ('photo_name', 'photo_info', 'image')
