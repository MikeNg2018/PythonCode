from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# def home(request):
#     string = "测试Django"
#     return render(request, 'learn/home.html', {'string': string})

def home(request):
    TutorialList = ['HTML', "CSS", "Python", "Django"]
    var = 80
    return render(request, 'learn/home.html', {'var': var, 'TutorialList': TutorialList})


def add(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))
