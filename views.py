from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.http import Http404

from postman.forms import SubscribeForm
from postman.views import subscribe, unsubscribe

def home(request):
    '''
    Display home.html with mailing list subscribe form
    '''
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            # Gather what's needed 
            email = form.cleaned_data['email']
            subscribe(email)
            return HttpResponseRedirect('/thanks/')
    else:
        form = SubscribeForm()

    return render_to_response('home.html',
            {
                'form': form,
            },
            context_instance=RequestContext(request)
        )

def signup_thanks(request):
    '''
    Redirects to a simple thank you page.
    Needed in casse a user signs up without using Javascript
    '''
    return render_to_response('thanks.html', {},
            context_instance=RequestContext(request)
        )

def validate_signup(request):
    '''
    Validates signup POSTed via AJAX - disallows any other input
    '''
    if request.is_ajax() and request.method == "POST":
        # check that POSTed data is good, generate a response
        # Gather what's needed 
        email = request.POST['email']
        subscribe(email)
        message = "<p>Thanks for signing up!</p>"
        return HttpResponse(message)
    else:
        raise Http404
