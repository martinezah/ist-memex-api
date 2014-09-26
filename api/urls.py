from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^/?$', 'api.views.index'),
    url(r'^hash/?$', 'api.views.get_urlkey'),
    url(r'^timestamp/?$', 'api.views.get_timestamp'),
    url(r'^from/(?P<start>[^/]+)(/to/(?P<stop>[^/]+))?/?$', 'api.views.search_by_timestamp'),
    url(r'^by/(?P<attribute>[^/]+)/(?P<value>[^/]+)/?$', 'api.views.search_by_attribute'),
    url(r'^(?P<urlkey>[^/]+)/(from/(?P<start>[^/]+)(/to/(?P<stop>[^/]+))?)?/?$', 'api.views.urlkey_list'),
    url(r'^(?P<urlkey>[^/]+)/(?P<timestamp>[^/]+)/(?P<attribute>[^/]+)/?$', 'api.views.urlkey_item_attribute'),
    url(r'^(?P<urlkey>[^/]+)/(?P<timestamp>[^/]+)/?$', 'api.views.urlkey_item'),
)
