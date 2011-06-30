from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^unsubscribe/(?P<code>\d+)/$', 'postman.views.unsubscribe'),
)
