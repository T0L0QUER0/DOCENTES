from django.db import models


class Profesor(models.Model):
    clave_docente = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1)  # H o M
    puesto = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    correo_institucional = models.EmailField(max_length=254)
    correo_personal = models.EmailField(max_length=254)
    correo_teams = models.EmailField(max_length=254)
    base = models.CharField(max_length=10)
    celular = models.CharField(max_length=15)
    status_docencia = models.CharField(max_length=50)
    tipo_inactividad = models.CharField(max_length=50)
    discapacidad = models.BooleanField(default=False)
    tutorado = models.BooleanField(default=False)
    fecha_ingreso = models.DateField()
    fecha_nacimiento = models.DateField()
    grado_actual = models.CharField(max_length=50)
    otro_empleo = models.BooleanField(default=False)
    residencia = models.CharField(max_length=100)
    id_division = models.ForeignKey('Division', on_delete=models.CASCADE)
    id_area_conocimiento = models.ForeignKey('AreaConocimiento', on_delete=models.CASCADE)
    id_programa_educativo = models.ForeignKey('ProgramaEducativo', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"

class Division(models.Model):
    clave_division = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    num_ext = models.CharField(max_length=10)
    
    def __str__(self):
        return self.nombre

class AreaConocimiento(models.Model):
    id_area = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class ProgramaEducativo(models.Model):
    id_pe = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

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
    fecha_ingreso = models.DateField()
    fecha_fin = models.DateField()
    clave_docente = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"SEI de {self.clave_docente}"

class Promep(models.Model):
    id_promep = models.IntegerField(primary_key=True)
    superfave = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    clave_docente = models.ForeignKey('Profesor', on_delete=models.CASCADE)

    def __str__(self):
        return f"Promep de {self.clave_docente}"

class ProyectoInvestigacion(models.Model):
    id_proyecto = models.CharField(max_length=20, primary_key=True)
    superfave = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    clave_docente = models.ForeignKey('Profesor', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class CedulaLicenciatura(models.Model):
    num_ced_lic = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    clave_docente = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cédula Lic. de {self.clave_docente}"

class CedulaMaestria(models.Model):
    num_ced_m = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    clave_docente = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cédula Maestría de {self.clave_docente}"

class CedulaDoctorado(models.Model):
    num_ced_dr = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    fecha_obtencion = models.DateField()
    clave_docente = models.ForeignKey('Profesor', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Cédula Doctorado de {self.clave_docente}"