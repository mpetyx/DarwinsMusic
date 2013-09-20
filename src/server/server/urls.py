from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'server.views.home', name='home'),
                       # url(r'^server/', include('server.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^map$', views.map, name="map"),
                       url(r'^sparql$', views.sparql, name="sparql"),
                       url(r'^$', views.index, name='index'),
                       (r'^s/(?P<path>.*)$', 'django.views.static.serve',
                                {'document_root': settings.STATIC_DOC_ROOT}),

)#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
