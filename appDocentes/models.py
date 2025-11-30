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
    division = models.ForeignKey('Division', on_delete=models.PROTECT, null=True, blank=True)
    Perfil = models.CharField(max_length=50, choices=[('Tiempo Completo', 'Tiempo Completo'), ('Medio Tiempo', 'Medio Tiempo'), ('Por Asignatura', 'Por Asignatura')]) # Ejemplo: 'Tiempo Completo', 'Medio Tiempo'
    FechaIngreso = models.DateField()
    OtroEmpleo = models.CharField(max_length=2, choices=[('Si', 'Si'), ('No', 'No')], default='No')
    categoria = models.CharField(max_length=10, null=True)
    base = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    tutorado = models.CharField(max_length=2, choices=[('Si', 'Si'), ('No', 'No')], default='No', null=True)
    programaE = models.ForeignKey('ProgramaEducativo', on_delete=models.PROTECT, null=True, blank=True)
    areaC = models.ForeignKey('AreaConocimiento', on_delete=models.PROTECT, null=True, blank=True)
    fechaInactividad = models.DateField(null=True,blank=True)
    tipoInactividad = models.CharField(null=True,blank=True)


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

class Asignatura(models.Model):
    clave_asignatura = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    id_area = models.ForeignKey('AreaConocimiento', on_delete=models.CASCADE)
    id_division = models.ForeignKey('Division', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre

class SEI(models.Model):
    id_sei = models.IntegerField(primary_key=True)
    superfave = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)
    clave_docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
    def __str__(self):
        return f"SEI de {self.clave_docente}"

class Promep(models.Model):
    id_promep = models.IntegerField(primary_key=True)
    superfave = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    clave_docente = models.ForeignKey('Docente', on_delete=models.CASCADE)

    def __str__(self):
        return f"Promep de {self.clave_docente}"

class ProyectoInvestigacion(models.Model):
    id_proyecto = models.CharField(max_length=20, primary_key=True)
    superllave = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    colaboradores=models.CharField(max_length=200,null=True,blank=True)
    descripcion=models.CharField(max_length=500,null=True,blank=True)
    clave_docente = models.ForeignKey('Docente', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class CedulaLicenciatura(models.Model):
    num_ced_lic = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    clave_docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cédula Lic. de {self.clave_docente}"

class CedulaMaestria(models.Model):
    num_ced_m = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    clave_docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cédula Maestría de {self.clave_docente}"

class CedulaDoctorado(models.Model):
    num_ced_dr = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    clave_docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cédula Doctorado de {self.clave_docente}"