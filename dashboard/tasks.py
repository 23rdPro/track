# import json
# from itertools import chain
# from celery import shared_task
# from googleapiclient.discovery import build
#
# from dashboard.models import Dashboard
# from guide.models import StarterGuide, Guide, IntermediateGuide, AdvancedGuide, Article, PDF, Klass, Video, Question
# from helpers.functions import get_text, run_check
# from track.settings import env
#
# cx_key = env('CX_KEY')
# cse_key = env('CSE_KEY')
#
#
# @shared_task
# def starter(pk: int, keys: tuple, link_set: dict) -> None:
#     dashboard = Dashboard.objects.get(pk=pk)
#     service = build('customsearch', 'v1', developerKey=cse_key)
#     field = dashboard.field.first()
#     stats, _, _ = [texts for texts in get_text(field.field, field.aoc)]
#
#     # order => article, pdf, class, video, question => 5
#     articles = json.loads(json.dumps(service.cse().list(
#         q=stats[0], cx=cx_key).execute()))['items']  # 10 dict items
#     article_objects = StarterGuide.objects.bulk_create([StarterGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(articles, link_set)])
#     article = Article.objects.get(keys[0])
#     article.starter.add(article_objects)
#
#     pdfs = json.loads(json.dumps(service.cse().list(
#         q=stats[1], cx=cx_key).execute()))['items']
#     pdf_objects = StarterGuide.objects.bulk_create([StarterGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(pdfs, link_set)])
#     pdf = PDF.objects.get(keys[1])
#     pdf.starter.add(pdf_objects)
#
#     classes = json.loads(json.dumps(service.cse().list(
#         q=stats[2], cx=cx_key).execute()))['items']
#     class_objects = StarterGuide.objects.bulk_create([StarterGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(classes, link_set)])
#     klass = Klass.objects.get(keys[2])
#     klass.starter.add(class_objects)
#
#     videos = json.loads(json.dumps(service.cse().list(
#         q=stats[3], cx=cx_key).execute()))['items']
#     video_objects = StarterGuide.objects.bulk_create([StarterGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(videos, link_set)])
#     video = Video.objects.get(keys[3])
#     video.starter.add(video_objects)
#
#     questions = json.loads(json.dumps(service.cse().list(
#         q=stats[4], cx=cx_key).execute()))['items']
#     question_objects = StarterGuide.objects.bulk_create([StarterGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(questions, link_set)])
#     question = Question.objects.get(keys[4])
#     question.starter.add(question_objects)
#
#     field = Dashboard.objects.get(pk=pk).field.first()
#     guide = Guide.objects.get(pk=field.guide.pk)
#     objects = list(chain(*[article_objects, pdf_objects, class_objects,
#                            video_objects, question_objects]))
#     guide.starter.add(*objects)
#     field.save()
#
#
# # @shared_task
# # def starter(pk: int, link_set: dict) -> None:
# #     dashboard = Dashboard.objects.get(pk=pk)  # dry
# #     service = build('customsearch', 'v1', developerKey=cse_key)  # dry
# #     field = dashboard.field.first()  # dry
# #     stats, _, _ = [texts for texts in get_text(field.field, field.aoc)]
# #     starters = [json.loads(json.dumps(service.cse().list(
# #         q=stats[resp], cx=cx_key
# #     ).execute()))['items'] for resp in range(len(stats))]  # 4 times
# #
# #     attributes = []
# #     for items in chain(*starters):
# #         if items['link'] not in link_set:
# #             attributes.append((items['title'], items['link'], items['snippet']))
# #             link_set[items['link']] = items['link']
# #     starter_objects = StarterGuide.objects.bulk_create([StarterGuide(
# #         title=item[0], link=item[1], description=item[2]
# #     ) for item in attributes])
# #     field = Dashboard.objects.get(pk=pk).field.first()
# #     guide = Guide.objects.get(pk=field.guide.pk)  # todo pdb here
# #     guide.starter.add(*[obj for obj in starter_objects])
# #     field.save()
#
#
# @shared_task
# def intermediate(pk: int, link_set: dict) -> None:
#     dashboard = Dashboard.objects.get(pk=pk)
#     service = build('customsearch', 'v1', developerKey=cse_key)
#     field = dashboard.field.first()
#     _, ints, _ = [texts for texts in get_text(field.field, field.aoc)]
#
#     articles = json.loads(json.dumps(service.cse().list(
#         q=ints[0], cx=cx_key).execute()))['items']
#     article_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(articles, link_set)])
#
#     pdfs = json.loads(json.dumps(service.cse().list(
#         q=ints[1], cx=cx_key).execute()))['items']
#     pdf_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(pdfs, link_set)])
#
#     classes = json.loads(json.dumps(service.cse().list(
#         q=ints[2], cx=cx_key).execute()))['items']
#     class_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(classes, link_set)])
#
#     videos = json.loads(json.dumps(service.cse().list(
#         q=ints[3], cx=cx_key).execute()))['items']
#     video_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(videos, link_set)])
#
#     questions = json.loads(json.dumps(service.cse().list(
#         q=ints[4], cx=cx_key).execute()))['items']
#     question_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(questions, link_set)])
#
#     field = Dashboard.objects.get(pk=pk).field.first()
#     guide = Guide.objects.get(pk=field.guide.pk)
#     objects = list(chain(*[article_objects, pdf_objects, class_objects,
#                            video_objects, question_objects]))
#     guide.starter.add(*objects)
#     field.save()
#
#
# # @shared_task
# # def intermediate(pk: int, link_set: dict) -> None:
# #     dashboard = Dashboard.objects.get(pk=pk)
# #     service = build('customsearch', 'v1', developerKey=cse_key)
# #     field = dashboard.field.first()
# #     _, ints, _ = [texts for texts in get_text(field.field, field.aoc)]
# #     intermediates = [json.loads(json.dumps(service.cse().list(
# #         q=ints[resp], cx=cx_key
# #     ).execute()))['items'] for resp in range(len(ints))]
# #
# #     attributes = []
# #     for items in chain(*intermediates):
# #         if items['link'] not in link_set:
# #             attributes.append((items['title'], items['link'], items['snippet']))
# #             link_set[items['link']] = items['link']
# #     intermediate_objects = IntermediateGuide.objects.bulk_create([IntermediateGuide(
# #         title=item[0], link=item[1], description=item[2]
# #     ) for item in attributes])
# #     field = Dashboard.objects.get(pk=pk).field.first()
# #     guide = Guide.objects.get(pk=field.guide.pk)
# #     guide.intermediate.add(*[obj for obj in intermediate_objects])
# #     field.save()
#
#
# @shared_task
# def advance(pk: int, link_set: dict) -> None:
#     dashboard = Dashboard.objects.get(pk=pk)
#     service = build('customsearch', 'v1', developerKey=cse_key)
#     field = dashboard.field.first()
#     _, _, advs = [texts for texts in get_text(field.field, field.aoc)]
#
#     articles = json.loads(json.dumps(service.cse().list(
#         q=advs[0], cx=cx_key).execute()))['items']
#     article_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(articles, link_set)])
#
#     pdfs = json.loads(json.dumps(service.cse().list(
#         q=advs[1], cx=cx_key).execute()))['items']
#     pdf_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(pdfs, link_set)])
#
#     classes = json.loads(json.dumps(service.cse().list(
#         q=advs[2], cx=cx_key).execute()))['items']
#     class_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(classes, link_set)])
#
#     videos = json.loads(json.dumps(service.cse().list(
#         q=advs[3], cx=cx_key).execute()))['items']
#     video_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(videos, link_set)])
#
#     questions = json.loads(json.dumps(service.cse().list(
#         q=advs[4], cx=cx_key).execute()))['items']
#     question_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
#         title=item[0], link=item[1], description=item[2]
#     )for item in run_check(questions, link_set)])
#
#     field = Dashboard.objects.get(pk=pk).field.first()
#     guide = Guide.objects.get(pk=field.guide.pk)
#     objects = list(chain(*[article_objects, pdf_objects, class_objects,
#                            video_objects, question_objects]))
#     guide.starter.add(*objects)
#     field.save()
#
#
# # @shared_task
# # def advance(pk: int, link_set: dict) -> None:
# #     dashboard = Dashboard.objects.get(pk=pk)
# #     service = build('customsearch', 'v1', developerKey=cse_key)
# #     field = dashboard.field.first()
# #     _, _, advs = [texts for texts in get_text(field.field, field.aoc)]
# #     advanced = [json.loads(json.dumps(service.cse().list(
# #         q=advs[resp], cx=cx_key
# #     ).execute()))['items'] for resp in range(len(advs))]
# #
# #     attributes = []
# #     for items in chain(*advanced):
# #         if items['link'] not in link_set:
# #             attributes.append((items['title'], items['link'], items['snippet']))
# #             link_set[items['link']] = items['link']
# #     advance_objects = AdvancedGuide.objects.bulk_create([AdvancedGuide(
# #         title=item[0], link=item[1], description=item[2]
# #     ) for item in attributes])
# #     field = Dashboard.objects.get(pk=pk).field.first()
# #     guide = Guide.objects.get(pk=field.guide.pk)
# #     guide.advanced.add(*[obj for obj in advance_objects])
# #     field.save()
#
#
# parallels = [starter, intermediate, advance]
