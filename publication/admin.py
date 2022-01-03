# flake8: noqa

from django.contrib import admin, messages

from publication.models import Publication


class PublicationAdmin(admin.ModelAdmin):
    # list_display = ('author', 'title')
    search_fields = ('description', 'title', )
    list_filter = ('author', 'title', 'description')
    list_select_related = True
    actions_on_bottom = True

    def delete_model(self, request, obj):
        author = request.user
        if obj.author is not author:
            messages.error(request, 'method is not allowed')
        else:
            super(PublicationAdmin, self).delete_model(request, obj)


admin.site.register(Publication, PublicationAdmin)
