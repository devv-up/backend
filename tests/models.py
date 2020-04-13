from django.db import models


class TestModel(models.Model):
    test_str = models.CharField(max_length=50)
    test_int = models.IntegerField()
    test_date = models.DateField()
