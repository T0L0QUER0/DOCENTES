from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import DocenteForm, DocenteEdit, ProyectoInvestigacionForm
from django.shortcuts import render, get_object_or_404
from .models import Docente, Division, ProgramaEducativo, AreaConocimiento, Proyectos
from datetime import date
from django.db import IntegrityError

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




def lista_proyectos(request):
    proyectos = Proyectos.objects.all()
    context = {
        'proyectos': proyectos,
        'titulo': 'Proyectos de Investigación'
    }
    return render(request, 'proyectos.html', context)


def agregar_proyecto_general(request):
    """Muestra el formulario para agregar un proyecto, incluyendo la selección del docente y colaboradores."""
    
    if request.method == 'POST':
        form = ProyectoInvestigacionForm(request.POST) # <--- Usando ProyectosForm
        if form.is_valid():
            try:
                # 1. Guardar la instancia (SIN guardar la relación Muchos a Muchos aún)
                proyecto = form.save(commit=False)
                
                # 2. Guardar la instancia principal (Ejecuta el .save() con la lógica del ID Compuesto)
                proyecto.save()
                
                # 3. Guardar la lista de Colaboradores (Muchos a Muchos)
                form.save_m2m() # ¡Paso necesario para ManyToManyField!
                
                return redirect('lista_proyectos') 
                
            except IntegrityError:
                # Error en caso de clave primaria duplicada (ID_Compuesto)
                form.add_error(None, "Ya existe un proyecto con ese ID base para el Docente Líder seleccionado.")
    
        # Si no es válido o hay IntegrityError, se renderiza el formulario con errores
    else:
        form = ProyectoInvestigacionForm() # <--- Usando ProyectosForm

    context = {
        'form': form,
        'titulo': "Agregar Nuevo Proyecto",
    }
    return render(request, 'agregar_proyecto.html', context)



def editar_proyecto(request, pk):
    """
    Permite editar un proyecto existente.
    Recibe el pk (ID_Compuesto) del proyecto.
    """
    # Recupera la instancia del proyecto, si no existe lanza un 404
    proyecto = get_object_or_404(Proyectos, ID_Compuesto=pk)
    if request.method == 'POST':
        # Inicializa el formulario con los datos POST y la instancia existente
        form = ProyectoInvestigacionForm(request.POST, instance=proyecto)
        if form.is_valid():
            try:
                # 1. Guarda la instancia sin guardar la relación ManyToMany (Colaboradores)
                proyecto_editado = form.save(commit=False)
                
                # NOTA: No es necesario llamar a proyecto_editado.save() aquí 
                # si no cambias el claveDocente/IdProyecto_Base, pero lo haremos por seguridad
                proyecto_editado.save()
                # 2. Guarda la relación Muchos a Muchos (Colaboradores)
                form.save_m2m() 
                # Redirige a la lista de proyectos después de la edición exitosa
                return redirect('lista_proyectos')
            except IntegrityError:
                # Esto maneja si la edición genera un ID_Compuesto duplicado
                form.add_error(None, "La combinación de Docente Líder e ID Base ya existe en otro proyecto.")
    else:
        # Método GET: Inicializa el formulario con la instancia actual del proyecto
        form = ProyectoInvestigacionForm(instance=proyecto)
    context = {
        'form': form,
        'titulo': f"Editar Proyecto: {proyecto.ID_Compuesto}",
        'es_edicion': True # Flag para posibles ajustes en la plantilla
    }
    # Reutilizamos la misma plantilla de formulario
    return render(request, 'agregar_proyecto.html', context)



def eliminar_proyecto(request, pk):
    """
    Elimina un proyecto de investigación. 
    Busca la instancia por el ID_Compuesto (pk) y la elimina si el método es POST.
    """
    # 1. Recuperar la instancia (falla con 404 si no existe)
    proyecto = get_object_or_404(Proyectos, ID_Compuesto=pk)

    # 2. Manejar la eliminación (solo con POST)
    if request.method == 'POST':
        proyecto.delete()
        # Redirige a la lista después de la eliminación
        return redirect('lista_proyectos')
    
    # Para el caso de que alguien intente acceder a esta URL con GET, simplemente redirigimos.
    # Si quisieras una página de confirmación separada, aquí renderizarías ese HTML.
    return redirect('lista_proyectos')