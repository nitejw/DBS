from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
import requests

def index(request):
    user = authenticate(username='marytan', password='marypassword')
    if user is not None:
        return HttpResponse('OK')
    else:
        # No backend authenticated the credentials
        return HttpResponse('NOK')

def userHome(request):
    return HttpResponse('login')