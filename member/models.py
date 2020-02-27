from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        elif not username:
            raise ValueError('유저네임은 필수입니다.')
        elif not password:
            raise ValueError('비밀번호는 필수입니다.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class Member(AbstractUser):
    verification = models.BooleanField(default=False)
    verification_key = models.CharField(max_length=256, null=True)

    bookmarks = models.ManyToManyField('meeting_board.Board', blank=True)

    objects = MyUserManager()

    def __str__(self):
        return self.username


class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    photo_info = models.IntegerField(null=True)

    def __str__(self):
        return self.photo_name
