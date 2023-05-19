from django.shortcuts import render, redirect
from .models import Titulares, Cuentas
from django.http import HttpResponse
from django.contrib import messages
from django.db import transaction, IntegrityError


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
                return redirect('login')
            return HttpResponse('Bienvenido')
        except (Titulares.DoesNotExist, Cuentas.DoesNotExist, ValueError):
            messages.info(request, 'Cuenta no existente')
            return redirect('login')


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
                return redirect('change_password')
            cuenta.password = password
            cuenta.save()
            messages.success(request, 'Contraseña modificada con éxito')
            return redirect('login')
        except (Titulares.DoesNotExist, Cuentas.DoesNotExist, ValueError):
            messages.info(request, 'Cuenta no existente')
            return redirect('login')


@transaction.atomic
def create_user(request):
    if request.method == 'GET':
        return render(request, 'Authentication/signup.html', {
            'title': 'Crear Nuevo Usuario',
        })
    else:
        tipo_documento = request.POST.get('tipo_documento')
        documento = request.POST.get('documento')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        tipo_cuenta = request.POST.get('tipo_cuenta')
        saldo = float(request.POST.get('saldo'))
        password = request.POST.get('password')
        confirma_password = request.POST.get('password_confirmation')
        try:
            titular = Titulares.objects.get(tipo_documento=tipo_documento,
                                            documento_identidad=documento)
            if nombres != titular.nombres or apellidos != titular.apellidos:
                messages.error(request, 'Nombres y Apellidos no coinciden con la identificación dada')
                return redirect('signup')
        except Titulares.DoesNotExist:
            titular = Titulares.objects.create(tipo_documento=tipo_documento,
                                               documento_identidad=documento,
                                               nombres=nombres,
                                               apellidos=apellidos)
            titular.save()
        if password != confirma_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('signup')
        try:
            Cuentas.objects.create(id_titular=titular,
                                   tipo_cuenta=tipo_cuenta,
                                   saldo=saldo,
                                   password=password)
            messages.success(request, 'Usuario creado con éxito')
            return redirect('login')
        except IntegrityError:
            messages.error(request, 'Cuenta ya existente')
            return redirect('signup')
