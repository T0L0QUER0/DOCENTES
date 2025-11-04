from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import DocenteForm, DocenteEdit 
from django.shortcuts import render, get_object_or_404
from .models import Docente, Division, ProgramaEducativo, AreaConocimiento
from datetime import date
 

def login(request):
    if request.method == 'POST':
        return redirect('home')
    return render(request, 'login.html')

def recup_pass(request):
    return render(request, 'recup_pass.html')

# app/views.py

def home(request):
    hoy = date.today()

    #filtros
    filtros = {}
    puesto_seleccionado = request.GET.get('puesto', '')
    perfil_seleccionado = request.GET.get('perfil', '')

    if puesto_seleccionado:
        filtros['Puesto'] = puesto_seleccionado
    
    if perfil_seleccionado:
        filtros['Perfil'] = perfil_seleccionado 

    docentes_qs = Docente.objects.filter(**filtros).select_related('division').order_by('ApellidoP')
    
    # Antiguedad
    docentes_con_antiguedad = []
    for docente in docentes_qs:
        antiguedad_anios = hoy.year - docente.FechaIngreso.year
        if (hoy.month, hoy.day) < (docente.FechaIngreso.month, docente.FechaIngreso.day):
            antiguedad_anios -= 1
        docente.antiguedad = antiguedad_anios
        docentes_con_antiguedad.append(docente)
        
    opciones_puesto = Docente.objects.values_list('Puesto', flat=True).distinct()
    opciones_perfil = Docente.Perfil.field.choices 
    
    context = {
        'docentes': docentes_con_antiguedad,
        'opciones_puesto': opciones_puesto,
        'opciones_perfil': opciones_perfil,
        

        'puesto_seleccionado': puesto_seleccionado,
        'perfil_seleccionado': perfil_seleccionado,
    }
    
    return render(request, 'home.html', context)

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

def edicion_docente(request, clave_docente):
    # 1. Obtener el objeto Docente o devolver un 404 si no existe
    docente = get_object_or_404(Docente, claveDocente=clave_docente)

    if request.method == 'POST':
        # Cuando se envía el formulario:
        # Instanciar el formulario con los datos POST y la instancia del docente existente
        form = DocenteForm(request.POST, instance=docente)
        
        if form.is_valid():
            # El form.save() actualiza la instancia existente
            form.save()
            # Redirigir a la vista principal después de guardar
            return redirect('home')  
    else:
        # Cuando se carga la página (GET):
        # Instanciar el formulario con los datos del docente existente
        form = DocenteForm(instance=docente)

    context = {
        'form': form,
        'docente': docente,
    }
    return render(request, 'edicion_docente.html', context)
 