from django.contrib import admin
from .models import Bb, Rubric, Response, Profile
from django.contrib import admin


class ResponseInline(admin.StackedInline):
    model = Response
    extra = 0
    readonly_fields = ('name', 'text',)


@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'rubric', 'user', 'published',)
    list_display_links = ("title", 'content')
    search_fields = ('title', 'content',)
    inlines = [ResponseInline]


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'post',)
    list_display_links = ('name', 'post')
    readonly_fields = ('name', 'text',)


admin.site.register(Rubric)
#admin.site.register(Bb)
admin.site.register(Profile)

