from django.contrib import admin
from django.db import models
from oparupi.posts.models import Post, Section
from sorl.thumbnail.admin import AdminImageMixin
from epiceditor.widgets import AdminEpicEditorWidget
from datetime import datetime



class PostAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'published', 'is_published')
    formfield_overrides = {
        models.TextField: {'widget': AdminEpicEditorWidget },
    }

    # Actions
    def make_published(modeladmin, request, queryset):
        queryset.update(is_published=True, published=datetime.now())
    make_published.short_description = "Mark selected posts as published"

    def make_unpublished(modeladmin, request, queryset):
        queryset.update(is_published=False, published=None)
    make_unpublished.short_description = "Mark selected posts as unpublished"

    actions = [make_published, make_unpublished]

admin.site.register(Post, PostAdmin)
admin.site.register(Section)
