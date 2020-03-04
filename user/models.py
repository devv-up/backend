from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from typing import Any


class UserManager(BaseUserManager["User"]):
    def create_user(self, email: str, first_name: str, last_name: str,
                    password: str = None, commit: bool = True) -> Any:
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self.db)
        return user

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str) -> Any:
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    verification = models.BooleanField(null=False, default=False)
    verification_key = models.CharField(max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self) -> str:
        full_name = '%s%s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.get_full_name()

    def has_perm(self, perm: Any, obj: Any = None) -> bool:

        return True

    def has_module_perms(self, app_label: Any) -> bool:

        return True


class Photo(models.Model):
    photo_name = models.CharField(max_length=255)
    photo_info = models.IntegerField(null=True)

    def __str__(self) -> str:
        return self.photo_name
