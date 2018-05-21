from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'home.html')


def add(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def multiply(request, a, b):
    c = int(a) * int(b)
    return HttpResponse(str(c))


