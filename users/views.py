from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import UserUpdateAfterSignupForm
from users.models import User


class UserUpdateAfterSignupView(LoginRequiredMixin, UpdateView):
    model = User
    slug_field = 'id'
    slug_url_kwarg = 'id'
    form_class = UserUpdateAfterSignupForm
    template_name = 'account/user_update_after_signup.html'
    context_object_name = 'user'
    success_url = reverse_lazy('publication:list')
