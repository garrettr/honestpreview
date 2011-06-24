from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.hashcompat import sha_constructor

from markdown import markdown

import datetime

# Code taken liberally from
# https://github.com/howiworkdaily/django-newsletter
# and
# https://github.com/dokterbob/django-newsletter/

def make_activation_code():
    return sha_constructor(sha_constructor(str(random.random())).hexdigest()[:5]+str(datetime.now().microsecond)).hexdigest()

class SubscriptionBase(models.Model):
    '''
    Abstract base class for Subscription
    Ask: what does this actually do for us?
    '''
    subscribed = models.BooleanField(_('subscribed'), default=True)
    email = models.EmailField(_('email'), unique=True)
    created_on = models.DateField(_('created on'), blank=True)
    updated_on = models.DateField(_('updated on'), blank=True)
    #activation_code = models.CharField(_('activation code'), max_length=40,
    #        default=make_activation_code)

    class Meta:
        abstract = True

    @classmethod
    def is_subscribed(cls, email):
        try:
            return cls.objects.get(email=email).subscribed
        except cls.DoesNotExist, e:
            return False

    def __unicode__(self):
        return u'%s' % (self.email)

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.date.today()
        self.updated_on = datetime.date.today()
        super(SubscriptionBase,self).save(*args, **kwargs)

class Subscription(SubscriptionBase):
    '''
    Subscription
    '''
    def save(self, *args, **kwargs):
        super(Subscription, self).save()

class Message(models.Model):
    '''
    Allows you to write e-mail messages to the list using Markdown;
    saves them in a database
    '''
    email = models.CharField(_('email'), max_length=200, help_text=_('Sender e-mail'))
    sender = models.CharField(_('sender'), max_length=200, help_text=_('Sender name'))
    subject = models.CharField(blank=False, max_length=140)
    body = models.TextField(help_text=_('Supports Markdown'))
    body_html = models.TextField(editable=False, blank=True)

    STATUS_CHOICES = (
        (u'D', u'Draft'),
        (u'S', u'Sent'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __unicode__(self):
        return u'%s, from %s' % (self.subject, self.sender)

    def save(self, *args, **kwargs):
        self.body_html = markdown(self.body)
        super(Message, self).save(*args, **kwargs)
