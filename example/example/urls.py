from django.conf.urls import patterns, include, url

urlpatterns = patterns('example.views',
    url(r'^$', 'index', name='index'),
)
