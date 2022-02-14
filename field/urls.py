from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateFieldView.as_view(), name='create'),
    path('records/', views.ListFieldView.as_view(), name='list'),
    path('<int:pk>/', views.UpdateFieldView.as_view(), name='edit'),

]
