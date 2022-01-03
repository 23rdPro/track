# flake8: noqa

from django.urls import path
from . import views


urlpatterns = [
    path('', views.PublicationListView.as_view(), name='list'),
    path('<str:id>/', views.PublicationDetailView.as_view(), name='detail'),
]
