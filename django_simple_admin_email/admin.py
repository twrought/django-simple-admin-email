from django.contrib import admin
from django.shortcuts import render
from django.core.mail import send_mass_mail
from django.http import HttpResponseRedirect
from django.core.exceptions import ViewDoesNotExist
from django.conf import settings

from .forms import SendEmailForm
from .models import Email

# Email Model Admin

class EmailPage(admin.ModelAdmin):
    list_display = (
        'date',
        'subject',
        'body',
    )
    actions = ['start_mail_send', 'confirm_mail_send']

# Simple Mailer Actions

# Start process of selecting menu and sending to all recipients

    def start_mail_send(self, request, queryset):
        if request.method == 'POST':
            email_list = []
            for item in queryset:
                email_list.append(item)
            u_form = SendEmailForm(request.POST)
            context = {
                'u_form': u_form,
                'email_list': email_list
            }
            return render(request, 'email_select.html', context)
        else:
            raise ViewDoesNotExist('Only POST requests are allowed')

    start_mail_send.short_description = 'Start Mail Send'

# Send individual main to each selected recipient

    def confirm_mail_send(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = SendEmailForm(request.POST)
            if form.is_valid():
                recipients = form.cleaned_data['recipients']
                email_subject = request.POST.get('email_list_subject')
                email_body = request.POST.get('email_list_body')
                message_bit = "%s emails were" % len(recipients)
                message_list = []   
                for item in recipients:
                    message = (email_subject, 
                    email_body, 
                    settings.EMAIL_HOST_USER, 
                    [item.email])
                    message_list.append(message)
                for item in message_list:
                    send_mass_mail((message_list), fail_silently=False)
                self.message_user(request, "%s successfully emailed." % message_bit)
                return HttpResponseRedirect('/admin/django_simple_admin_email/email/')
        else:
            raise ViewDoesNotExist('Only POST requests are allowed')

    confirm_mail_send.short_description = 'Confirm Mail Send'

admin.site.register(Email, EmailPage)
