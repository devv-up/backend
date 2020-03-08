from typing import Any

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    verification = models.BooleanField(null=False, default=False)
    verification_key = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.name

    def has_perm(self, perm: Any, obj: Any = None) -> bool:

        return True

    def has_module_perms(self, app_label: Any) -> bool:

        return True

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.objects = UserManager.get_instance()


class UserManager(BaseUserManager):  # type: ignore
    __instance = None

    @staticmethod
    def get_instance() -> Any:
        """ Static access method. """
        if UserManager.__instance is None:
            UserManager()
        return UserManager.__instance

    def __init__(self) -> None:
        """ Virtually private constructor. """
        if UserManager.__instance is not None:
            assert Exception("This class is a singleton!")
        else:
            UserManager.__instance = self

    def create_user(self, email: str, name: str,
                    password: str = None) -> 'User':
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email: str, name: str, password: str) -> 'User':
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user
