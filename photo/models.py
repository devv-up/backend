from django.db import models


# Create your models here.
class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    photo_info = models.IntegerField(null=True)
    image = models.ImageField(default='media/default_img.jpg')

    def __str__(self) -> str:
        return self.photo_name
