from django.urls import re_path, path
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from lostflag.parser import countryCodes
import requests_async as requests
from decouple import config
import time, re
import urllib.parse
import asyncio

FLAG = config('FLAG')
DOMAIN_URL = config('DOMAIN_URL')
ADMIN_TOKEN = config('ADMIN_COOKIE')
REGEX = config('REGEX')
cookies = {'secretAuth': ADMIN_TOKEN}


# ---------------- ROUTING FUNCTIONS ---------------------

def flag(request: HttpRequest):
    token = request.COOKIES.get("secretAuth")
    path = urllib.parse.urlparse(request.path).path
    if not token or token != ADMIN_TOKEN:
        return render(request, 'flag.html', {'data': "Only admin can view this!"})
    
    if bool(re.match(REGEX, request.path[1:])):
        return render(request, 'flag.html', {'data': FLAG})
    else:
        if path.endswith(".css") or path.endswith(".js") or path.endswith(".html") or path.endswith(".txt"):
            return render(request, 'warning.html', {'data': "You are missing few characters in endpoint and those charaters should satisfy what a strong password contains. [ example: ^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[?!@$%^&*-]).{8,}$ ]"})
        else:
            return render(request, 'warning.html', {'data': 'Need an extension for this route (.html, .js, .css, .txt)'})

def countryFlag(request, cName):
    countryDetails = countryCodes(cName.replace(' ', '').lower())
    if countryDetails != 0:
        return render(request, 'country.html',{'countryDetails':countryDetails})
    return HttpResponse('Not Found')

async def report(request: HttpRequest):
    if request.method == 'POST':
        reportedEndpoint = str(request.POST['endpoint']).strip()
        URL = str()
        if reportedEndpoint.startswith('/'):
            URL = DOMAIN_URL+reportedEndpoint[1:]
        else:
            URL = DOMAIN_URL+reportedEndpoint
        await requests.get(URL, cookies=cookies)
        return render(request, 'reports.html', {'data':'Noted by Casshe.'})
    
    return render(request, 'reports.html', {'data':''})

def index(request: HttpRequest):
    if request.method == 'POST':
        cName = str(request.POST['countryname']).strip()
        return redirect(countryFlag, cName)
    return render(request, 'index.html', {})