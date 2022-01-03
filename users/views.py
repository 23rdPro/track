# flake8: noqa

from rest_framework import viewsets, permissions

from users.models import User
from users.serializers import UserSerializer


# REST
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-updated_at')
    serializer_class = UserSerializer
