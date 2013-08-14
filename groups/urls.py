from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.PlayerGroupListView.as_view(), name='player_group_list'),
    url(r'^create/$', views.PlayerGroupCreateView.as_view(), name='player_group_create'),

    url(r'^(?P<slug>.+)/games/$', views.PlayerGroupGameListView.as_view(), name='player_group_game_list'),
    url(r'^(?P<slug>.+)/games/create/$', views.PlayerGroupGameCreateView.as_view(), name='player_group_game_create'),

    url(r'^(?P<slug>.+)/players/add/$', views.PlayerGroupPlayerAddView.as_view(), name='player_group_player_add'),
    url(r'^(?P<slug>.+)/players/invite/$', views.PlayerGroupPlayerInviteView.as_view(), name='player_group_invite'),

    url(r'(?P<slug>.+)/$', views.PlayerGroupDetailView.as_view(), name='player_group_detail'),
)
