# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class SubscribersGroup(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        def __unicode__(self):
            return self.name


class Subscriber(models.Model):
    email_address = models.EmailField()
    name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    group = models.ManyToManyField(SubscribersGroup)

    class Meta:
        def __unicode__(self):
            return '%s - %s %s' % (self.email_address, self.name, self.second_name)
