from django.contrib import admin
from oparupi.posts.models import Post, Section
from sorl.thumbnail.admin import AdminImageMixin

class PostAdmin(AdminImageMixin, admin.ModelAdmin):
	pass

admin.site.register(Post, PostAdmin)
admin.site.register(Section)
