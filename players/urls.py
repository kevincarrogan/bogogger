from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^$', views.PlayerListView.as_view(), name='player_list'),
    url(r'^create/$', views.PlayerCreateView.as_view(), name='player_create'),
    url(r'(?P<slug>.+)/$', views.PlayerDetailView.as_view(), name='player_detail'),
)
