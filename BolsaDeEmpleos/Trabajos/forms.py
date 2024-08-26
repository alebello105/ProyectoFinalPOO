from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class FormularioRegistroUsuario(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'tipo_usuario']

class FormularioRegistroEmpleado(FormularioRegistroUsuario):
    class Meta(FormularioRegistroUsuario.Meta):
        fields = ['username', 'email', 'password1', 'password2']

class FormularioRegistroEmpleador(FormularioRegistroUsuario):
    class Meta(FormularioRegistroUsuario.Meta):
        fields = ['username', 'email', 'password1', 'password2', 'tipo_usuario']
