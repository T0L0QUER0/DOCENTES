from django import forms
from .models import Docente # Ya NO importamos Division por ahora

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'
        
        labels = {
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
            'Puesto': 'Puesto',
            'idDivision_FK': 'División',
            'Perfil': 'Perfil',
            'FechaIngreso': 'Fecha de Ingreso',
            'correoInstitucional': 'Correo Institucional',
            'correoPersonal': 'Correo Personal',
            'Telefono': 'Teléfono',
        }