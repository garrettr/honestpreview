from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from postman.forms import SubscribeForm

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

