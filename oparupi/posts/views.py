from django.http import HttpResponse

def index(request):
  return HttpResponse("Hello, world. You are at the post view")
# Create your views here.
