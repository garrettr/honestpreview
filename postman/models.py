from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.hashcompat import sha_constructor

from markdown import markdown

from datetime import datetime
import random

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
    deactivation_code = models.CharField(_('deactivation code'), max_length=40,
            editable=False, default=make_activation_code)

    class Meta:
        abstract = True
        ordering = ('email',)

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
        if self.subscribed == False:
            self.mailinglists.clear()
        super(Subscription, self).save()

class MailingList(models.Model):
    title = models.CharField(_('title'), max_length=200)
    subscribers = models.ManyToManyField(Subscription,
        related_name="mailinglists", blank=True,
        limit_choices_to = {'subscribed': True})
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    # note: limit_choices_to only controls what's shown in the admin
    # if front-facing unsubscription code isn't work, the admin paints an
    # unreliable picture of what the database looks like

    def __unicode__(self):
        return u'%s' % (self.title)

class Message(models.Model):
    '''
    Allows you to write e-mail messages to the list using Markdown;
    saves them in a database
    '''
    # try to import default from_email
    try:
        from settings import DEFAULT_FROM_EMAIL
    except ImportError:
        DEFAULT_FROM_EMAIL=''

    from_email = models.CharField(_('email'), max_length=200,
            help_text=_('Sender e-mail'), default=DEFAULT_FROM_EMAIL)
    sender = models.CharField(_('sender'), max_length=200,
            help_text=_('Sender name'), default="Honest Appalachia")
    subject = models.CharField(blank=False, max_length=140)
    body = models.TextField()
    body_html = models.TextField(editable=False, blank=True)

    recipients = models.ManyToManyField(MailingList, blank=True)

    STATUS_CHOICES = (
        (u'D', u'Draft'),
        (u'S', u'Sent'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
            default='D', blank=False)

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.subject)

    def save(self, *args, **kwargs):
        self.body_html = markdown(self.body)
        self.body_html = "<html>" + self.body_html + "</html>"
        super(Message, self).save(*args, **kwargs)
