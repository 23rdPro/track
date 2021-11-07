import pytest
from django.urls import reverse, resolve
from django.test import Client, RequestFactory
import dashboard
from dashboard import views
from dashboard.forms import AddDashboardFieldForm, CreateDashboardPublicationForm
from dashboard.models import Dashboard
from dashboard.views import DashboardListView, AddDashboardFormView, DashboardView
from users.factories import UserFactory
from users.models import User


@pytest.mark.django_db
class TestDashboardView:

    def test_valid_attributes(self):
        assert views.DashboardView
        assert views.DashboardListView
        assert views.AddDashboardFormView

        assert DashboardListView.paginate_by == 10
        assert DashboardListView.context_object_name == 'dashboards'
        assert DashboardListView.template_name == 'dashboard/list.html'

        assert AddDashboardFormView.form_class == AddDashboardFieldForm
        assert AddDashboardFormView.template_name == 'dashboard/list.html'
        assert not AddDashboardFormView.pk

        path = resolve('/dashboard/')
        assert path.view_name == 'dashboard:list'
        assert path.url_name == 'list'

    def test_view_with_client(self):
        client = Client()
        response = client.get('/dashboard/')
        assert response.url == '/accounts/login/?next=/dashboard/'
        assert response.status_code == 302

        user = UserFactory()
        client.force_login(user)

        response = client.get('/dashboard/')
        assert response.status_code == 200
        # todo test template used
        assert isinstance(response.content, bytes)  # :(
        assert response.context['dashboard_field_form']
        assert 'keyword' in response.context['dashboard_field_form'].fields
        assert 'aoc' in response.context['dashboard_field_form'].fields

    def test_view_with_rfactory(self):
        factory = RequestFactory()