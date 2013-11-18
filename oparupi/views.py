from django.http import HttpResponse
from django.shortcuts import render

from oparupi.posts.models import Post, Section
from taggit.models import Tag

def home(request, template='home.html', context={}):
  context['sections'] = Section.objects.all()
  context['post'] = Post.objects.latest('created')
  context['posts'] = Post.objects.all().order_by('-created')
  context['tags'] = Tag.objects.all();
  return render(request, template, context)

