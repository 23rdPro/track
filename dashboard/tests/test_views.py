import pytest
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse, resolve
from django.test import Client, RequestFactory

from dashboard import views
from dashboard.factories import DashboardFactory
from dashboard.forms import AddDashboardFieldForm
from dashboard.views import DashboardListView
from users.factories import UserFactory


@pytest.mark.django_db
class TestDashboardListView:

    def test_valid_attributes(self):
        assert views.DashboardListView
        view = DashboardListView
        assert view.paginate_by == 10
        assert view.context_object_name == 'dashboards'
        assert view.template_name == 'dashboard/list.html'

    def test_view_with_rfactory(self):
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        assert resolve(request.path).view_name == 'dashboard:list'

    def test_view_with_client(self):
        user = UserFactory()
        client = Client()
        response = client.get('/dashboard/')
        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/dashboard/"
        response = client.post(response.url, {
            'username': user.username,
            'password': user.password
        })
        assert response.status_code == 200
        # todo test template used
        client.force_login(user)
        response = client.get('/dashboard/')
        # assert response.context['dashboard_field_form'] == AddDashboardFieldForm
        # todo unbound form
        assert response.status_code == 200
        assert isinstance(response.content, bytes)




class TestAddDashboardFormView:
    pass