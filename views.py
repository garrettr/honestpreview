from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404

from postman.forms import SubscribeForm
from postman.models import MailingList, Subscriber

CURRENTML = "hpdev"

def home(request):
    '''
    Display home.html with mailing list subscribe form
    '''
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            # do stuff
            # redirect
            return HttpResponseRedirect('/thanks/')
    else:
        form = SubscribeForm()

    return render_to_response('home.html',
            {
                'form': form,
            },
            context_instance=RequestContext(request)
        )

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def validate_signup(request):
    '''Validates signup POSTed via AJAX - disallows any other input'''
    if request.is_ajax() and request.method == "POST":
        # check that POSTed data is good, generate a response
        message = "<p>Thanks for signing up!</p>"
        return HttpResponse(message)
    else:
        raise Http404
