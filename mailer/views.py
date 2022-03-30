# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os.path

import magic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView

from core.settings import ALLOWED_FILE_EXTANTIONS_FOR_SUBSCRIBERS_UPLOAD
from .forms import SubscriberForm, SubscribersForm, PushActionForm, EmailTemplateForm
from .mailer import is_valid_template
from .models import Subscriber, SubscribersCollection, SubscribersGroup, PushAction, PushedMessage, EmailTemplate
from .reader import FileReader
from .tasks import push_mails_task

logger = logging.getLogger(__name__)
reader = FileReader()


class SubscriberListView(LoginRequiredMixin, ListView):
    # TODO сделать переключение страниц возможно перевести списки в табличный вид
    paginate_by = 20
    model = Subscriber
    template_name = 'subscriber_list.html'

    def get_queryset(self):
        user = self.request.user
        return Subscriber.objects.filter(active=True, user=user).prefetch_related('group')


@login_required
def add_subscriber(request):
    """Add single subscriber view"""
    form = SubscriberForm()
    context = {'form': form}
    if request.method == 'POST':
        bound_form = SubscriberForm(request.POST)
        if bound_form.is_valid():
            try:
                objs = Subscriber.objects.filter(email_address=bound_form.cleaned_data['email_address'])
                if len(objs) > 0:
                    context = {'form': bound_form}
                    return render(request, 'add_subscriber.html', context=context)

                subscriber = Subscriber.objects.create(
                    email_address=bound_form.cleaned_data['email_address'],
                    name=bound_form.cleaned_data['name'],
                    second_name=bound_form.cleaned_data['second_name'],
                    birthday=bound_form.cleaned_data['birthday'],
                    user=request.user,
                )
                groups = bound_form.cleaned_data['group']
                for group in groups:
                    subscriber.group.add(group)

                return redirect('main_page')
            except Exception as e:
                form.add_error(None, 'Ошибка добавления подписчика')
        context = {'form': bound_form}
    return render(request, 'add_subscriber.html', context=context)


@login_required
def add_subscribers(request):
    """Add many subscribers from file view"""
    form = SubscribersForm()
    context = {'form': form}
    if request.method == 'POST':
        bound_form = SubscribersForm(request.POST, request.FILES)
        if bound_form.is_valid():
            extantion = get_extantion(request.FILES['upload_file'])
            if not extantion:
                form.add_error(None, 'Ошибка добавления не распозналось раширение')
            if not is_allowed_extantion(extantion):
                form.add_error(None, 'Неверное расширение')
            group = SubscribersGroup.objects.create(
                name=bound_form.cleaned_data['group_name'],
                user=request.user,
            )
            subscribers_collection = SubscribersCollection(
                upload_file=request.FILES['upload_file'],
                group=group,
                group_name=bound_form.cleaned_data['group_name']
            )
            subscribers_collection.save()
            subscribers_list = reader.read(subscribers_collection.upload_file)
            obj_subscribers_list = []
            for item in subscribers_list:
                obj = Subscriber(
                    email_address=item['email_address'],
                    name=item.get('name'),
                    second_name=item.get('second_name'),
                    birthday=item.get('birthday'),
                    user=request.user,
                )
                obj_subscribers_list.append(obj)
            subs = Subscriber.objects.bulk_create(obj_subscribers_list)
            # TODO В этом месте можно сильно оптимизировать код используя
            #  bukl_create для промежуточной таблицы
            for sub in subs:
                sub.group.add(group.pk)
            return redirect('main_page')
        context = {'form': bound_form}
    return render(request, 'add_subscribers.html', context=context)


@login_required
def push_mails(request):
    """ Post mails with one template all of groups members view """
    form = PushActionForm(user=request.user)
    context = {'form': form}
    if request.method == 'POST':
        bound_form = PushActionForm(data=request.POST, user=request.user)
        if bound_form.is_valid():
            try:
                template = bound_form.cleaned_data['template']
                subject = bound_form.cleaned_data['subject']
                group = bound_form.cleaned_data['pushed_group']
                delay_time = bound_form.cleaned_data['delay_time']

                push_action = PushAction.objects.create(
                    template=template,
                    subject=subject,
                    pushed_group=group,
                    delay_time=delay_time,
                )

                if push_action.delay_time is not None:
                    push_mails_task.apply_async((push_action.pk,), eta=push_action.delay_time)
                else:
                    push_mails_task.apply_async((push_action.pk,), countdown=5)

                return redirect('main_page')
            except Exception as e:
                logger.exception('Error in push_mails')
                form.add_error(None, 'Ошибка отправки писем')
        context = {'form': bound_form}
    return render(request, 'push_mails.html', context=context)


@login_required
def add_template(request):
    """ Add template view """
    form = EmailTemplateForm()
    context = {'form': form}
    if request.method == 'POST':
        bound_form = EmailTemplateForm(request.POST, request.FILES)
        if bound_form.is_valid():
            extantion = get_extantion(request.FILES['body'])
            if not extantion:
                bound_form.add_error(None, 'Ошибка добавления не распозналось раширение')
            if extantion != 'text/html':
                bound_form.add_error(None, 'Неверное расширение')
            template = EmailTemplate(
                body=request.FILES['body'],
                name=bound_form.cleaned_data['name'],
                user=request.user
            )
            template.save()
            if is_valid_template(template.body.name):
                return redirect('main_page')
            bound_form.add_error(None, 'Ошибка добавления в шаблоне есть {%%}, файл не будет сохранен')
            template.body.delete(False)
            template.delete()
            context = {'form': bound_form}
            return render(request, 'add_subscribers.html', context=context)
        context = {'form': bound_form}
    return render(request, 'add_template.html', context=context)


def email_identificator(request, pushed_email_identificator):
    """ Counting and check time first open mail view """
    if pushed_email_identificator:
        ident = pushed_email_identificator[0:36]
        id = pushed_email_identificator[36:]
        message = get_object_or_404(PushedMessage, identificator=ident, pk=int(id))
        message.view_count += 1
        if not message.first_view_data:
            message.first_view_data = timezone.now()
        message.save()
        with open('mailer/templates/general_pixel/general_pixel.jpg', "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")


def is_allowed_extantion(extantion):
    if extantion in ALLOWED_FILE_EXTANTIONS_FOR_SUBSCRIBERS_UPLOAD:
        return True
    return False


def get_extantion(file_obj):
    try:
        extantion = magic.Magic(mime=True).from_buffer(file_obj.read())
    except:
        extantion = None
    return extantion
