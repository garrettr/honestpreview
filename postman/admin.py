from django.contrib import admin
from postman.models import Subscription, Message

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed', 'created_on',)
    search_fields = ('email',)
    list_filter = ('subscribed',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject', 'status',)
    search_fields = ('subject', 'body',)
    list_filter = ('status',)

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Message, MessageAdmin)
