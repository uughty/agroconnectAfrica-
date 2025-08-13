from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to Agroconnect</h1>")
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

