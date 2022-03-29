# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from uuid import uuid4
from django.contrib.auth.models import User
from django.db import models


class SubscribersGroup(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.name


class Subscriber(models.Model):
    email_address = models.EmailField()
    name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    group = models.ManyToManyField(SubscribersGroup)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s - %s %s' % (self.email_address, self.name, self.second_name)

# add static root
def user_directory_path_for_SubscribersCollection(instance, filename):
    return 'static/user_{0}/{1}'.format(instance.group.user.pk, filename)


def user_directory_path_for_EmailTemplate(instance, filename):
    return 'static/user_{0}/templates/{1}'.format(instance.user.pk, filename)


class SubscribersCollection(models.Model):
    group = models.ForeignKey(SubscribersGroup, on_delete=models.SET_NULL, null=True)
    calculated = models.BooleanField(default=False)
    group_name = models.CharField(max_length=100)
    upload_file = models.FileField(upload_to=user_directory_path_for_SubscribersCollection)

    # TODO unicode


class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    body = models.FileField(upload_to=user_directory_path_for_EmailTemplate)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class PushAction(models.Model):
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=150)
    group_push_date = models.DateTimeField(auto_now_add=True)
    pushed_group = models.ForeignKey(SubscribersGroup, on_delete=models.SET_NULL, null=True)
    delay_time = models.DateTimeField(null=True, blank=True)


class PushedMessage(models.Model):
    push_action = models.ForeignKey(PushAction, on_delete=models.SET_NULL, null=True)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.SET_NULL, null=True)
    view_count = models.SmallIntegerField(default=0)
    first_view_data = models.DateTimeField(null=True, blank=True)
    identificator = models.UUIDField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.identificator:
            self.identificator = uuid4()
        super(PushedMessage, self).save(*args, **kwargs)

    def get_full_identificator(self):
        if self.pk is not None:
            return '%s%s' % (self.identificator, self.pk)
        raise Exception("id is not set yet")
