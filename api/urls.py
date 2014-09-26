from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^/$', 'api.views.index'),
    url(r'^by/(?P<attribute>.+)/(?P<value>.+)/$', 'api.views.attribute_scan'),
    url(r'^from/(?P<start>.+)/(to/(?P<end>.+)/)?$', 'api.views.timestamp_scan'),
    url(r'^artifacts/(?P<url>.+)/(?P<attribute>.+)/$', 'api.views.attribute_item'),
    url(r'^artifacts/(?P<url>.+)/$', 'api.views.artifact_item'),
)
