import json
from celery import shared_task
from googleapiclient.discovery import build

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
from helpers.functions import get_text, run_check
from track.settings import env

cx_key = env('CX_KEY')
cse_key = env('CSE_KEY')


@shared_task
def starter(field_pk: int, keys: tuple, link_set: dict) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(field_pk)
    stats, _, _ = [texts for texts in get_text(field.field, field.aoc)]

    # order => article, pdf, class, video, question => 5
    articles = json.loads(json.dumps(service.cse().list(
        q=stats[0], cx=cx_key).execute()))['items']  # 10 dict items
    article_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(articles, link_set)])
    article = Article.objects.get(keys[0])
    article.starter.add(article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=stats[1], cx=cx_key).execute()))['items']
    pdf_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(pdfs, link_set)])
    pdf = PDF.objects.get(keys[1])
    pdf.starter.add(pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=stats[2], cx=cx_key).execute()))['items']
    class_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(classes, link_set)])
    klass = Klass.objects.get(keys[2])
    klass.starter.add(class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=stats[3], cx=cx_key).execute()))['items']
    video_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(videos, link_set)])
    video = Video.objects.get(keys[3])
    video.starter.add(video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=stats[4], cx=cx_key).execute()))['items']
    question_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(questions, link_set)])
    question = Question.objects.get(keys[4])
    question.starter.add(question_objects)


@shared_task
def intermediate(field_pk: int, keys: tuple, link_set: dict) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(field_pk)
    _, ints, _ = [texts for texts in get_text(field.field, field.aoc)]

    articles = json.loads(json.dumps(service.cse().list(
        q=ints[0], cx=cx_key).execute()))['items']
    article_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(articles, link_set)])
    article = Article.objects.get(keys[0])
    article.intermediate.add(article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=ints[1], cx=cx_key).execute()))['items']
    pdf_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(pdfs, link_set)])
    pdf = PDF.objects.get(keys[1])
    pdf.intermediate.add(pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=ints[2], cx=cx_key).execute()))['items']
    class_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(classes, link_set)])
    klass = Klass.objects.get(keys[2])
    klass.intermediate.add(class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=ints[3], cx=cx_key).execute()))['items']
    video_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(videos, link_set)])
    video = Video.objects.get(keys[3])
    video.intermediate.add(video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=ints[4], cx=cx_key).execute()))['items']
    question_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(questions, link_set)])
    question = Question.objects.get(keys[4])
    question.intermediate.add(question_objects)


@shared_task
def advance(field_pk: int, keys: tuple, link_set: dict) -> None:
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = Field.objects.get(field_pk)
    _, _, advs = [texts for texts in get_text(field.field, field.aoc)]

    articles = json.loads(json.dumps(service.cse().list(
        q=advs[0], cx=cx_key).execute()))['items']
    article_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(articles, link_set)])
    article = Article.objects.get(keys[0])
    article.advanced.add(article_objects)

    pdfs = json.loads(json.dumps(service.cse().list(
        q=advs[1], cx=cx_key).execute()))['items']
    pdf_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(pdfs, link_set)])
    pdf = PDF.objects.get(keys[1])
    pdf.advanced.add(pdf_objects)

    classes = json.loads(json.dumps(service.cse().list(
        q=advs[2], cx=cx_key).execute()))['items']
    class_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(classes, link_set)])
    klass = Klass.objects.get(keys[2])
    klass.advanced.add(class_objects)

    videos = json.loads(json.dumps(service.cse().list(
        q=advs[3], cx=cx_key).execute()))['items']
    video_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(videos, link_set)])
    video = Video.objects.get(keys[3])
    video.advanced.add(video_objects)

    questions = json.loads(json.dumps(service.cse().list(
        q=advs[4], cx=cx_key).execute()))['items']
    question_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in run_check(questions, link_set)])
    question = Question.objects.get(keys[4])
    question.advanced.add(question_objects)


parallels = [starter, intermediate, advance]
