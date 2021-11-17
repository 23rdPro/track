# flake8: noqa

import json
from itertools import chain
from celery import shared_task
from googleapiclient.discovery import build

from dashboard.models import (
    Dashboard,
    StarterGuide,
    IntermediateGuide,
    AdvancedGuide,
    Guide)
from helpers.functions import get_text
from track.settings import env

cx_key = env('CX_KEY')
cse_key = env('CSE_KEY')


@shared_task
def starter(pk: int, link_set: dict) -> None:
    dashboard = Dashboard.objects.get(pk=pk)
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = dashboard.field.first()
    stats, _, _ = [texts for texts in get_text(field.field, field.aoc)]
    starters = [json.loads(json.dumps(service.cse().list(
        q=stats[resp], cx=cx_key
    ).execute()))['items'] for resp in range(len(stats))]  # 4 times

    attributes = []
    for items in chain(*starters):
        if items['link'] not in link_set:
            attributes.append((items['title'], items['link'], items['snippet']))
            link_set[items['link']] = items['link']
    starter_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in attributes])
    field = Dashboard.objects.get(pk=pk).field.first()
    guide = Guide.objects.get(pk=field.guide.pk)  # todo pdb here
    guide.starter.add(*[obj for obj in starter_objects])
    field.save()


@shared_task
def intermediate(pk: int, link_set: dict) -> None:
    dashboard = Dashboard.objects.get(pk=pk)
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = dashboard.field.first()
    _, ints, _ = [texts for texts in get_text(field.field, field.aoc)]
    intermediates = [json.loads(json.dumps(service.cse().list(
        q=ints[resp], cx=cx_key
    ).execute()))['items'] for resp in range(len(ints))]

    attributes = []
    for items in chain(*intermediates):
        if items['link'] not in link_set:
            attributes.append((items['title'], items['link'], items['snippet']))
            link_set[items['link']] = items['link']
    intermediate_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in attributes])
    field = Dashboard.objects.get(pk=pk).field.first()
    guide = Guide.objects.get(pk=field.guide.pk)
    guide.intermediate.add(*[obj for obj in intermediate_objects])
    field.save()


@shared_task
def advance(pk: int, link_set: dict) -> None:
    dashboard = Dashboard.objects.get(pk=pk)
    service = build('customsearch', 'v1', developerKey=cse_key)
    field = dashboard.field.first()
    _, _, advs = [texts for texts in get_text(field.field, field.aoc)]
    advanced = [json.loads(json.dumps(service.cse().list(
        q=advs[resp], cx=cx_key
    ).execute()))['items'] for resp in range(len(advs))]

    attributes = []
    for items in chain(*advanced):
        if items['link'] not in link_set:
            attributes.append((items['title'], items['link'], items['snippet']))
            link_set[items['link']] = items['link']
    advance_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in attributes])
    field = Dashboard.objects.get(pk=pk).field.first()
    pk = field.guide.pk
    guide = Guide.objects.get(pk=pk)
    guide.advanced.add(*[obj for obj in advance_objects])
    field.save()


parallels = [starter, intermediate, advance]
