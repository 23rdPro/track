from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    FormView,
    DetailView,
)
from django.views.generic.edit import FormMixin

from dashboard.forms import (
    AddDashboardFieldForm,
    CreateDashboardPublicationForm
)
from dashboard.models import Dashboard
from dashboard.serializers import DashboardSerializer
from field.models import Field
from guide.models import Guide
from publication.models import Publication
from rest_framework import viewsets


class DashboardListView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/list.html'
    context_object_name = 'dashboards'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        return Dashboard.objects.filter(
            publication__author=user).select_related('field')

    def get_context_data(self, **kwargs):
        context = super(DashboardListView,
                        self).get_context_data(**kwargs)
        context['dashboard_field_form'] = AddDashboardFieldForm()  # +add form
        context['guide_attributes'] = ['Articles', 'PDFs', 'Online Classes', 'Videos', 'Questions']
        context['level_attributes'] = ['starter', 'intermediate', 'advanced']
        return context


class AddDashboardFormView(LoginRequiredMixin, FormView):
    template_name = 'dashboard/list.html'
    form_class = AddDashboardFieldForm
    pk = None

    def get_context_data(self, **kwargs):
        return super(AddDashboardFormView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        publication = Publication()
        publication.author = user
        publication.save()

        guide = Guide().save()
        key = form.cleaned_data['keyword']
        qualify_key = form.cleaned_data['aoc']
        field = Field(field=key, aoc=qualify_key)
        field.guide = guide
        field.save()

        dashboard = Dashboard()
        dashboard.field = field
        dashboard.publication.add(publication)
        dashboard.save()
        self.pk = dashboard.pk
        return super(AddDashboardFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:detail', kwargs={'pk': self.pk})


class DashboardView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = DashboardListView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AddDashboardFormView.as_view()
        return view(request, *args, **kwargs)


# rewrite into plain function to accommodate delete and any other update todo
class DashboardDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Dashboard
    template_name = 'dashboard/detail.html'
    context_object_name = 'dashboard'
    form_class = CreateDashboardPublicationForm
    object = None

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        context['dashboards'] = Dashboard.objects.filter(
            publication__author=self.request.user
        )  # other dashboards you could otherwise check
        return context

    def get_success_url(self):
        return reverse_lazy('dashboard:detail', kwargs={'pk': self.object.pk})

    def post(self, request, pk):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)  # todo

    def form_valid(self, form):
        self.object = self.get_object()
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        upload_pdf = form.cleaned_data['upload_pdf']
        publications = self.object.publication
        user = self.request.user

        # because publications is 1 twice- once when it was instantiated
        # with dashboard and an empty file, the other, when file is uploaded
        if publications.count() == 1:
            try:
                if publications.first().upload_pdf.path:
                    self.run_save(user, title, description, upload_pdf, self.object)
            except ValueError:
                publication = publications.first()  # has user
                publication.title = title
                publication.description = description
                publication.upload_pdf = upload_pdf
                publication.save()
        else:
            self.run_save(user, title, description, upload_pdf, self.object)

        return super(DashboardDetailView, self).form_valid(form)

    @staticmethod
    def run_save(user, title, description, upload_pdf, obj):
        publication = Publication(author=user)
        publication.title = title
        publication.description = description
        publication.upload_pdf = upload_pdf
        publication.save()
        # dashboard is instantiated with publication,
        # without this clause, an extra object is
        # floating- unused, thus publication is only added
        # here afterwards
        obj.publication.add(publication)


class DashboardRESTView(viewsets.ModelViewSet):
    serializer_class = DashboardSerializer
    queryset = Dashboard.objects.all()  # get_queryset
