from django.core.mail import send_mail
from postman.models import Subscription, Message

def send_confirmation_email():
    pass

def subscribe(email):
    '''
    Add a Subscription for email, if one does not already exist
    '''
    try:
        s = Subscription.objects.get(email=email)
        if s.subscribed == False:
            s.subscribed = True
            s.save()    #resubscribe
        # you're already subscribed
    except:
        s = Subscription(email = email,)
        s.save()

def unsubscribe(email):
    '''
    Unsubscribe an email from the list; return False if they were not
    unsubscribed (meaning they weren't subscribed in the first place)
    '''
    try:
        s = Subscription.objects.get(email=email)
        s.subscribed = False
        s.save()
    except:
        return False
