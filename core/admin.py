from django.contrib import admin
from .models import Cliente, Cuenta, Movimiento, Contacto


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = ("nombre", "apellido", "correo", "telefono", "usuario")


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):

    list_display = ("numero_cuenta", "cliente", "saldo", "fecha_creacion")


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):

    list_display = ("cuenta", "tipo", "monto", "fecha")


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):

    list_display = ("alias", "nombre", "numero_cuenta", "banco", "cliente")