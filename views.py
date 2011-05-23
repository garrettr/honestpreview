from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

def home(request):
    '''
    Display basic page, home.html
    '''
    return render_to_response('home.html', {})

