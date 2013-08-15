from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'signup/$', views.SignUpView.as_view(), name='sign_up'),
    url(r'signin/$', views.SignInView.as_view(), name='sign_in'),
    url(r'signout/$', views.SignOutView.as_view(), name='sign_out'),
)
