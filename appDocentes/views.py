from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#Vistas

def login(request):
    return render (request, 'login.html')
