# -*- coding: utf-8 -*-
from core.celery_core import app
from .mailer import send, is_valid_template
from .models import PushAction, Subscriber, PushedMessage


@app.task
def push_mails_task(push_action_id):
    # todo try
    push_action = PushAction.objects.get(pk=push_action_id)
    subscribers = Subscriber.objects.filter(active=True, group=push_action.pushed_group)

    for subscriber in subscribers:
        pushed_message = PushedMessage.objects.create(
            push_action=push_action,
            subscriber=subscriber
        )

        send(
            template=push_action.template.body.name,
            subject=push_action.subject,
            subscriber=subscriber,
            msg_id=pushed_message.get_full_identificator()
        )


"Начать тестирование"
"Зарефакторить шаблоны"
"Зарефакторить код"
