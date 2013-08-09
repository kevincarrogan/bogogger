from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dashboard.views import DashboardView


urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'', include('authorisation.urls')),
    url(r'^games/', include('games.urls')),
    url(r'^players/', include('players.urls')),
    url(r'^groups/', include('groups.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
