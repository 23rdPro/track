from django.urls import path
from . import views


urlpatterns = [
    path('', views.PublicationListView.as_view(), name='list'),
    path('<uuid:id>/', views.PublicationDetailView.as_view(), name='detail'),
    path('<uuid:id>/delete', views.PublicationDeleteView.as_view(), name='delete'),
    path('publish/', views.PublicationCreateView.as_view(), name='publish'),
]
