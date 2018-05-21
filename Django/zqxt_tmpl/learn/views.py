from django.shortcuts import render

# Create your views here.


# def home(request):
#     string = "测试Django"
#     return render(request, 'learn/home.html', {'string': string})

def home(request):
    TutorialList = ['HTML', "CSS", "Python", "Django"]
    return render(request, 'learn/home.html', {'TutorialList': TutorialList})


