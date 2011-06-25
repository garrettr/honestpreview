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
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)
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

class Subscription(SubscriptionBase):
    '''
    Subscription
    '''
    def save(self, *args, **kwargs):
        super(Subscription, self).save()

class MailingList(models.Model):
    title = models.CharField(_('title'), max_length=200)
    subscribers = models.ManyToManyField(Subscription,
        related_name="mailing_list", blank=True)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.title)

class Message(models.Model):
    '''
    Allows you to write e-mail messages to the list using Markdown;
    saves them in a database
    '''
    from_email = models.CharField(_('email'), max_length=200, help_text=_('Sender e-mail'))
    sender = models.CharField(_('sender'), max_length=200, help_text=_('Sender name'))
    subject = models.CharField(blank=False, max_length=140)
    body = models.TextField(help_text=_('Supports Markdown'))
    body_html = models.TextField(editable=False, blank=True)

    recipients = models.ManyToManyField(MailingList, blank=True)

    STATUS_CHOICES = (
        (u'D', u'Draft'),
        (u'S', u'Sent'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return u'%s, from %s' % (self.subject, self.sender)

    def save(self, *args, **kwargs):
        self.body_html = markdown(self.body)
        super(Message, self).save(*args, **kwargs)
