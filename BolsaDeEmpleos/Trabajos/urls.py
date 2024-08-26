from django.urls import path
from . import views

urlpatterns = [
    path('registrar/empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('registrar/empleador/', views.registrar_empleador, name='registrar_empleador'),
    path('trabajo/<int:pk>/', views.detalle_trabajo, name='detalle_trabajo'),
]
