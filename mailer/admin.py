# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PushedMessage, EmailTemplate, SubscribersCollection, SubscribersGroup, Subscriber


class GroupAdmin(admin.ModelAdmin):
    pass


class SubscriberAdmin(admin.ModelAdmin):
    pass


class SubscribersCollectionAdmin(admin.ModelAdmin):
    pass


class PushedMessageAdmin(admin.ModelAdmin):
    pass


class EmailTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(PushedMessage, PushedMessageAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(SubscribersCollection, SubscribersCollectionAdmin)
admin.site.register(SubscribersGroup, GroupAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
