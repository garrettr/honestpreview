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
        # for each message in queryset (could select multiple)
        for message in queryset:
            # iterate through recipients and send an email
            for mailing_list in message.recipients.all():
                for subscriber in mailing_list.subscribers.all():
                    print "Sending %s to %s" % (message.subject,
                            subscriber.email)
                    #send_mail(message.subject, message.body_html,
                    #        message.from_email, [subscriber.email],
                    #        fail_silently=False)
            # mark message as sent
            message.status = 'S'
            message.save()



admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MailingList, MailingListAdmin)
