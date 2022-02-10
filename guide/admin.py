from django.contrib import admin

from guide.models import (
    Guide,
    BasicGuide,
    AdvancedGuide,
    Article, PDF, Klass, Video, Question)

admin.site.register(Guide)
admin.site.register(BasicGuide)
admin.site.register(AdvancedGuide)
admin.site.register(Article)
admin.site.register(PDF)
admin.site.register(Klass)
admin.site.register(Video)
admin.site.register(Question)
