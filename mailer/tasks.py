# -*- coding: utf-8 -*-
from core.celery_core import app
from .mailer import send
from .models import PushAction, Subscriber, PushedMessage


@app.task
def push_mails_task(push_action_id):
    push_action = PushAction.objects.get(pk=push_action_id)
    subscribers = Subscriber.objects.filter(active=True, group=push_action.pushed_group)

    for subscriber in subscribers:
        pushed_message = PushedMessage.objects.create(
            push_action=push_action,
            subscriber=subscriber
        )

        result = send(
            template=push_action.template.body.name,
            subject=push_action.subject,
            subscriber=subscriber,
            msg_id=pushed_message.get_full_identificator()
        )

        if int(result) == 1:
            pushed_message.status = 'success'
        else:
            pushed_message.status = 'error'

        pushed_message.save()
