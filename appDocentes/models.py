from django.db import models

class Docente(models.Model): # Tabla Docentes

    # DATOS PERSONALES ========================================================
    Nombre = models.CharField(max_length=100)
    ApellidoP = models.CharField(max_length=100)
    ApellidoM = models.CharField(max_length=100)
    FechaNacimiento = models.DateField()
    CedulaProfesional = models.CharField(max_length=50, unique=True, blank=True, null=True)
    GradoAcademico = models.CharField(max_length=100, choices=[('Licenciatura', 'Licenciatura'), ('Maestría', 'Maestría'), ('Doctorado', 'Doctorado')])
    EstadoCivil = models.CharField(max_length=30, choices=[('Casado', 'Casado'), ('Soltero', 'Soltero'),('Divorciado', 'Divorciado'),('Viudo', 'Viudo')])
    Sexo = models.CharField(max_length=10, choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer')])
    Residencia = models.CharField(max_length=100)
    Ciudad = models.CharField(max_length=100)
    Colonia = models.CharField(max_length=100)
    Discapacidad = models.CharField(max_length=50,null=True, choices=[('Visual','Visual'),('Auditiva','Auditiva'),('Fisica','Fisica'),('Mental','Mental'),('Otra','Otra'),('Ninguna','Ninguna')])


    # DATOS LABORALES =========================================================
    claveDocente = models.CharField(max_length=50, primary_key=True)
    Puesto = models.CharField(max_length=50,choices=[('Docencia','Docencia'),('Administrativo','Administrativo'),('Intendencia','Intendencia')])
    division = models.ForeignKey('Division', on_delete=models.PROTECT, null=True)
    Perfil = models.CharField(max_length=50, choices=[('Tiempo Completo', 'Tiempo Completo'), ('Medio Tiempo', 'Medio Tiempo'), ('Por Asignatura', 'Por Asignatura')])
    FechaIngreso = models.DateField()
    OtroEmpleo = models.CharField(max_length=2, choices=[('Si', 'Si'), ('No', 'No')], default='No')
    categoria = models.CharField(max_length=10, null=True, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    base = models.CharField(max_length=20, null=True, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    status = models.CharField(max_length=20, null=True, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
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
    


class Proyectos(models.Model):
    ID_Compuesto = models.CharField(max_length=100, primary_key=True, editable=False) 
    IdProyecto_Base = models.CharField(max_length=50, verbose_name="ID Proyecto Base") 
    Nombre = models.CharField(max_length=256)
    Descripcion = models.TextField(
        verbose_name="Descripción del Proyecto", 
        blank=True, 
        null=True
    )
    claveDocente = models.ForeignKey(
        'Docente', 
        on_delete=models.CASCADE, 
        db_column='claveDocente',
        verbose_name="Docente Líder"
    )
    Colaboradores = models.ManyToManyField(
        'Docente', 
        related_name='proyectos_colaborados', 
        verbose_name="Colaboradores (Docentes)"
    )


    def save(self, *args, **kwargs):
        clave_docente_str = self.claveDocente.claveDocente 
        id_proyecto_base_str = self.IdProyecto_Base
        self.ID_Compuesto = f"{clave_docente_str}-{id_proyecto_base_str}"
        
        # Debe usar commit=False en la vista si queremos guardar Colaboradores.
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Proyecto: {self.ID_Compuesto} - {self.Nombre}"