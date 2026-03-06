from django import forms
from .models import Docente, Division, Proyectos, Cedulas

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        exclude = ['FechaInactividad', 'TipoInactividad']
        
        labels = {
            # Personales
            'Nombre': 'Nombre',
            'ApellidoP': 'Apellido Paterno',
            'ApellidoM': 'Apellido Materno',
            'FechaNacimiento': 'Fecha de Nacimiento',
            'CedulaProfesional': 'Cédula Profesional',
            'GradoAcademico': 'Grado Académico',
            'EstadoCivil': 'Estado Civil',
            'Sexo': 'Sexo',
            'Residencia': 'Residencia',
            'Ciudad': 'Ciudad',
            'Colonia': 'Colonia',
            'Discapacidad' : 'Discapacidad',
            # Laborales
            'claveDocente': 'Matrícula',
            'Puesto': 'Puesto',
            'division': 'División',
            'Perfil': 'Perfil',
            'FechaIngreso': 'Fecha de Ingreso',
            'OtroEmpleo': 'Otro Empleo',
            'categoria': 'Categoría',
            'base': 'Base',
            'status': 'Status',
            'tutorado': 'Tutorado',
            'programaE': 'Programa Educativo',
            'areaC': 'Área de Conocimiento',
            # Contacto
            'correoInstitucional': 'Correo Institucional',
            'correoPersonal': 'Correo Personal',
            'Telefono': 'Teléfono',
            'cuentaTeams': 'Cuenta Teams'
        }

        widgets = {
            'FechaNacimiento': forms.DateInput(attrs={'type': 'date'}),
            'FechaIngreso': forms.DateInput(attrs={'type': 'date'}),
            'FechaInactividad': forms.DateInput(attrs={'type': 'date'}),
        }


class DocenteEdit(forms.ModelForm): # Cambiamos la herencia para incluir TODO
    claveDocente = forms.CharField(label='Matrícula', disabled=True) 

    class Meta:
        model = Docente
        fields = '__all__' # Aquí sí incluimos los nuevos campos


        labels = {
            # Personales
            'Nombre': 'Nombre',
            'ApellidoP': 'Apellido Paterno',
            'ApellidoM': 'Apellido Materno',
            'FechaNacimiento': 'Fecha de Nacimiento',
            'CedulaProfesional': 'Cédula Profesional',
            'GradoAcademico': 'Grado Académico',
            'EstadoCivil': 'Estado Civil',
            'Sexo': 'Sexo',
            'Residencia': 'Residencia',
            'Ciudad': 'Ciudad',
            'Colonia': 'Colonia',
            'Discapacidad' : 'Discapacidad',
            # Laborales
            'claveDocente': 'Matrícula',
            'Puesto': 'Puesto',
            'division': 'División',
            'Perfil': 'Perfil',
            'FechaIngreso': 'Fecha de Ingreso',
            'OtroEmpleo': 'Otro Empleo',
            'categoria': 'Categoría',
            'base': 'Base',
            'status': 'Status',
            'tutorado': 'Tutorado',
            'programaE': 'Programa Educativo',
            'areaC': 'Área de Conocimiento',
            # Contacto
            'correoInstitucional': 'Correo Institucional',
            'correoPersonal': 'Correo Personal',
            'Telefono': 'Teléfono',
            'cuentaTeams': 'Cuenta Teams'
        }

        
        widgets = {
            'FechaNacimiento': forms.DateInput(attrs={'type': 'date'}),
            'FechaIngreso': forms.DateInput(attrs={'type': 'date'}),
            'FechaInactividad': forms.DateInput(attrs={'type': 'date'}),
        }


class ProyectoInvestigacionForm(forms.ModelForm):
    class Meta:
        model = Proyectos
        fields = ['claveDocente', 'Nombre', 'Descripcion', 'Colaboradores'] 
        
        widgets = {
            'Descripcion': forms.Textarea(attrs={'rows': 4}), 
        }






class CedulasForm(forms.ModelForm):
    
    class Meta:
        model = Cedulas
        # Incluimos todos los campos del modelo, excepto el ID (primary_key) si quieres que sea inmutable
        # Si quieres que el usuario pueda escribir el ID, déjalo aquí. 
        # Si usas ModelForm para editar, el ID se pasa en la URL, no en el formulario.
        fields = [
            'id_cedula',
            'NombreTitulo',
            'Institucion',
            'FechaObtencion',
        ]
        
        widgets = {
            'id_cedula': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: 1234567'}),
            'NombreTitulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Maestría en Ciencias'}),
            'Institucion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: UJAT'}),
            # Usar un input de tipo date para facilitar la selección de fecha
            'FechaObtencion': forms.DateInput(attrs={'class': 'form-input date-input', 'type': 'date'}),
        }
        
        labels = {
            'id_cedula': 'Número de Cédula Profesional',
            'NombreTitulo': 'Título Obtenido',
            'Institucion': 'Institución Expedidora',
            'FechaObtencion': 'Fecha de Obtención',
        }
