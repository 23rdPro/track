import json
import logging
from abc import ABC
from itertools import chain

import celery
from celery import shared_task
from googleapiclient.discovery import build

from dashboard.models import Dashboard
from field.models import Field
from guide.models import BasicGuide, AdvancedGuide, Article, PDF, Klass, Video, Question
from helpers.functions import get_text
from track.settings import env

cx_key = env('CX_KEY')
cse_key = env('CSE_KEY')
logger = logging.getLogger(__name__)


class BaseRetryTask(celery.Task, ABC):
    autoretry_for = (Exception, )
    retry_backoff = True
    retry_jitter = True
    retry_kwargs = {'max_retries': 5, 'countdown': 5}


@shared_task(bind=True, base=BaseRetryTask)
def basic_guide(self, a_pk: int, p_pk: int, c_pk: int, v_pk: int, q_pk: int, f_pk: int, d_pk: int) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    stats, _ = get_text(field.field, field.aoc)
    dd = Dashboard.objects.get(pk=d_pk)
    link_set = [
        dd.field.guide.article.basic.values_list, dd.field.guide.pdf.basic.values_list,
        dd.field.guide.klass.basic.values_list, dd.field.guide.video.basic.values_list,
        dd.field.guide.question.basic.values_list, dd.field.guide.article.advanced.values_list,
        dd.field.guide.pdf.advanced.values_list, dd.field.guide.klass.advanced.values_list,
        dd.field.guide.video.advanced.values_list, dd.field.guide.question.advanced.values_list]

    # order => article, pdf, class, video, question => 5
    articles = json.loads(json.dumps(service.cse().list(
        q=stats[0], cx=cx_key).execute()))['items']  # 10 dict items
    article_objects = BasicGuide.objects.bulk_create([BasicGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in articles if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    article = Article.objects.get(pk=a_pk)
    article.basic.add(*article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=stats[1], cx=cx_key).execute()))['items']
    pdf_objects = BasicGuide.objects.bulk_create([BasicGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in pdfs if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    pdf = PDF.objects.get(pk=p_pk)
    pdf.basic.add(*pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=stats[2], cx=cx_key).execute()))['items']
    class_objects = BasicGuide.objects.bulk_create([BasicGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in classes if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    klass = Klass.objects.get(pk=c_pk)
    klass.basic.add(*class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=stats[3], cx=cx_key).execute()))['items']
    video_objects = BasicGuide.objects.bulk_create([BasicGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in videos if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    video = Video.objects.get(pk=v_pk)
    video.basic.add(*video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=stats[4], cx=cx_key).execute()))['items']
    question_objects = BasicGuide.objects.bulk_create([BasicGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in questions if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    question = Question.objects.get(pk=q_pk)
    question.basic.add(*question_objects)
    return


@shared_task(bind=True, base=BaseRetryTask)
def advanced_guide(self, a_pk: int, p_pk: int, c_pk: int, v_pk: int, q_pk: int, f_pk: int, d_pk: int) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    _, advs = get_text(field.field, field.aoc)
    dd = Dashboard.objects.get(pk=d_pk)
    link_set = [
        dd.field.guide.article.basic.values_list, dd.field.guide.pdf.basic.values_list,
        dd.field.guide.klass.basic.values_list, dd.field.guide.video.basic.values_list,
        dd.field.guide.question.basic.values_list, dd.field.guide.article.advanced.values_list,
        dd.field.guide.pdf.advanced.values_list, dd.field.guide.klass.advanced.values_list,
        dd.field.guide.video.advanced.values_list, dd.field.guide.question.advanced.values_list]

    articles = json.loads(json.dumps(service.cse().list(
        q=advs[0], cx=cx_key).execute()))['items']
    article_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in articles if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    article = Article.objects.get(pk=a_pk)
    article.advanced.add(*article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=advs[1], cx=cx_key).execute()))['items']
    pdf_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in pdfs if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    pdf = PDF.objects.get(pk=p_pk)
    pdf.advanced.add(*pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=advs[2], cx=cx_key).execute()))['items']
    class_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in classes if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    klass = Klass.objects.get(pk=c_pk)
    klass.advanced.add(*class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=advs[3], cx=cx_key).execute()))['items']
    video_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in videos if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    video = Video.objects.get(pk=v_pk)
    video.advanced.add(*video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=advs[4], cx=cx_key).execute()))['items']
    question_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=items['title'], link=items['link'], description=items['snippet']
    ) for items in questions if items['link'] not in list(chain(*(f('link', flat=True) for f in link_set)))])
    question = Question.objects.get(pk=q_pk)
    question.advanced.add(*question_objects)
    return
