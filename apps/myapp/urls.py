from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^myapp$', views.index),
    url(r'^myapp/register$', views.register),
    url(r'^myapp/login$', views.login),
    url(r'^user/(?P<id>\d+)/$', views.user_page),
    url(r'^friends$', views.friends_page, name='friends'),
    url(r'^connect/(?P<operation>.+)/(?P<id>\d+)/$', views.change_friends, name='change_friends'),
    url(r'^logout$', views.logout)
]