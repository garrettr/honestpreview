from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^unsubscribe/(?P<code>[0-9a-f]+)/$', 'postman.views.unsubscribe'),
)
