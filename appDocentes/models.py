from django.db import models

class Docente(models.Model):
    # DATOS PERSONALES
    Nombre = models.CharField(max_length=100)
    ApellidoP = models.CharField(max_length=100)
    ApellidoM = models.CharField(max_length=100)
    FechaNacimiento = models.DateField()
    CedulaProfesional = models.CharField(max_length=50, unique=True, blank=True, null=True)
    GradoAcademico = models.CharField(max_length=50) #'Maestría', 'Doctorado'
    EstadoCivil = models.CharField(max_length=30, choices=[('Casado', 'Casado'), ('Soltero', 'Soltero')])
    Sexo = models.CharField(max_length=10, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')])
    Residencia = models.CharField(max_length=100)
    Ciudad = models.CharField(max_length=100)
    Colonia = models.CharField(max_length=100)
    #Discapacidad = models.CharField(max_length=1, choices=[('Si', 'Si'), ('No', 'No')])
    
    # DATOS LABORALES
    claveDocente = models.CharField(max_length=50, primary_key=True)
    Puesto = models.CharField(max_length=50)
    idDivision_FK = models.CharField(max_length=10, choices=[('DACyTI', 'DACyTI'), ('DAIA', 'DAIA'), ('DACB', 'DACB')])
    Perfil = models.CharField(max_length=50, choices=[('Tiempo Completo', 'Tiempo Completo'), ('Medio Tiempo', 'Medio Tiempo'), ('Por Asignatura', 'Por Asignatura')]) # Ejemplo: 'Tiempo Completo', 'Medio Tiempo'
    FechaIngreso = models.DateField()

    # DATOS DE CONTACTO
    correoInstitucional = models.EmailField(max_length=100, unique=True)
    correoPersonal = models.EmailField(max_length=100, blank=True, null=True)
    Telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.claveDocente} - {self.Nombre} {self.ApellidoP}"