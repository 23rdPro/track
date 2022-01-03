# flake8: noqa

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from dashboard import views as d_views
from field import views as f_views
from frontend.views import index
from users import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'fields', f_views.FieldRESTView)
router.register(r'dashboard', d_views.DashboardRESTView,
                basename='dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include((
        'publication.urls', 'publication'), namespace='publication'
    )),
    path('dashboard/', include((
        'dashboard.urls', 'dashboard'), namespace='dashboard'
    )),
    # path('', include(('frontend.urls', 'frontend'), namespace='frontend')),
    # path('', index, name='index'),

    # api routes
    path('api/', include(router.urls)),
    path('api-auth/', include((
        'rest_framework.urls', 'rest_framework'),
        namespace='api_auth'
    )),

]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
