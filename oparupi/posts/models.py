from django.db import models

from taggit.managers import TaggableManager

class Section(models.Model):
    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __unicode__(self):
        return self.title

    def latest(self):
        return self.posts.latest('updated')

    
    title = models.CharField(max_length=50)

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=256)
    body = models.TextField()
    section = models.ForeignKey(Section, related_name='posts')
    tags = TaggableManager(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
