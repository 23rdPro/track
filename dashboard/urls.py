from django.urls import path

from . import views


urlpatterns = [
    path('', views.DashboardListView.as_view(), name='list'),
]
