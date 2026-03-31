from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

telefono_validator = RegexValidator( #validamos que el numero telefonico sea correcto
    regex=r'^9\d{8}$', #^9 = comienzo | \d{8} = 8 digitos mas  | $ = fin 
    message="El teléfono debe tener 9 dígitos y comenzar con 9 (ej: 912345678)"
)

class Cliente(models.Model):
    
    #Representa a cada usuario y sus datos
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente")
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(
        max_length=9,
        validators=[telefono_validator]
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        permissions = [
            ("view_reportes", "Puede ver reportes de clientes"),
        ]


class Cuenta(models.Model):

    #Un cliente -> un usuario 

    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    numero_cuenta = models.CharField(max_length=12, unique=True)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cuenta {self.numero_cuenta} - {self.cliente}"
    
    
class Movimiento(models.Model):

    #Todos los movimientos registrados por cada CUENTA 

    TIPO_MOVIMIENTO = [

        ("deposito", "Depósito"),

        ("transferencia_enviada", "Transferencia enviada"),

        ("transferencia_recibida", "Transferencia recibida"),

    ]

    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=30, choices=TIPO_MOVIMIENTO)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=255, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - ${self.monto}"
    

class Contacto(models.Model):

    #Contacto guardado por cada CUENTA

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=12)
    alias = models.CharField(max_length=100)
    banco = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.alias} ({self.numero_cuenta})"
