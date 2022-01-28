from rest_framework import viewsets

from dashboard.api.serializers import DashboardSerializer
from dashboard.models import Dashboard


class DashboardRESTView(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()  # get_queryset
