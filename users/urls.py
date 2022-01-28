from django.urls import path

from . import views


urlpatterns = [
    path('<uuid:id>/', views.UserUpdateAfterSignupView.as_view(), name='complete_signup'),
]

