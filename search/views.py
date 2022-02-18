import fitz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView


class PublicationSearchView(FormView):
    pass


class SearchView(LoginRequiredMixin, FormView):
    pass
