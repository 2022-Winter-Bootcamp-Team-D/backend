from waiting.models import Waiting
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from datetime import datetime


class Token(models.Model):
    # token_id = models.BigAutoField()
    token = models.CharField(max_length=200)
    waiting_id = models.ForeignKey(Waiting, primary_key=True, on_delete=models.CASCADE, db_column='token_id')

    class Meta:
        db_table = 'token'


class UserManager(BaseUserManager):
    """
    Custom users model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        # users.set_is_staff(False)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
