# flake8: noqa

import pytest
from django.urls import resolve
from django.test import Client, RequestFactory
from dashboard import views
from dashboard.forms import AddDashboardFieldForm
from dashboard.models import Dashboard
from dashboard.views import DashboardListView, AddDashboardFormView
from users.factories import UserFactory


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

        response = client.post('/dashboard/', {
            'keyword': 'bone medicine',
            'aoc': 'surgery'
        })
        assert response.status_code == 302
        assert Dashboard.objects.count() == 1
        queryset = Dashboard.objects.filter(publication__author=user)
        obj = queryset.get()
        assert obj.publication.first().author == user
        assert obj.field.first().field == 'bone medicine'
        assert obj.field.first().aoc == 'surgery'

    def test_view_with_rfactory(self):
        pass


if __name__ == '__main__':
    pytest.main()
