# flake8: noqa

import json
from itertools import chain
from celery import shared_task
from googleapiclient.discovery import build

from dashboard.models import (
    Dashboard,
    Guide,
    StarterGuide,
    IntermediateGuide,
    AdvancedGuide,
    Field)
from helpers.functions import get_text
from track.settings import env

cx_key = env('CX_KEY')
cse_key = env('CSE_KEY')


def execute_starters(link_set: set, service, guide: Guide, field_obj: Field, sta: list):
    pass


def execute_intermediates(link_set: set, service, guide: Guide, field_obj: Field, inta: list):
    pass


def execute_advance(link_set: set, service, guide: Guide, field_obj: Field, adv: list):
    pass


def get_names():
    return execute_starters, execute_intermediates, execute_advance


# todo: rewrite using thread or process, handle timeout gracefully
@shared_task
def track(pk: int):
    dashboard = Dashboard.objects.get(pk=pk)
    link_set = set()
    service = build('customsearch', 'v1', developerKey=cse_key)
    field_obj = dashboard.field.first()
    guide = Guide()
    guide.save()

    # query terms
    starter, intermediate, advance = [texts for texts in get_text(
        field_obj.field, field_obj.aoc)]

    # starters
    starters = [json.loads(json.dumps(service.cse().list(
        q=starter[resp], cx=cx_key
    ).execute()))['items'] for resp in range(4)]

    starter_attrs = []
    for items in chain(*starters):
        if items['link'] not in link_set:
            attr = (items['title'],
                    items['link'],
                    items['snippet'],
                    )
            starter_attrs.append(attr)
            link_set.add(items['link'])

    starter_objects = StarterGuide.objects.bulk_create([StarterGuide(
        title=item[0], link=item[1], description=item[2]) for item in
        starter_attrs])
    guide.starter.add(*[obj for obj in starter_objects])

    # intermediates
    intermediate = [json.loads(json.dumps(service.cse().list(
        q=intermediate[resp], cx=cx_key
    ).execute()))['items'] for resp in range(4)]

    intermediate_attrs = []
    for items in chain(*intermediate):
        if items['link'] not in link_set:
            attr = (items['title'],
                    items['link'],
                    items['snippet'],
                    )
            intermediate_attrs.append(attr)
            link_set.add(items['link'])

    intermediate_objects = IntermediateGuide.objects.bulk_create([
        IntermediateGuide(title=item[0], link=item[1], description=item[2])
        for item in intermediate_attrs])
    guide.intermediate.add(*[obj for obj in intermediate_objects])

    # advance
    advance = [json.loads(json.dumps(service.cse().list(
        q=advance[response], cx=cx_key
    ).execute()))['items'] for response in range(4)]

    advance_attrs = []
    for items in chain(*advance):
        if items['link'] not in link_set:
            attr = (items['title'],
                    items['link'],
                    items['snippet'],
                    )
            advance_attrs.append(attr)
            link_set.add(items['link'])

    advance_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=item[0], link=item[1], description=item[2]
    ) for item in advance_attrs])
    guide.advanced.add(*[obj for obj in advance_objects])

    # to field by foreign key
    field_obj.guide = guide
    field_obj.save()

    # q = queue.Queue(maxsize=3)
    # q.put([Process(
    #     target=get_names()[i], args=(link_set, service, guide),
    #     kwargs={'sta': sta, 'inta': inta, 'adv': adv}) for i in range(3)
    # ])
    # while not q.empty():
    #     proc = q.get()
    #     if proc is None:
    #         break
    #     _start = proc.start()
    #     _join = proc.join()
    #  todo
    # procs = [Process(
    #     target=get_names()[i], args=(link_set, service, guide, field_obj),
    #     kwargs={'sta': sta, 'inta': inta, 'adv': adv}) for i in range(3)
    # ]
    # _start = [proc.start() for proc in procs]
    # # _terminate = [proc.terminate() for proc in procs]
    # _join = [proc.join() for proc in procs]
