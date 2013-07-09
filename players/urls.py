from django.conf.urls import patterns, include, url

from . import views


urlpatterns = patterns('',
    url(r'^create/$', views.PlayerCreateView.as_view(), name='player_create'),
    url(r'(?P<pk>\d+)/$', views.PlayerDetailView.as_view(), name='player_detail'),
)
