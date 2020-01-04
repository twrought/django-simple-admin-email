from django.contrib import admin
from django.shortcuts import render
from django.core.mail import send_mail
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
                recipients = []
                failure_list = []
                unfiltered_rec = form.cleaned_data['recipients']
                for item in unfiltered_rec:
                    if item.email:
                        recipients.append(item.email)
                    else: 
                        failure_list.append(item.username)
                email_subject = request.POST.get('email_list_subject')
                email_body = request.POST.get('email_list_body')
                for item in recipients:
                    lst = [item]
                    send_mail(subject=email_subject,
                        message=email_body, from_email=settings.EMAIL_HOST_USER,
                        recipient_list=lst)
                failure_message_bit = "%s emails were" % len(failure_list)
                success_message_bit = "%s emails were" % len(recipients)
                self.message_user(request, "%s successfully emailed." % success_message_bit)
                self.message_user(request, "%s unsuccessfully sent. No email addresses for these users:" % failure_message_bit)
                self.message_user(request, failure_list)
                return HttpResponseRedirect('/admin/django_simple_admin_email/email/')
        else:
            raise ViewDoesNotExist('Only POST requests are allowed')

    confirm_mail_send.short_description = 'Confirm Mail Send'

admin.site.register(Email, EmailPage)
