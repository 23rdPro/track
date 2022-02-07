import json
from itertools import chain

from celery import shared_task
from googleapiclient.discovery import build

from dashboard.models import Dashboard
from field.models import Field
from guide.models import (
    StarterGuide,
    IntermediateGuide,
    AdvancedGuide,
    Article,
    PDF,
    Klass,
    Video,
    Question
)
from helpers.functions import get_text
from track.settings import env

cx_key = env('CX_KEY')
cse_key = env('CSE_KEY')


@shared_task
def starter(a_pk: int, p_pk: int, c_pk: int, v_pk: int, q_pk: int, f_pk: int, d_pk: int) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    stats, _, _ = [texts for texts in get_text(field.field, field.aoc)]
    dd = Dashboard.objects.get(pk=d_pk)
    link_set = [
        dd.field.guide.article.starter.values_list, dd.field.guide.pdf.starter.values_list,
        dd.field.guide.klass.starter.values_list, dd.field.guide.video.starter.values_list,
        dd.field.guide.question.starter.values_list, dd.field.guide.article.intermediate.values_list,
        dd.field.guide.pdf.intermediate.values_list, dd.field.guide.klass.intermediate.values_list,
        dd.field.guide.video.intermediate.values_list, dd.field.guide.question.intermediate.values_list,
        dd.field.guide.article.advanced.values_list, dd.field.guide.pdf.advanced.values_list,
        dd.field.guide.klass.advanced.values_list, dd.field.guide.video.advanced.values_list,
        dd.field.guide.question.advanced.values_list]

    # order => article, pdf, class, video, question => 5
    articles = json.loads(json.dumps(service.cse().list(
        q=stats[0], cx=cx_key).execute()))['items']  # 10 dict items
    article_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in articles if items['link'] not in (f('link', flat=True) for f in link_set)])
    article = Article.objects.get(pk=a_pk)
    article.starter.add(*article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=stats[1], cx=cx_key).execute()))['items']
    pdf_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in pdfs if items['link'] not in (f('link', flat=True) for f in link_set)])
    pdf = PDF.objects.get(pk=p_pk)
    pdf.starter.add(*pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=stats[2], cx=cx_key).execute()))['items']
    class_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in classes if items['link'] not in (f('link', flat=True) for f in link_set)])
    klass = Klass.objects.get(pk=c_pk)
    klass.starter.add(*class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=stats[3], cx=cx_key).execute()))['items']
    video_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in videos if items['link'] not in (f('link', flat=True) for f in link_set)])
    video = Video.objects.get(pk=v_pk)
    video.starter.add(*video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=stats[4], cx=cx_key).execute()))['items']
    question_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in questions if items['link'] not in (f('link', flat=True) for f in link_set)])
    question = Question.objects.get(pk=q_pk)
    question.starter.add(*question_objects)
    return


@shared_task
def intermediate(a_pk: int, p_pk: int, c_pk: int, v_pk: int, q_pk: int, f_pk: int, d_pk: int) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    _, ints, _ = [texts for texts in get_text(field.field, field.aoc)]
    dd = Dashboard.objects.get(pk=d_pk)
    link_set = [
        dd.field.guide.article.starter.values_list, dd.field.guide.pdf.starter.values_list,
        dd.field.guide.klass.starter.values_list, dd.field.guide.video.starter.values_list,
        dd.field.guide.question.starter.values_list, dd.field.guide.article.intermediate.values_list,
        dd.field.guide.pdf.intermediate.values_list, dd.field.guide.klass.intermediate.values_list,
        dd.field.guide.video.intermediate.values_list, dd.field.guide.question.intermediate.values_list,
        dd.field.guide.article.advanced.values_list, dd.field.guide.pdf.advanced.values_list,
        dd.field.guide.klass.advanced.values_list, dd.field.guide.video.advanced.values_list,
        dd.field.guide.question.advanced.values_list]
    articles = json.loads(json.dumps(service.cse().list(
        q=ints[0], cx=cx_key).execute()))['items']
    article_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in articles if items['link'] not in (f('link', flat=True) for f in link_set)])
    article = Article.objects.get(pk=a_pk)
    article.intermediate.add(*article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=ints[1], cx=cx_key).execute()))['items']
    pdf_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in pdfs if items['link'] not in (f('link', flat=True) for f in link_set)])
    pdf = PDF.objects.get(pk=p_pk)
    pdf.intermediate.add(*pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=ints[2], cx=cx_key).execute()))['items']
    class_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in classes if items['link'] not in (f('link', flat=True) for f in link_set)])
    klass = Klass.objects.get(pk=c_pk)
    klass.intermediate.add(*class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=ints[3], cx=cx_key).execute()))['items']
    video_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in videos if items['link'] not in (f('link', flat=True) for f in link_set)])
    video = Video.objects.get(pk=v_pk)
    video.intermediate.add(*video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=ints[4], cx=cx_key).execute()))['items']
    question_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in questions if items['link'] not in (f('link', flat=True) for f in link_set)])
    question = Question.objects.get(pk=q_pk)
    question.intermediate.add(*question_objects)
    return


@shared_task
def advance(a_pk: int, p_pk: int, c_pk: int, v_pk: int, q_pk: int, f_pk: int, d_pk: int) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    _, _, advs = [texts for texts in get_text(field.field, field.aoc)]
    dd = Dashboard.objects.get(pk=d_pk)
    link_set = [
        dd.field.guide.article.starter.values_list, dd.field.guide.pdf.starter.values_list,
        dd.field.guide.klass.starter.values_list, dd.field.guide.video.starter.values_list,
        dd.field.guide.question.starter.values_list, dd.field.guide.article.intermediate.values_list,
        dd.field.guide.pdf.intermediate.values_list, dd.field.guide.klass.intermediate.values_list,
        dd.field.guide.video.intermediate.values_list, dd.field.guide.question.intermediate.values_list,
        dd.field.guide.article.advanced.values_list, dd.field.guide.pdf.advanced.values_list,
        dd.field.guide.klass.advanced.values_list, dd.field.guide.video.advanced.values_list,
        dd.field.guide.question.advanced.values_list]

    articles = json.loads(json.dumps(service.cse().list(
        q=advs[0], cx=cx_key).execute()))['items']
    article_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in articles if items['link'] not in (f('link', flat=True) for f in link_set)])
    article = Article.objects.get(pk=a_pk)
    article.advanced.add(*article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=advs[1], cx=cx_key).execute()))['items']
    pdf_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in pdfs if items['link'] not in (f('link', flat=True) for f in link_set)])
    pdf = PDF.objects.get(pk=p_pk)
    pdf.advanced.add(*pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=advs[2], cx=cx_key).execute()))['items']
    class_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in classes if items['link'] not in (f('link', flat=True) for f in link_set)])
    klass = Klass.objects.get(pk=c_pk)
    klass.advanced.add(*class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=advs[3], cx=cx_key).execute()))['items']
    video_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in videos if items['link'] not in (f('link', flat=True) for f in link_set)])
    video = Video.objects.get(pk=v_pk)
    video.advanced.add(*video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=advs[4], cx=cx_key).execute()))['items']
    question_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in questions if items['link'] not in (f('link', flat=True) for f in link_set)])
    question = Question.objects.get(pk=q_pk)
    question.advanced.add(*question_objects)
    return


parallels = [starter, intermediate, advance]
