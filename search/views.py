import fitz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from guide.models import AdvancedGuide, BasicGuide
from publication.models import Publication


def search_pdf(query):
    publications = []
    for pub in Publication.objects.all():
        doc = fitz.open(pub.upload_pdf.path)
        for page in doc:
            text = page.get_text().lower()
            if query.lower() in text:
                publications.append(pub.id)
                break
        doc.close()
    return publications


class PublicationSearchView(TemplateView):
    template_name = 'search/publication.html'

    def post(self, request, **kwargs):
        query = request.POST.get('query')
        if query:
            pdfs = Publication.objects.filter(id__in=search_pdf(query))
            qs = Publication.objects.annotate(
                search=SearchVector('title', 'description')).filter(search=query)
            context = {'queryset': qs | pdfs}
            return render(request, self.template_name, context)
        else:
            return HttpResponse("You didn't provide search key, please do that then hit return")


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search/publication.html'

    def post(self, request, **kwargs):
        query = request.POST.get('query')
        if query:
            u = request.user
            pdfs = Publication.objects.filter(id__in=search_pdf(query))
            pubs = Publication.objects.annotate(
                search=SearchVector('title', 'description')).filter(search=query)
            a_articles = AdvancedGuide.objects.filter(
                article_adv__guide_article__field_guide__dashboard_field__user=u).annotate(
                search=SearchVector('title', 'description')).filter(search=query)
            b_articles = BasicGuide.objects.filter(
                article_basic__guide_article__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)
            a_pdfs = AdvancedGuide.objects

