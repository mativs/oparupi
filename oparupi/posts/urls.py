from django.conf.urls import patterns, url

from oparupi.posts import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)