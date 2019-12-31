from django.db import models

# Create your models here.

class Email(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    body = models.TextField(max_length=5000, null=True, default=None, blank=True)
    subject = models.TextField(max_length=250, null=True, default=None, blank=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

    def __str__(self):
        return str(self.subject)