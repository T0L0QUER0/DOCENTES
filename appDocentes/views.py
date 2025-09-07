from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

def login(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'login.html')

def home(request):
    if request.method == 'POST':
        return redirect('registro')
    return render (request, 'home.html')

def registro(request):
    return render (request, 'registro.html')
 