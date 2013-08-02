from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^create/$', views.PlayerGroupCreateView.as_view(), name='player_group_create'),
    url(r'(?P<slug>.+)/$', views.PlayerGroupDetailView.as_view(), name='player_group_detail'),
)
