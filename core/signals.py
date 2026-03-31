#evento que Django ejecuta automáticamente cuando ocurre algo
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cliente, Cuenta
import random


def generar_numero_cuenta():
    while True:
        numero = str(random.randint(10000000, 99999999))

        if not Cuenta.objects.filter(numero_cuenta=numero).exists():
            return numero


@receiver(post_save, sender=Cliente)
def crear_cuenta_cliente(sender, instance, created, **kwargs):

    if created:

        numero = generar_numero_cuenta()

        Cuenta.objects.create(
            cliente=instance,
            numero_cuenta=numero,
            saldo=0
        )