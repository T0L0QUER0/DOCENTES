from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import DocenteForm 

def login(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'login.html')

def recup_pass(request):
    return render(request, 'recup_pass.html')

def home(request):
    return render (request, 'home.html')

# def registro(request):
#     if request.method == 'POST':
#         return redirect('home')
#     return render (request, 'registro.html')

def registro(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            docente_guardado = form.save()
            return redirect('home') # Debes definir esta URL
        else:
            print(form.errors) # Muestra los errores en la consola del servidor
            
    else:
        form = DocenteForm()
    contexto = {
        'form': form
    }
    return render(request, 'registro.html', contexto) 
 