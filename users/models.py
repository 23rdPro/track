import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from track.mixins import TimeStampMixin
from users.managers import UserManager


class BlackListedUsername(models.Model):
    username = models.CharField(max_length=37, unique=True, blank=False)
    objects = models.Manager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = "black_listed_usernames"


class User(TimeStampMixin, AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    email = models.EmailField(_('email address'), unique=True, max_length=255)
    username = models.CharField(_('username'), unique=True, max_length=37,
                                help_text='account unique moniker',
                                validators=[
                                    RegexValidator(
                                        regex="^[a-z0-9]*$",
                                        message="Username may only contain letters and numbers model",
                                        code="invalid_username"
                                    )
                                ])
    name = models.CharField(_('Full name'), max_length=128, help_text='full name')
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    is_active = models.BooleanField(_('active status'), default=True)

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_staff and self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_active and self.is_staff and self.is_superuser

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]
    objects = UserManager()

    class Meta:
        ordering = ['created_at', ]

    def clean(self):
        if self.name and len(str(self.name).split()) < 2:
            raise ValidationError(_('Please provide your full name'))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        instance = super(User, self).save(force_insert, force_update, *args, **kwargs)
        return instance

    def __str__(self):
        return self.get_username()

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
