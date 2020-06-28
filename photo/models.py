from django.db import models


# Create your models here.
class photo(models.Model):
    photo_category = models.CharField(max_length=30)
    photo_detail = models.CharField(max_length=30)
    # set default to anything or blank image
    image = models.ImageField(upload_to="images/%Y/%m/%d", default='images/None/no-img,jpg')

    def __str__(self) -> str:
        return f'Photo(category="{self.photo_category}", detail="{self.photo_detail}")'
