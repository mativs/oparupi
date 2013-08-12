from django.http import HttpResponse
from django.views import generic


from oparupi.posts.models import Post

class DetailView(generic.DetailView):
	model = Post
	template_name = 'posts/detail.html'