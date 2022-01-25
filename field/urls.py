from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateFieldView.as_view(), name='create'),
]
