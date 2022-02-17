from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [
    path('', views.DashboardListView.as_view(), name='list'),
    # path('', cache_page(60*15, key_prefix='dashboard'), views.DashboardListView.as_view(), name='list'),

]
