from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^games/', include('games.urls')),
    # url(r'^players/$', include('gamelog.players.urls')),
)
