from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from makematter_server.models import MatterTemplate, MatterTemplateVar


def index(request):
    return render_to_response('index.html')
