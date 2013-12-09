from django.http import HttpResponse
from django.shortcuts import render

from oparupi.posts.models import Post, Section
from taggit.models import Tag

def home(request, template='home.html', context={}):
  context['sections'] = Section.objects.all()
  context['post'] = Post.objects.latest('published')
  context['posts'] = Post.objects.filter(is_published=True).order_by('-published')
  context['tags'] = Tag.objects.all();
  return render(request, template, context)

