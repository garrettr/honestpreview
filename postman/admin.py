from django.contrib import admin
from postman.models import MailingList, Subscriber

class MailingListAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'active', 'to',)

admin.site.register(MailingList, MailingListAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
