import json

from dashboard.models import (
    Dashboard,
    Guide,
    StarterGuide,
    IntermediateGuide,
    AdvancedGuide
)
from helpers.functions import get_text
from track.settings import env

cx_key = env('CX_KEY')
cse_key = env('CSE_KEY')


# @shared_task  todo
def track(dashboard: Dashboard):
    link_set = set()
    # service = build('customsearch', 'v1', developerKey=cse_key)
    field_obj = dashboard.field.first()
    guide = Guide()
    guide.save()
    sr, ie, ae = [texts for texts in get_text(field_obj.field, field_obj.aoc)]

    starters = {}
    # for i in range(4):
    #     response = service.cse().list(q=sr[i], cx=cx_key
    #                                   ).execute()
    #     data = json.loads(json.dumps(response))
    #     items = data['items']
    #     for j in range(10):
    #         if items[j]['link'] not in link_set:
    #             starters[j] = starters.get(
    #                 j,
    #                 [items[j]['title'], items[j]['link'],
    #                  items[j]['snippet']]
    #             )
    #             link_set.add(items[j]['link'])

    # todo include order_by (time created perhaps)
    #  filter to reduce size:time
    before_starter = {obj for obj in StarterGuide.objects.all()}
    StarterGuide.objects.bulk_create([StarterGuide(
        title=starters[i][0], link=starters[i][1],
        description=starters[i][2]) for i in range(len(starters))])
    after_starter = {obj for obj in StarterGuide.objects.all()}
    starter = [obj.save() for obj in after_starter-before_starter]
    guide.starter.set(starter)

    intermediates = {}
    # for i in range(4):
    #     response = service.cse().list(q=ie[i], cx=cx_key
    #                                   ).execute()
    #     data = json.loads(json.dumps(response))
    #     items = data['items']
    #     for j in range(10):
    #         if items[j]['link'] not in link_set:
    #             intermediates[j] = intermediates.get(
    #                 j,
    #                 [items[j]['title'], items[j]['link'],
    #                  items[j]['snippet']]
    #             )
    #             link_set.add(items[j]['link'])

    before_inter = {obj for obj in IntermediateGuide.objects.all()}
    IntermediateGuide.objects.bulk_create([IntermediateGuide(
        title=intermediates[i][0], link=intermediates[i][1],
        description=intermediates[i][2])
        for i in range(len(intermediates))])
    after_inter = {obj for obj in IntermediateGuide.objects.all()}
    intermediate = [obj.save() for obj in after_inter-before_inter]
    guide.intermediate.set(intermediate)

    advance = {}
    # for i in range(4):
    #     response = service.cse().list(q=ae[i], cx=cx_key
    #                                   ).execute()
    #     data = json.loads(json.dumps(response))
    #     items = data['items']
    #     for j in range(10):
    #         if items[j]['link'] not in link_set:
    #             advance[j] = advance.get(
    #                 j,
    #                 [items[j]['title'], items[j]['link'],
    #                  items[j]['snippet']]
    #             )
    #             link_set.add(items[j]['link'])

    before_adv = {obj for obj in AdvancedGuide.objects.all()}
    AdvancedGuide.objects.bulk_create([AdvancedGuide(
        title=advance[i][0], link=advance[i][1],
        description=advance[i][2]) for i in range(len(advance))])
    after_adv = {obj for obj in AdvancedGuide.objects.all()}
    advanced = [obj.save() for obj in after_adv-before_adv]
    guide.advanced.set(advanced)

    field_obj.guide = guide
    field_obj.save()
