from django import forms
from .models import Docente, Division

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'
        
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


class DocenteEdit(forms.ModelForm):
    # Opcional pero recomendado: Desactivar la edición de la clave primaria (Matrícula)
    # Esto evita que el usuario cambie la llave, lo cual puede causar errores de base de datos.
    claveDocente = forms.CharField(label='Matrícula', max_length=50, disabled=True) 

    class Meta:
        model = Docente
        fields = '__all__'
        
        # Copia de los labels para mantener consistencia
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
        
        # Mantenemos los widgets para los campos de fecha
        widgets = {
            'FechaNacimiento': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
            'FechaIngreso': forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'}),
        }