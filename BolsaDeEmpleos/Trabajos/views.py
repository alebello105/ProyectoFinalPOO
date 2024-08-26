from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import FormularioRegistroEmpleado, FormularioRegistroEmpleador
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Trabajo, Aplicacion
from .forms import AplicacionForm

def registrar_empleado(request):
    if request.method == 'POST':
        form = FormularioRegistroEmpleado(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo_usuario = 'empleado'
            usuario.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = FormularioRegistroEmpleado()
    return render(request, 'trabajos/registrar_empleado.html', {'form': form})

def registrar_empleador(request):
    if request.method == 'POST':
        form = FormularioRegistroEmpleador(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.tipo_usuario = 'empleador'
            usuario.save()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = FormularioRegistroEmpleador()
    return render(request, 'trabajos/registrar_empleador.html', {'form': form})
@login_required
def detalle_trabajo(request, trabajo_id):
    trabajo = get_object_or_404(Trabajo, pk=trabajo_id)
    
    if request.method == 'POST':
        form = AplicacionForm(request.POST, request.FILES)
        if form.is_valid():
            aplicacion = form.save(commit=False)
            aplicacion.usuario = request.user
            aplicacion.trabajo = trabajo
            aplicacion.save()
            return HttpResponseRedirect(reverse('detalle_trabajo', args=[trabajo_id]))
    else:
        form = AplicacionForm()

    return render(request, 'trabajos/detalle_trabajo.html', {
        'trabajo': trabajo,
        'form': form
    })