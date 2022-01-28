from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import reverse


class UserAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated and not user.name:
            return reverse('users:complete_signup', kwargs={
                'id': request.user.id
            })
        return resolve_url(settings.LOGIN_REDIRECT_URL)
