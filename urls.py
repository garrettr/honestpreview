from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'honestpreview.views.home', name='home'),
    # url(r'^honestpreview/', include('honestpreview.foo.urls')),

    #url(r'^$', home, name="home"),
    (r'^$', 'views.home'),
    (r'^signup$', 'views.validate_signup'),

    # django-newsletter
    (r'^newsletter/', include('newsletter.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
