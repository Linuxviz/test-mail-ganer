# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from .views import RegisterUser, LoginUser, logout_user

urlpatterns = [
    url(r'^$', views.main_view, name='main_page'),
    url(r'^register/$', RegisterUser.as_view(), name='register'),
    url(r'^login/$', LoginUser.as_view(), name='login'),
    url(r'^logout/$', logout_user, name='logout_user'),
]
