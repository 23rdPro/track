# flake8: noqa

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, username, password, **extras):
        # to avoid tight-coupling / circular dependency, memory leak,
        # infinite recursions
        from .models import User

        if not email and not username:
            raise ValueError(_('Email and Username are required'))
        email = self.normalize_email(email)
        user_model = User
        username = user_model.normalize_username(username)
        user = self.model(email=email, username=username, **extras)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extras):
        extras.setdefault('is_superuser', False)
        extras.setdefault('is_staff', False)
        extras.setdefault('is_active', True)

        if extras.get('is_superuser') is not False:
            raise ValueError('This action is not permitted')
        if extras.get('is_staff') is not False:
            raise ValueError('This action is not permitted')
        return self._create_user(email, username, password, **extras)

    def create_superuser(self, email, username, password, **extras):
        extras.setdefault('is_superuser', True)
        extras.setdefault('is_staff', True)
        extras.setdefault('is_active', True)

        if extras.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if extras.get('is_staff') is not True:
            raise ValueError(_('superuser must be is_staff=True.'))
        return self._create_user(email, username, password, **extras)