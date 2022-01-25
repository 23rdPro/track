from django.urls import path
from . import views


urlpatterns = [
    path('', views.DashboardView.as_view(), name='list'),
    path('<int:pk>/', views.DashboardDetailView.as_view(), name='detail'),

]
