from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import authentication
from rest_framework.authtoken.models import Token


class CustomUserAccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, fullname, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, fullname, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, fullname, **extra_fields)


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    fullname = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserAccountManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BearerAuthentication(authentication.TokenAuthentication):
    """
   Simple token based authentication.

   Clients should authenticate by passing the token key in the "Authorization"
   HTTP header, prepended with the string "Token ".  For example:

       Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
   """
    keyword = 'Bearer'


