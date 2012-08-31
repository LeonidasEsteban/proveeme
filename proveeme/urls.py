from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'website.views.home'),
    url(r'^entrar$', 'website.views.entrar'),
    url(r'^registro$', 'website.views.registro'),
    url(r'^cotiza$', 'website.views.cotiza'),
    url(r'^solicitudes$', 'website.views.solicitudes'),
    url(r'^cotizaciones$', 'website.views.cotizaciones'),
    url(r'^salir$', 'website.views.salir'),

    # search engine
    url(r'^buscar_producto$', 'website.views.buscar_producto'),
    url(r'^buscar_region$', 'website.views.buscar_region'),
    url(r'^buscar_empresas$', 'website.views.buscar_empresas'),

    # url(r'^proveeme/', include('proveeme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
