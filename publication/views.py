from django.http import FileResponse
from django.views.generic import ListView, DetailView

from publication.models import Publication


class PublicationListView(ListView):
    context_object_name = 'publications'
    paginate_by = 25
    template_name = 'publication/list.html'

    def get_queryset(self):
        return Publication.objects.exclude(title__isnull=True).exclude(
            description__isnull=True)


class PublicationDetailView(DetailView):
    model = Publication
    template_name = 'publication/detail.html'
    context_object_name = 'publication'
    pk_url_kwarg = 'id'

    def render_to_response(self, context, **response_kwargs):
        return FileResponse(self.object.upload_pdf)
