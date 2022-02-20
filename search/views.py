import fitz
from celery import group, shared_task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from field.tasks import BaseRetryTask
from guide.models import AdvancedGuide, BasicGuide
from publication.models import Publication


def search_pdf(query: str) -> list:
    job = group(_search.si(p.id, query) for p in Publication.objects.all())
    return job.apply_async().get()


@shared_task(base=BaseRetryTask)
def _search(hi_d: str, query: str) -> str or None:
    publication = Publication.objects.get(id=hi_d)
    doc = fitz.open(publication.upload_pdf.path)
    for page in doc:
        text = page.get_text().lower()
        if query.lower() in text:
            doc.close()
            return publication.id
    else:
        doc.close()
        return None


class PublicationSearchView(TemplateView):
    template_name = 'search/publication.html'

    def post(self, request, **kwargs):
        query = request.POST.get('query')
        if query:
            id_s = [k for k in search_pdf(query) if k]
            pdfs = Publication.objects.filter(id__in=id_s)
            qs = Publication.objects.annotate(
                search=SearchVector('title', 'description')).filter(search=query)
            context = {'queryset': qs | pdfs}
            return render(request, self.template_name, context)
        else:
            return HttpResponse(
                "You didn't provide search key, please do that then hit return")


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search/result.html'

    def post(self, request, **kwargs):
        query = request.POST.get('query')
        if query:
            id_s = [k for k in search_pdf(query) if k]
            u = request.user
            pdfs = Publication.objects.filter(id__in=id_s)
            pubs = Publication.objects.annotate(
                search=SearchVector('title', 'description')).filter(search=query)

            a_articles = AdvancedGuide.objects.filter(
                article_adv__guide_article__field_guide__dashboard_field__user=u).annotate(
                search=SearchVector('title', 'description')).filter(search=query)
            b_articles = BasicGuide.objects.filter(
                article_basic__guide_article__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)

            a_pdfs = AdvancedGuide.objects.filter(
                pdf_adv__guide_pdf__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)
            b_pdfs = BasicGuide.objects.filter(
                pdf_basic__guide_pdf__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)

            a_classes = AdvancedGuide.objects.filter(
                klass_adv__guide_klass__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)
            b_classes = BasicGuide.objects.filter(
                klass_basic__guide_klass__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)

            a_videos = AdvancedGuide.objects.filter(
                video_adv__guide_video__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)
            b_videos = BasicGuide.objects.filter(
                video_basic__guide_video__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)

            a_questions = AdvancedGuide.objects.filter(
                question_adv__guide_question__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)
            b_questions = BasicGuide.objects.filter(
                question_basic__guide_question__field_guide__dashboard_field__user=u
            ).annotate(search=SearchVector('title', 'description')).filter(search=query)

            publications = pdfs | pubs
            advanced_guides = a_articles | a_videos | a_classes | a_pdfs | a_questions
            basic_guides = b_articles | b_classes | b_pdfs | b_questions | b_videos
            context = {'publications': publications, 'advanced_guides': advanced_guides,
                       'basic_guides': basic_guides}
            if any([publications, advanced_guides, basic_guides]):
                context['items'] = True
            print(context)
            return render(request, self.template_name, context)
        else:
            return HttpResponse(
                "You didn't provide search key, please do that then hit return")
