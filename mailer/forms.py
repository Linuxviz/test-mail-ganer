from django import forms

from .models import Subscriber, SubscribersGroup, SubscribersCollection, EmailTemplate, PushAction


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = (
            'email_address',
            'name',
            'second_name',
            'birthday',
            'group',
        )


class EmailTemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ('name', 'body')


class SubscribersForm(forms.ModelForm):
    class Meta:
        model = SubscribersCollection
        fields = ('group_name', 'upload_file')


class PushActionForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(PushActionForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = EmailTemplate.objects.filter(user=user)
        self.fields['pushed_group'].queryset = SubscribersGroup.objects.filter(user=user)

    class Meta:
        model = PushAction
        fields = ('template', 'subject', 'pushed_group', 'delay_time')
