from django.http import HttpResponse
from django.shortcuts import render

from oparupi.posts.models import Post

def home(request, template='home.html', context={}):
  post = Post.objects.latest('created')
  context['post'] = post
  return render(request, template, context)

