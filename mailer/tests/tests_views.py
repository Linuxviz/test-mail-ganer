# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mock import patch
from django.contrib.auth.models import User
from django.test import TestCase
from django.template.loader import render_to_string

# Create your tests here.
from django.urls import reverse

from mailer.models import Subscriber, SubscribersGroup, PushAction, EmailTemplate, PushedMessage
from django.core.files.uploadedfile import SimpleUploadedFile


class TestEmailIdentificatorViewTest(TestCase):
    def test_get_page(self):
        self.user = User.objects.create(
            username='OpenUser',
            is_staff=False,
            is_superuser=False
        )
        self.client.force_login(self.user)
        self.group = SubscribersGroup.objects.create(
            name='sb_name_grp',
            user=self.user
        )
        self.subscriber = Subscriber.objects.create(
            email_address='',
            user=self.user,
        )
        self.subscriber.group.add(self.group.pk)
        self.email_template = EmailTemplate.objects.create(
            name='some_template',
            user=self.user,
            body=SimpleUploadedFile(
                "template.html",
                str("<p>Test</p>")  # note the b in front of the string [bytes]
            )
        )
        self.push_action = PushAction.objects.create(
            template=self.email_template,
            subject='somesubject',
            pushed_group=self.group,
        )
        self.pushed_message = PushedMessage.objects.create(
            push_action=self.push_action,
            subscriber=self.subscriber
        )
        self.pushed_message.refresh_from_db()
        self.assertEqual(self.pushed_message.view_count, 0)
        self.assertEqual(self.pushed_message.first_view_data, None)
        self.assertEqual(len(str(self.pushed_message.identificator)), 36)

        url = reverse(
            'email_identificator',
            args=[
                str(self.pushed_message.identificator) + str(self.pushed_message.pk),
            ]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.pushed_message.refresh_from_db()
        self.assertEqual(self.pushed_message.view_count, 1)
        self.assertNotEqual(self.pushed_message.first_view_data, None)
        old_data = self.pushed_message.first_view_data

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.pushed_message.refresh_from_db()
        self.assertEqual(self.pushed_message.view_count, 2)
        self.assertEqual(self.pushed_message.first_view_data, old_data)


class PushMailsViewTest(TestCase):

    def test_post_page(self):
        with patch('mailer.views.push_mails_task.apply_async') as perm_mock:
            self.user = User.objects.create(
                username='OpenUser',
                is_staff=False,
                is_superuser=False
            )
            self.client.force_login(self.user)
            self.group = SubscribersGroup.objects.create(
                name='sb_name_grp',
                user=self.user
            )
            self.subscriber = Subscriber.objects.create(
                email_address='',
                user=self.user,
            )
            self.subscriber.group.add(self.group.pk)
            self.email_template = EmailTemplate.objects.create(
                name='some_template',
                user=self.user,
                body=SimpleUploadedFile(
                    "template.html",
                    str("<p>Test</p>")  # note the b in front of the string [bytes]
                )
            )

            response = self.client.post(
                path=reverse('push_mails'),
                data={
                    'template': self.email_template.pk,
                    'subject': 'somesubject',
                    'pushed_group': self.group.pk,
                    # 'delay_time' :
                }
            )

            self.assertEqual(response.status_code, 302)
            self.assertEqual(perm_mock.call_count, 1)
