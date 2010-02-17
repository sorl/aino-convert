from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/1/'}),
    (r'^1/$', 'django.views.generic.simple.direct_to_template', {'template': '1.html'}),
    (r'^2/$', 'django.views.generic.simple.direct_to_template', {'template': '2.html'}),
    (r'^3/$', 'django.views.generic.simple.direct_to_template', {'template': '3.html'}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
