# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from mailer.models import SubscribersGroup, Subscriber


class GroupAdmin(admin.ModelAdmin):
    pass


class SubscriberAdmin(admin.ModelAdmin):
    pass


admin.site.register(SubscribersGroup, GroupAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
