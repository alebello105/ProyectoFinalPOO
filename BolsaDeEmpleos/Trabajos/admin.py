from django.contrib import admin
from .models import Trabajo, TipoTrabajo, Empleador, Aplicacion

@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'ubicacion', 'fecha_publicacion')
    search_fields = ('titulo', 'empresa__username', 'ubicacion')
    list_filter = ('fecha_publicacion', 'tipo_trabajo')

@admin.register(TipoTrabajo)
class TipoTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Empleador)
class EmpleadorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')

@admin.register(Aplicacion)
class AplicacionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'trabajo', 'estado', 'fecha_aplicacion')
    search_fields = ('usuario__username', 'trabajo__titulo', 'estado')
    list_filter = ('estado', 'fecha_aplicacion')
