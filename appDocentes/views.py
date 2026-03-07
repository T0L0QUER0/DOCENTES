from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import DocenteForm, DocenteEdit, ProyectoInvestigacionForm, CedulasForm
from django.shortcuts import render, get_object_or_404
from .models import Docente, Division, ProgramaEducativo, AreaConocimiento, Proyectos, Cedulas
from datetime import date, datetime
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user) 
            return redirect('home')
        else:
            error_message = "Credenciales incorrectas o cuenta inactiva."
            return render(request, 'login.html', {'error': error_message})
    return render(request, 'login.html')

def logout_usuario(request):
    logout(request)
    return redirect('login')

def recup_pass(request):
    return render(request, 'recup_pass.html')

# app/views.py
@never_cache
@login_required
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

@never_cache
@login_required
def registro(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            docente_guardado = form.save()
            messages.success(request, f'El docente {Docente.Nombre} {Docente.ApellidoP} ha sido registrado correctamente.')
            return redirect('home') # Debes definir esta URL
        else:
            print(form.errors) # Muestra los errores en la consola del servidor
            
    else:
        form = DocenteForm()
    contexto = {
        'form': form
    }
    return render(request, 'registro.html', contexto)

@never_cache
@login_required
def edicion_docente(request, clave_docente):
    # 1. Obtener el objeto Docente o devolver un 404 si no existe
    docente = get_object_or_404(Docente, claveDocente=clave_docente)

    if request.method == 'POST':
        # Cuando se envía el formulario:
        # Instanciar el formulario con los datos POST y la instancia del docente existente
        form = DocenteEdit(request.POST, instance=docente)
        
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
 @never_cache
@login_required
def lista_proyectos(request):
    proyectos = Proyectos.objects.all()
    context = {
        'proyectos': proyectos,
        'titulo': 'Proyectos de Investigación'
    }
    return render(request, 'proyectos.html', context)

@never_cache
@login_required
def agregar_proyecto(request): # <-- Quitamos clave_docente de aquí
    if request.method == 'POST':
        form = ProyectoInvestigacionForm(request.POST)
# En views.py, dentro de agregar_proyecto
        if form.is_valid():
            proyecto = form.save(commit=False)
            docente_lider = form.cleaned_data['claveDocente']
            
            # Buscamos el último proyecto para el contador
            ultimo_p = Proyectos.objects.filter(claveDocente=docente_lider).order_by('-IdProyecto_Base').first()
            
            nuevo_numero = "01"
            if ultimo_p and ultimo_p.IdProyecto_Base:
                prefijo = ultimo_p.IdProyecto_Base[:2]
                if prefijo.isdigit():
                    nuevo_numero = str(int(prefijo) + 1).zfill(2)

            mes_anio = datetime.now().strftime('%m%Y')
            
            # Esta es tu nueva llave primaria única
            proyecto.IdProyecto_Base = f"{nuevo_numero}{mes_anio}PDI-{docente_lider.claveDocente}"
            
            proyecto.save()
            form.save_m2m() # Esto ahora guardará en la tabla de colaboradores usando el nuevo ID
            return redirect('lista_proyectos')
    else:
        form = ProyectoInvestigacionForm()
    
    return render(request, 'agregar_proyecto.html', {'form': form, 'titulo': 'Agregar Proyecto'})

@never_cache
@login_required
def editar_proyecto(request, pk):
    """
    Permite editar un proyecto existente.
    Recibe el pk (IdProyecto_Base) del proyecto.
    """
    # Recupera la instancia del proyecto, si no existe lanza un 404
    proyecto = get_object_or_404(Proyectos, IdProyecto_Base=pk)
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
                # Esto maneja si la edición genera un IdProyecto_Base duplicado
                form.add_error(None, "La combinación de Docente Líder e ID Base ya existe en otro proyecto.")
    else:
        # Método GET: Inicializa el formulario con la instancia actual del proyecto
        form = ProyectoInvestigacionForm(instance=proyecto)
    context = {
        'form': form,
        'titulo': f"Editar Proyecto: {proyecto.IdProyecto_Base}",
        'es_edicion': True # Flag para posibles ajustes en la plantilla
    }
    # Reutilizamos la misma plantilla de formulario
    return render(request, 'agregar_proyecto.html', context)

@never_cache
@login_required
def eliminar_proyecto(request, pk):
    """
    Elimina un proyecto de investigación. 
    Busca la instancia por el IdProyecto_Base (pk) y la elimina si el método es POST.
    """
    # 1. Recuperar la instancia (falla con 404 si no existe)
    proyecto = get_object_or_404(Proyectos, IdProyecto_Base=pk)

    # 2. Manejar la eliminación (solo con POST)
    if request.method == 'POST':
        proyecto.delete()
        # Redirige a la lista después de la eliminación
        return redirect('lista_proyectos')
    
    # Para el caso de que alguien intente acceder a esta URL con GET, simplemente redirigimos.
    # Si quisieras una página de confirmación separada, aquí renderizarías ese HTML.
    return redirect('lista_proyectos')

@never_cache
@login_required
def lista_cedulas(request, clave_docente):
    docente = get_object_or_404(Docente, claveDocente=clave_docente)
    cedulas = Cedulas.objects.filter(claveDocente=docente)
    return render(request, 'lista_cedulas.html', {
        'docente': docente, 
        'cedulas': cedulas
    })

# 2. AGREGAR CÉDULA
@never_cache
@login_required
def agregar_cedula(request, clave_docente):
    docente = get_object_or_404(Docente, claveDocente=clave_docente)
    if request.method == 'POST':
        form = CedulasForm(request.POST)
        if form.is_valid():
            cedula = form.save(commit=False)
            cedula.claveDocente = docente # Asignamos el docente automáticamente
            cedula.save()
            messages.success(request, f'¡La cédula {cedula.id_cedula} se ha registrado con éxito!')
            return redirect('lista_cedulas', clave_docente=clave_docente)
    else:
        # Iniciamos el formulario con el docente ya seleccionado
        form = CedulasForm(initial={'claveDocente': docente})
    
    return render(request, 'agregar_cedula.html', {'form': form, 'docente': docente})

# 3. EDITAR CÉDULA
@never_cache
@login_required
def editar_cedula(request, clave_docente, id_cedula):
    cedula = get_object_or_404(Cedulas, id_cedula=id_cedula)
    docente = get_object_or_404(Docente, claveDocente=clave_docente)
    
    if request.method == 'POST':
        form = CedulasForm(request.POST, instance=cedula)
        if form.is_valid():
            form.save()
            return redirect('lista_cedulas', clave_docente=clave_docente)
    else:
        form = CedulasForm(instance=cedula)
    
    return render(request, 'agregar_cedula.html', {'form': form, 'docente': docente, 'editando': True})

# 4. ELIMINAR CÉDULA
@never_cache
@login_required
def eliminar_cedula(request, clave_docente, id_cedula):
    cedula = get_object_or_404(Cedulas, id_cedula=id_cedula)
    if request.method == 'POST':
        cedula.delete()
    return redirect('lista_cedulas', clave_docente=clave_docente)