from django.shortcuts import render, redirect
from .models import Titulares, Cuentas, Movimientos, TipoTransaccion
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
            return redirect('account', account=cuenta.numero_cuenta)
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


@transaction.atomic
def account(request, account):
    cuenta = Cuentas.objects.select_for_update().get(numero_cuenta=account)
    if request.method == 'GET':
        return render(request, 'Account/home.html', {
            'title': f'{cuenta.id_titular.nombres}',
            'cuenta': cuenta,
        })
    else:
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        saldo = float(request.POST.get('saldo'))
        tipo_cuenta = request.POST.get('tipo_cuenta')

        cuenta.id_titular.nombres = nombres
        cuenta.id_titular.apellidos = apellidos
        cuenta.id_titular.save()

        try:
            cuenta.saldo = saldo
            cuenta.tipo_cuenta = tipo_cuenta
            cuenta.save()
        except (ValueError, IntegrityError):
            messages.error(request, 'Ya tienes otra cuenta con ese tipo de cuenta')
            return redirect('account', account=account)
        messages.success(request, 'Cuenta modificada con éxito')
        return redirect('account', account=account)


def transfers(request, account):
    cuenta = Cuentas.objects.get(numero_cuenta=account)
    transacciones = Movimientos.objects.filter(numero_cuenta_entrada=cuenta) | Movimientos.objects.filter(
        numero_cuenta_salida=cuenta)
    return render(request, 'Account/transfers.html', {
        'title': f'{cuenta.id_titular.nombres}',
        'cuenta': cuenta,
        'transactions': transacciones,
    })


def transfer(request, account):
    cuenta = Cuentas.objects.get(numero_cuenta=account)
    tipo_transacciones = TipoTransaccion.objects.all()
    if request.method == 'GET':
        return render(request, 'Account/transaction.html', {
            'title': f'{cuenta.id_titular.nombres}',
            'cuenta': cuenta,
            'tipo_transacciones': tipo_transacciones,
        })
    else:
        numero_cuenta_destino = request.POST.get('numero_cuenta')
        monto = float(request.POST.get('monto'))
        id_tipo_transaccion = int(request.POST.get('tipo_transaccion'))
        try:
            cuenta_destino = Cuentas.objects.get(numero_cuenta=numero_cuenta_destino)
            if cuenta_destino == cuenta:
                messages.error(request, 'No puedes transferir a la misma cuenta')
                return redirect('transfer', account=account)
            if cuenta.saldo < monto:
                messages.error(request, 'Saldo insuficiente')
                return redirect('transfer', account=account)
            Movimientos.objects.create(numero_cuenta_entrada_id=cuenta_destino.numero_cuenta,
                                       numero_cuenta_salida_id=cuenta.numero_cuenta,
                                       valor=monto,
                                       id_tipo_transaccion_id=id_tipo_transaccion)
            messages.success(request, 'Transferencia realizada con éxito')
            return redirect('account', account=account)
        except Cuentas.DoesNotExist:
            messages.error(request, 'La cuenta destino no existe')
            return redirect('transfer', account=account)


@transaction.atomic
def cancel(request, account):
    cuenta = Cuentas.objects.select_for_update().get(numero_cuenta=account)
    Movimientos.objects.create(numero_cuenta_salida_id=cuenta.numero_cuenta,
                               valor=cuenta.saldo,
                               id_tipo_transaccion_id=1)
    messages.success(request, 'Cuenta cancelada con éxito')
    return redirect('account', account=account)
