from django.contrib import admin
from .models import Query, Link


class QueryAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Link, LinkAdmin)
admin.site.register(Query, QueryAdmin)
