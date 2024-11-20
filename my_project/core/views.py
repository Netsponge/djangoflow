# views.py
# This is the views file for the core directory

#from django.http import HttpResponse
from django.shortcuts import render


def homepage(request):
    #return HttpResponse("Home.")
    return render(request, 'home.html')

def about(request):
    #return HttpResponse("About page.")
    return render(request, 'about.html')

