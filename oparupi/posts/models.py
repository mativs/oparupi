from django.db import models
from django.utils.text import slugify
from sorl.thumbnail import ImageField

from taggit.managers import TaggableManager

class Section(models.Model):
    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return self.title

    def latest(self):
        return self.posts.filter(is_published=True).latest('created')

    
    title = models.CharField(max_length=50)

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256)
    body = models.TextField()
    photo = ImageField(upload_to='photos', blank=True, null=True)
    section = models.ForeignKey(Section, related_name='posts')
    tags = TaggableManager(blank=True)
    is_published = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateField(default=None, blank=True, null=True)

    @property
    def preview(self):
        return self.body.split("<!--more-->")[0]