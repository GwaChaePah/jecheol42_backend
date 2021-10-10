from django.http import HttpResponse
from django.shortcuts import render
import requests


def index(request):
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
