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
    result = render_to_string('email_example.html', context={'content': html_content})
    text_content = strip_tags(result)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=None,
        to=[subscriber.email_address, ],
    )
    email.attach_alternative(result, 'text/html')
    result = email.send()
    return result


def is_valid_template(template):
    """ Html-template must have not '%}' or '{%' """
    with open(template, 'r') as f:
        for line in f:
            if ('{%' in line) or ('%}' in line):
                return False
    return True
