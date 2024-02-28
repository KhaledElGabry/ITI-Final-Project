from django.shortcuts import render
from django.http import HttpRequest , HttpResponse

# Create your views here.
def theme(request):
    return HttpResponse("Hello World")