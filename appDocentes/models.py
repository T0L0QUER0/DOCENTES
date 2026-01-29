from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

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
        
class DivisionManager(BaseUserManager):
    def create_user(self, correo_administrador, password=None, **extra_fields):
        if not correo_administrador:
            raise ValueError('El correo electrónico debe ser obligatorio')        
        user = self.model(correo_administrador=correo_administrador, **extra_fields)
        user.set_password(password)        
        user.save(using=self._db)
        return user
    

    
class Division(AbstractBaseUser): 
    claveDivision=models.CharField(max_length=100, primary_key=True, db_column='claveDivision')
    Nombre = models.CharField(max_length=100,null=True)
    Calle = models.CharField(max_length=100,null=True)
    Col = models.CharField(max_length=100,null=True)
    Ciudad = models.CharField(max_length=100,null=True)
    NumExt = models.CharField(max_length=10,null=True)
    CodigoP = models.CharField(max_length=10,null=True)
    correo_administrador = models.EmailField(max_length=100, unique=True)


    @property
    def is_authenticated(self):
        return True 

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def get_email_field_name(cls):
        return 'correo_administrador'

    def has_perm(self, perm, obj=None):
        return self.is_admin 

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return str(self.claveDivision)
    

    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo_administrador'
    @property
    def email (self):
        return self.correo_administrador
    @property
    def pk(self):
        return self.claveDivision
    password = models.CharField(max_length=128, db_column='contraseña_administrador')

    objects = DivisionManager()

    def get_session_auth_hash(self):
        return self.password
    
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

