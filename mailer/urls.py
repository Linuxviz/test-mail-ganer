# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import SubscriberListView, add_subscriber, add_subscribers, push_mails, email_identificator, add_template

urlpatterns = [
    url(r'^$', SubscriberListView.as_view(), name='subscriber_list'),
    url(r'^add_subscriber/$', add_subscriber, name='add_subscriber'),
    url(r'^add_subscribers/$', add_subscribers, name='add_subscribers'),
    url(r'^add_template/$', add_template, name='add_template'),
    url(r'^push_mails/$', push_mails, name='push_mails'),
    url(
        r'^general_pixel/(?P<pushed_email_identificator>.+)/$',
        email_identificator,
        name='email_identificator'
    ),

]
