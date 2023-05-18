from django.shortcuts import render
from .models import Titulares, Cuentas
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction


# Create your views here.

# view to render the login page
def login(request):
    if request.method == 'GET':
        return render(request, 'Authentication/login.html', {
            'title': 'Iniciar Sesión',
        })
    else:
        tipo_documento = request.POST.get('tipo_documento')
        documento = request.POST.get('documento')
        tipo_cuenta = request.POST.get('tipo_cuenta')
        password = request.POST.get('password')
        try:
            cuenta = Cuentas.objects.get(id_titular=Titulares.objects.get(
                        tipo_documento=tipo_documento, documento_identidad=documento),
                        tipo_cuenta=tipo_cuenta)
            if cuenta.password != password:
                messages.error(request, 'Contraseña incorrecta')
                return render(request, 'Authentication/login.html', {
                    'title': 'Iniciar Sesión',
                })
            return HttpResponse('Bienvenido')
        except (Titulares.DoesNotExist, Cuentas.DoesNotExist, ValueError):
            messages.info(request, 'Cuenta no existente')
            return render(request, 'Authentication/login.html', {
                'title': 'Iniciar Sesión',
            })


@transaction.atomic
def change_password(request):
    if request.method == "GET":
        return render(request, 'Authentication/change_password.html', {
            'title': 'Cambiar Contraseña',
        })
    else:
        tipo_documento = request.POST.get('tipo_documento')
        documento = request.POST.get('documento')
        tipo_cuenta = request.POST.get('tipo_cuenta')
        password = request.POST.get('password')
        confirma_password = request.POST.get('password_confirmation')
        try:
            cuenta = Cuentas.objects.get(id_titular=Titulares.objects.get(
                        tipo_documento=tipo_documento, documento_identidad=documento),
                        tipo_cuenta=tipo_cuenta)
            if password != confirma_password:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'Authentication/change_password.html', {
                    'title': 'Cambiar Contraseña',
                })
            cuenta.password = password
            cuenta.save()
            messages.success(request, 'Contraseña cambiada con éxito')
            return render(request, 'Authentication/login.html', {
                'title': 'Iniciar Sesión',
            })
        except (Titulares.DoesNotExist, Cuentas.DoesNotExist, ValueError):
            messages.info(request, 'Cuenta no existente')
            return render(request, 'Authentication/login.html', {
                'title': 'Iniciar Sesión',
            })

