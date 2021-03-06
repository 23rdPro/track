import os

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from dashboard.api import views as dashboard_views
from field.api import views as field_views
from search.views import SearchView
from users.api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'fields', field_views.FieldRESTView)
router.register(r'dashboard', dashboard_views.DashboardRESTView, basename='dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('user/', include(('users.urls', 'users'), namespace='users')),
    path('field/', include(('field.urls', 'field'), namespace='field')),
    path('', include(('publication.urls', 'publication'), namespace='publication')),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('result/', SearchView.as_view(), name='search_track'),

    # api routes
    path('api/', include(router.urls)),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='api_auth')),

]

# todo if settings.DEBUG instead
if not os.environ.get('MEMCACHIER_PASSWORD') and not os.environ.get('MEMCACHIER_SERVERS') \
        and not os.environ.get('MEMCACHIER_USERNAME'):

    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
