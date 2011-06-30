from django.contrib import admin
from postman.models import Subscription, MailingList, Message

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed', 'created_on',)
    search_fields = ('email',)
    list_filter = ('subscribed',)

class MailingListAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated_on',)
    search_fields = ('title', 'subscribers',)
    filter_horizontal = ('subscribers',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject', 'status',)
    search_fields = ('subject', 'body',)
    list_filter = ('status',)
    actions = ['send_message']
    def send_message(self, request, queryset):
        from django.core.mail import send_mail
        num_recipients = 0
        # for each message in queryset (could select multiple)
        for message in queryset:
            # iterate through recipients and send an email
            for mailing_list in message.recipients.all():
                for subscriber in mailing_list.subscribers.all():
                    num_recipients += 1
                    print "Sending %s to %s" % (message.subject,
                            subscriber.email)
                    #send_mail(message.subject, message.body_html,
                    #        message.from_email, [subscriber.email],
                    #        fail_silently=False)
        # mark messages as sent
        messages_sent = queryset.update(status='S')
        if messages_sent == 1:
            message_bit = "1 message was"
        else:
            message_bit = "%s messages were" % messages_sent
        self.message_user(request, "%s successfully sent to a total of %d recipients."
                % (message_bit, num_recipients))

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MailingList, MailingListAdmin)
