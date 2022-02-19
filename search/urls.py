from django.urls import path

from . import views

urlpatterns = [
    path('', views.PublicationSearchView.as_view(), name='publication'),
]