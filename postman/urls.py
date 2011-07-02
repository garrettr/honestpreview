from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^unsubscribe/(?P<code>[0-9a-f]+)/$', 'postman.views.unsubscribe'),
    (r'^unsubscribe/confirmation/(?P<id>\d+)/$', 'postman.views.unsubscribe_confirm'),
    (r'^unsubscribe/error/(?P<id>\d+)/$', 'postman.views.unsubscribe_error'),
)
