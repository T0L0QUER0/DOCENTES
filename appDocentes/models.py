from django.db import models

class Docente(models.Model): # Tabla Docentes

    # DATOS PERSONALES ========================================================
    Nombre = models.CharField(max_length=100)
    ApellidoP = models.CharField(max_length=100)
    ApellidoM = models.CharField(max_length=100)
    FechaNacimiento = models.DateField()
    CedulaProfesional = models.CharField(max_length=50, unique=True, blank=True, null=True)
    GradoAcademico = models.CharField(max_length=50)
    EstadoCivil = models.CharField(max_length=30, choices=[('Casado', 'Casado'), ('Soltero', 'Soltero')])
    Sexo = models.CharField(max_length=10, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')])
    Residencia = models.CharField(max_length=100)
    Ciudad = models.CharField(max_length=100)
    Colonia = models.CharField(max_length=100)
    Discapacidad = models.CharField(max_length=50,null=True)


    # DATOS LABORALES =========================================================
    claveDocente = models.CharField(max_length=50, primary_key=True)
    Puesto = models.CharField(max_length=50)
    division = models.ForeignKey('Division', on_delete=models.PROTECT, null=True)
    Perfil = models.CharField(max_length=50, choices=[('Tiempo Completo', 'Tiempo Completo'), ('Medio Tiempo', 'Medio Tiempo'), ('Por Asignatura', 'Por Asignatura')]) # Ejemplo: 'Tiempo Completo', 'Medio Tiempo'
    FechaIngreso = models.DateField()
    OtroEmpleo = models.CharField(max_length=2, choices=[('Si', 'Si'), ('No', 'No')], default='No')
    categoria = models.CharField(max_length=10, null=True)
    base = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    tutorado = models.CharField(max_length=2, choices=[('Si', 'Si'), ('No', 'No')], default='No', null=True)
    programaE = models.ForeignKey('ProgramaEducativo', on_delete=models.PROTECT, null=True)
    areaC = models.ForeignKey('AreaConocimiento', on_delete=models.PROTECT, null=True)


    # DATOS DE CONTACTO =======================================================
    correoInstitucional = models.EmailField(max_length=100, unique=True)
    correoPersonal = models.EmailField(max_length=100, blank=True, null=True)
    Telefono = models.CharField(max_length=20, blank=True, null=True)
    cuentaTeams = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.claveDocente} - {self.Nombre} {self.ApellidoP}"
    
class Division(models.Model): #Tabla Division
    claveDivision = models.CharField(max_length=10, primary_key=True)
    Nombre = models.CharField(max_length=100,null=True)
    Calle = models.CharField(max_length=100,null=True)
    Col = models.CharField(max_length=100,null=True)
    Ciudad = models.CharField(max_length=100,null=True)
    NumExt = models.CharField(max_length=10,null=True)
    CodigoP = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.claveDivision
    
class ProgramaEducativo(models.Model):
    idPe = models.CharField(max_length=10, primary_key=True)
    Nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.idPe
    
class AreaConocimiento(models.Model):
    IdAreaC = models.CharField(max_length=10, primary_key=True)
    Nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Nombre