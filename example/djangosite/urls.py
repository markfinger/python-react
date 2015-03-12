from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('example_app.urls')),
)