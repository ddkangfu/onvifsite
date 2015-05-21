from django.conf.urls import patterns, include, url
from django.contrib import admin
from onvifsiteapp.views import CamInformationView, thanks

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'onvifsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', CamInformationView.as_view(), name='camview'),
    url(r'^admin/', include(admin.site.urls)),
)
