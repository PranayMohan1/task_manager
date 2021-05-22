from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
    PermissionsMixin
from ..base.models import TimeStampedModel
from django.contrib.auth.models import UserManager
from django.conf import settings
from django.utils.translation import ugettext_lazy as ul
import binascii, os

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    username = models.CharField(max_length=128, blank=True, null=True, default='', unique=True)
    mobile = models.CharField(max_length=128, blank=True, null=True, default='')
    email = models.EmailField(max_length=256, null=True, blank=True, default='')
    first_name = models.CharField(max_length=1024, blank=True, null=True)
    last_name = models.CharField(max_length=1024, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    # Mobile number to be used as the username
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        """Returns the mobile no. of the User when it is printed in the console"""
        return self.mobile


class AuthTokenModel(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(ul("Key"), max_length=40, primary_key=True)
    created = models.DateTimeField(ul("Created"), auto_now_add=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='auth_token_model_user',
        on_delete=models.CASCADE, verbose_name=ul("User"), default=None
    )
    last_accessed = models.DateTimeField(ul("LastAccessed"), auto_now_add=True)

    class Meta:
        verbose_name = ul("Token")
        verbose_name_plural = ul("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(AuthTokenModel, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key