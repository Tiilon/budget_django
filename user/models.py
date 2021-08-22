from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def create_user(self, email,first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        user = self.model(
            email = email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self,email, first_name, last_name, password):
        user = self.create_user(email=email,first_name=first_name,last_name=last_name,password=password)

        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.username = f"{first_name} {last_name}"
        user.save(using=self.db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True, blank=True, null=True)
    is_superuser = models.BooleanField(default=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'user'
        ordering = ('-first_name',)

    def __str__(self):
        return f"{self.get_full_name()}"



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)

