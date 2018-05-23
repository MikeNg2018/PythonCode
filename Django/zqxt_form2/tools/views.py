from django.shortcuts import render
from django.http import HttpResponse
from .form import AddForm

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = AddForm(request.POST)

        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
    else:
        form = AddForm()

    return render(request, 'index.html', {'form': form})
