import json
import logging
from abc import ABC

import celery
from celery import shared_task
from googleapiclient.discovery import build

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


def get_article_guides(f_pk: int) -> tuple:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    bsc, adn = get_text(field.field, field.aoc)
    b_articles = json.loads(json.dumps(service.cse().list(
        q=bsc[0], cx=cx_key).execute()))['items']
    a_articles = json.loads(json.dumps(service.cse().list(
        q=adn[0], cx=cx_key).execute()))['items']
    return b_articles, a_articles


def get_pdf_guides(f_pk: int) -> tuple:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    bsc, adn = get_text(field.field, field.aoc)
    b_pdfs = json.loads(json.dumps(service.cse().list(
        q=bsc[1], cx=cx_key).execute()))['items']
    a_pdfs = json.loads(json.dumps(service.cse().list(
        q=adn[1], cx=cx_key).execute()))['items']
    return b_pdfs, a_pdfs


def get_klass_guides(f_pk: int) -> tuple:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    bsc, adn = get_text(field.field, field.aoc)
    b_classes = json.loads(json.dumps(service.cse().list(
        q=bsc[2], cx=cx_key).execute()))['items']
    a_classes = json.loads(json.dumps(service.cse().list(
        q=adn[2], cx=cx_key).execute()))['items']
    return b_classes, a_classes


def get_video_guides(f_pk: int) -> tuple:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    bsc, adn = get_text(field.field, field.aoc)
    b_videos = json.loads(json.dumps(service.cse().list(
        q=bsc[3], cx=cx_key).execute()))['items']
    a_videos = json.loads(json.dumps(service.cse().list(
        q=adn[3], cx=cx_key).execute()))['items']
    return b_videos, a_videos


def get_question_guides(f_pk: int) -> tuple:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(pk=f_pk)
    bsc, adn = get_text(field.field, field.aoc)
    b_questions = json.loads(json.dumps(service.cse().list(
        q=bsc[4], cx=cx_key).execute()))['items']
    a_questions = json.loads(json.dumps(service.cse().list(
        q=adn[4], cx=cx_key).execute()))['items']
    return b_questions, a_questions


@shared_task(bind=True, base=BaseRetryTask)
def create_article_objects(self, a_pk: int, f_pk: int, link_set: dict) -> None:
    b_articles, a_articles = get_article_guides(f_pk)
    article = Article.objects.get(pk=a_pk)
    b_objects = []
    for items in b_articles:
        if items['link'] not in link_set:
            o = BasicGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            b_objects.append(o)
            link_set[items['link']] = items['link']
    article.basic.add(*b_objects)
    a_objects = []
    for items in a_articles:
        if items['link'] not in link_set:
            o = AdvancedGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            a_objects.append(o)
            link_set[items['link']] = items['link']
    article.advanced.add(*a_objects)
    return


@shared_task(bind=True, base=BaseRetryTask)
def create_pdf_objects(self, p_pk: int, f_pk: int, link_set: dict) -> None:
    b_pdfs, a_pdfs = get_pdf_guides(f_pk)
    pdf = PDF.objects.get(pk=p_pk)
    b_objects = []
    for items in b_pdfs:
        if items['link'] not in link_set:
            o = BasicGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            b_objects.append(o)
            link_set[items['link']] = items['link']
    pdf.basic.add(*b_objects)
    a_objects = []
    for items in a_pdfs:
        if items['link'] not in link_set:
            o = AdvancedGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            a_objects.append(o)
            link_set[items['link']] = items['link']
    pdf.advanced.add(*a_objects)
    return


@shared_task(bind=True, base=BaseRetryTask)
def create_klass_objects(self, c_pk: int, f_pk: int, link_set: dict) -> None:
    b_classes, a_classes = get_klass_guides(f_pk)
    klass = Klass.objects.get(pk=c_pk)
    b_objects = []
    for items in b_classes:
        if items['link'] not in link_set:
            o = BasicGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            b_objects.append(o)
            link_set[items['link']] = items['link']
    klass.basic.add(*b_objects)
    a_objects = []
    for items in a_classes:
        if items['link'] not in link_set:
            o = AdvancedGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            a_objects.append(o)
            link_set[items['link']] = items['link']
    klass.advanced.add(*a_objects)
    return


@shared_task(bind=True, base=BaseRetryTask)
def create_video_objects(self, v_pk: int, f_pk: int, link_set: dict) -> None:
    b_videos, a_videos = get_video_guides(f_pk)
    video = Video.objects.get(pk=v_pk)
    b_objects = []
    for items in b_videos:
        if items['link'] not in link_set:
            o = BasicGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            b_objects.append(o)
            link_set[items['link']] = items['link']
    video.basic.add(*b_objects)
    a_objects = []
    for items in a_videos:
        if items['link'] not in link_set:
            o = AdvancedGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            a_objects.append(o)
            link_set[items['link']] = items['link']
    video.advanced.add(*a_objects)
    return


@shared_task(bind=True, base=BaseRetryTask)
def create_question_objects(self, q_pk: int, f_pk: int, link_set: dict) -> None:
    b_questions, a_questions = get_question_guides(f_pk)
    question = Question.objects.get(pk=q_pk)
    b_objects = []
    for items in b_questions:
        if items['link'] not in link_set:
            o = BasicGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            b_objects.append(o)
            link_set[items['link']] = items['link']
    question.basic.add(*b_objects)
    a_objects = []
    for items in a_questions:
        if items['link'] not in link_set:
            o = AdvancedGuide.objects.create(
                title=items['title'], link=items['link'], description=items['snippet']
            )
            a_objects.append(o)
            link_set[items['link']] = items['link']
    question.advanced.add(*a_objects)
    return
