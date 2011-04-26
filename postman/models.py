from django.db import models

# Create your models here.

class MailingList(models.Model):
    name = models.CharField(max_length=100, blank=False)

class Subscriber(models.Model):
    email = models.EmailField()
    to = models.ForeignKey(MailingList)
