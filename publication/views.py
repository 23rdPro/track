from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from publication.forms import AddPublicationForm
from publication.models import Publication


class PublicationListView(ListView):
    context_object_name = 'publications'
    paginate_by = 25

    def get_queryset(self):
        qs = Publication.objects.exclude(title__isnull=True).exclude(description__isnull=True)
        return qs

    def get_template_names(self):
        if self.get_queryset():
            return 'publication/list.html'
        return 'publication_alert.html'


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publication/detail.html'
    context_object_name = 'publication'
    pk_url_kwarg = 'id'

    def render_to_response(self, context, **response_kwargs):
        return FileResponse(self.object.upload_pdf)


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    form_class = AddPublicationForm
    success_url = reverse_lazy('publication:list')
    template_name = 'publication/create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super(PublicationCreateView, self).form_valid(form)


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Publication
    success_url = reverse_lazy('publication:list')
    context_object_name = 'publication'
    pk_url_kwarg = 'id'
