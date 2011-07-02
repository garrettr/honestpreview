from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
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

def unsubscribe(request, code):
    '''
    Unsubscribe an email from the list; return False if they were not
    unsubscribed (meaning they weren't subscribed in the first place)
    '''
    try:
        s = Subscription.objects.get(deactivation_code=code)
        s.subscribed = False
        s.save()
        return HttpResponseRedirect('/newsletter/unsubscribe/confirmation/%d/' %
                s.pk)
    except:
        return HttpResponseRedirect('/newsletter/unsubscribe/error/%d/' % s.pk)

def unsubscribe_confirm(request, id):
    s = Subscription.objects.get(pk=id)
    message = "%s has been removed from the Honest Appalachia mailing list." % s.email
    return render_to_response('postman/unsubscribe_confirm.html',
            {
                'message': message,
            },
            context_instance=RequestContext(request)
        )

def unsubscribe_error(request, id):
    try:
        s = Subscription.objects.get(pk=id)
        message = "An error occurred while trying to remove %s from the mailing list." % s.email
    except:
        message = "Something went horribly wrong."
    return render_to_response('postman/unsubscribe_error.html',
            {
                'message': message,
            },
            context_instance=RequestContext(request)
        )
