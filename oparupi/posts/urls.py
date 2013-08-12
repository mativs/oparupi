from django.conf.urls import patterns, url

from oparupi.posts import views

urlpatterns = patterns('',
	url(r'^(?P<slug>[\w-]+)/', views.DetailView.as_view(), name='detail'),
)