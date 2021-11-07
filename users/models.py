from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, max_length=255,
                              help_text='user email address',
                              )
    username = models.CharField(_('username'), unique=True, max_length=37,
                                help_text='account unique moniker')
    name = models.CharField(_('Full name'), max_length=128, help_text='full name')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active status'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
    objects = UserManager()

    class Meta:
        ordering = ['created_at', ]

    def clean(self):
        if self.name and len(str(self.name).split()) < 2:
            raise ValidationError(_('Please provide your full name'))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        instance = super(User, self).save(
            force_insert, force_update, *args, **kwargs
        )
        return instance

    def __str__(self):
        return self.get_username()

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})