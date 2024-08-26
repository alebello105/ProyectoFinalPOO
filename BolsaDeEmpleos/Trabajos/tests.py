from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Trabajo, TipoTrabajo, Aplicacion

class TipoTrabajoTests(TestCase):
    def setUp(self):
        self.tipo_trabajo = TipoTrabajo.objects.create(nombre='Desarrollador')

    def test_tipo_trabajo_str(self):
        self.assertEqual(str(self.tipo_trabajo), 'Desarrollador')

class TrabajoTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='usuario', password='contraseña')
        self.tipo_trabajo = TipoTrabajo.objects.create(nombre='Desarrollador')
        self.trabajo = Trabajo.objects.create(
            titulo='Desarrollador Backend',
            empresa=self.user,
            ubicacion='Ciudad',
            descripcion='Trabajo de desarrollador backend.',
            requisitos='Experiencia en Python.',
            tipo_trabajo=self.tipo_trabajo
        )

    def test_trabajo_str(self):
        self.assertEqual(str(self.trabajo), 'Desarrollador Backend en usuario')

    def test_aplicacion_creation(self):
        aplicacion = Aplicacion.objects.create(
            usuario=self.user,
            trabajo=self.trabajo,
            cv=None,
            carta_presentacion='Carta de presentación',
            estado='Enviado'
        )
        self.assertEqual(aplicacion.usuario, self.user)
        self.assertEqual(aplicacion.trabajo, self.trabajo)
        self.assertEqual(aplicacion.estado, 'Enviado')
