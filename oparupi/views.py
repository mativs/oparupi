from django.http import HttpResponse
from django.shortcuts import render

from oparupi.posts.models import Post, Section

def home(request, template='home.html', context={}):
  context['sections'] = Section.objects.all()
  context['post'] = Post.objects.latest('created')
  return render(request, template, context)

