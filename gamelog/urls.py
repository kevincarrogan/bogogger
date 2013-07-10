from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^games/', include('games.urls')),
    url(r'^players/', include('players.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
