from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    message = "Helllo from View"
    return render(request, 'main/home.html', {'message': message})
