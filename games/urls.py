from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.GameListView.as_view(), name='game_list'),
    url(r'^create/$', views.GameCreateView.as_view(), name='game_create'),
    url(r'^play/$', views.GamePlayCreateView.as_view(), name='game_play_create'),
    url(r'^play/(?P<pk>\d+)/$', views.GamePlayDetailView.as_view(), name='game_play_detail'),
    url(r'^(?P<slug>.+)/$', views.GameDetailView.as_view(), name='game_detail'),
)
