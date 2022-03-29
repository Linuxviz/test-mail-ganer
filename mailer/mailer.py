# -*- coding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send(template, subscriber, subject, msg_id):
    """ Render and push mail """
    html_content = render_to_string(
        template,
        {
            'msg_id': msg_id,
            'name': subscriber.name,
            'second_name': subscriber.second_name,
            'birthday': subscriber.birthday,
        }
    )
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=None,
        to=[subscriber.email_address, ],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send()


def is_valid_template(template):
    """ Html-template must have not '%}' or '{%' """
    with open(template, 'r') as f:
        for line in f:
            if ('{%' in line) or ('%}' in line):
                return False
    return True
