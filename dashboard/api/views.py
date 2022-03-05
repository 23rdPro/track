from rest_framework import viewsets

from dashboard.api.serializers import DashboardSerializer
from dashboard.models import Dashboard


class DashboardRESTView(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer

    def get_queryset(self):
        user = self.request.user
        return Dashboard.objects.filter(user=user).select_related('field')

