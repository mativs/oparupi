from django.http import HttpResponse
from django.shortcuts import render

def home(request, template='home.html', context=[]):
  
  return render(request, template, context)

