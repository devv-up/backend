from django.db import models


# Create your models here.
class Poll(models.Model):
    Name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.Name
