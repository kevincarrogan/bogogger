from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'signup/$', views.SignUpView.as_view(), name='sign_up'),
)
