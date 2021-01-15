from django.contrib import admin
from .models import Bb, Rubric, Profile, Response, Reviews
from django.contrib import admin


class ResponseInline(admin.StackedInline):
    model = Response
    extra = 0
    readonly_fields = ('user', 'text',)


@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'rubric', 'user', 'published',)
    list_display_links = ("title", 'content')
    search_fields = ('title', 'content',)
    inlines = [ResponseInline]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'post',)
    list_display_links = ('user', 'post')
    readonly_fields = ('user', 'text',)


admin.site.register(Rubric)
#admin.site.register(Bb)
admin.site.register(Reviews)
admin.site.register(Profile)

