# flake8: noqa

from django.http import FileResponse
from django.views.generic import ListView, DetailView

from publication.models import Publication


class PublicationListView(ListView):
    model = Publication
    context_object_name = 'publications'
    paginate_by = 10
    template_name = 'publication/list.html'


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publication/detail.html'
    context_object_name = 'publication'

    def render_to_response(self, context, **response_kwargs):
        return FileResponse(self.object.upload_pdf)
