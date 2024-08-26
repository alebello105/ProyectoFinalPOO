from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPOS_USUARIO = (
        ('empleado', 'Empleado'),
        ('empleador', 'Empleador'),
    )
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO)

    def es_empleado(self):
        return self.tipo_usuario == 'empleado'

    def es_empleador(self):
        return self.tipo_usuario == 'empleador'

class Empleador(models.Model):
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    industria = models.CharField(max_length=255)
    sitio_web = models.URLField(max_length=200)

    def __str__(self):
        return self.nombre

class TipoTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

class Trabajo(models.Model):
    titulo = models.CharField(max_length=255)
    empresa = models.ForeignKey(Empleador, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    requisitos = models.TextField()
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.SET_NULL, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} en {self.empresa.nombre}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle_trabajo', kwargs={'pk': self.pk})

    def es_reciente(self):
        from datetime import timedelta
        from django.utils import timezone
        return self.fecha_publicacion >= timezone.now().date() - timedelta(days=7)

    def aplicar(self, usuario, cv=None, carta_presentacion=None):
        Aplicacion.objects.create(
            usuario=usuario,
            trabajo=self,
            cv=cv,
            carta_presentacion=carta_presentacion,
            estado='Enviado'
    )

    def trabajos_similares(self):
        return Trabajo.objects.filter(
            empresa=self.empresa,
            tipo_trabajo=self.tipo_trabajo
        ).exclude(id=self.id)

    def obtener_reseñas(self):
        return self.reseña_set.all()

    def calificacion_promedio(self):
        reseñas = self.obtener_reseñas()
        if reseñas.exists():
            return reseñas.aggregate(models.Avg('calificacion'))['calificacion__avg']
        return None

    class Meta:
        ordering = ['-fecha_publicacion']
        
class Aplicacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    carta_presentacion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='Enviado')
    fecha_aplicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aplicación de {self.usuario.username} a {self.trabajo.titulo}"


class Reseña(models.Model):
    empresa = models.ForeignKey(Empleador, on_delete=models.CASCADE)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.SET_NULL, null=True, blank=True)
    calificacion = models.PositiveIntegerField()
    comentario = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.empresa.nombre}"

    class Meta:
        ordering = ['-fecha_creacion']
