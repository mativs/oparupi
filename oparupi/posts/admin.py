from django.contrib import admin
from django.db import models
from oparupi.posts.models import Post, Section
from sorl.thumbnail.admin import AdminImageMixin
from epiceditor.widgets import AdminEpicEditorWidget

class PostAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    formfield_overrides = {
        models.TextField: {'widget': AdminEpicEditorWidget },
    }

admin.site.register(Post, PostAdmin)
admin.site.register(Section)
