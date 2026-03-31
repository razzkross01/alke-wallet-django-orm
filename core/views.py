from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied, ValidationError
from .models import Cliente, Cuenta, Movimiento, Contacto
from django.contrib import messages
from django.contrib.auth.models import User
from decimal import Decimal
from django.db import transaction
from django.db.models import Count
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

#Contenido

def index(request):
    contexto = {
        "titulo": "Alke Web Base",
    }
    return render(request, 'core/index.html', contexto)



def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("menu")

        else:
            return render(request, "core/login.html", {
                "error": "Credenciales incorrectas"
            })

    return render(request, "core/login.html")


def logout_view(request):

    logout(request)

    return redirect("login")

#Nuevo saldo real
@login_required
def menu_view(request):

    cliente = Cliente.objects.get(usuario=request.user)
    cuenta = Cuenta.objects.get(cliente=cliente)

    contexto = {
        "cliente": cliente,
        "cuenta": cuenta
    }

    return render(request, "core/menu.html", contexto)




#Nuevi deposito real
@login_required
def deposit(request):

    cliente = Cliente.objects.get(usuario=request.user)
    cuenta = Cuenta.objects.get(cliente=cliente)

    if request.method == "POST":

        monto = Decimal(request.POST.get("monto"))

        if monto <= 0:
            messages.error(request, "Monto inválido")
            return redirect("deposit")

        with transaction.atomic():

            cuenta.saldo += monto
            cuenta.save()

            Movimiento.objects.create(
                cuenta=cuenta,
                tipo="deposito",
                monto=monto,
                descripcion="Depósito de dinero"
            )

        messages.success(request, "Depósito realizado correctamente")

        return redirect("menu")

    contexto = {
        "cuenta": cuenta
    }

    return render(request, "core/deposit.html", contexto)



#Nuevo sendmoney real

@login_required
def sendmoney(request):

    cliente = Cliente.objects.get(usuario=request.user)
    cuenta_origen = Cuenta.objects.get(cliente=cliente)
    contactos = Contacto.objects.filter(cliente=cliente)

   

    if request.method == "POST":

        numero_cuenta_destino = request.POST.get("numero_cuenta")
        monto = Decimal(request.POST.get("monto"))

        if monto <= 0:
            messages.error(request, "Monto inválido")
            return redirect("sendmoney")

        try:
            cuenta_destino = Cuenta.objects.get(numero_cuenta=numero_cuenta_destino)
        except Cuenta.DoesNotExist:
            messages.error(request, "Cuenta destino no encontrada")
            return redirect("sendmoney")

        if cuenta_origen.saldo < monto:
            messages.error(request, "Saldo insuficiente")
            return redirect("sendmoney")
        
        if cuenta_destino == cuenta_origen:
            messages.error(request, "No puedes transferirte a tu propia cuenta")
            return redirect("sendmoney")

        with transaction.atomic():

            # restar saldo origen
            cuenta_origen.saldo -= monto
            cuenta_origen.save()

            # sumar saldo destino
            cuenta_destino.saldo += monto
            cuenta_destino.save()

            # movimiento enviado
            Movimiento.objects.create(
                cuenta=cuenta_origen,
                tipo="transferencia_enviada",
                monto=monto,
                descripcion=f"Transferencia a cuenta {cuenta_destino.numero_cuenta}"
            )

            # movimiento recibido
            Movimiento.objects.create(
                cuenta=cuenta_destino,
                tipo="transferencia_recibida",
                monto=monto,
                descripcion=f"Transferencia desde cuenta {cuenta_origen.numero_cuenta}"
            )

        messages.success(request, "Transferencia realizada correctamente")

        return redirect("menu")

    contexto = {
        "cuenta": cuenta_origen,
        "contactos": contactos
    }

    return render(request, "core/sendmoney.html", contexto)



#Nuevo Historial real
@login_required
def transactions(request):

    cliente = Cliente.objects.get(usuario=request.user)
    cuenta = Cuenta.objects.get(cliente=cliente)

    movimientos = Movimiento.objects.filter(
        cuenta=cuenta
    ).order_by("-fecha")

    contexto = {
        "movimientos": movimientos
    }

    return render(request, "core/transactions.html", contexto)


@login_required
def perfil_view(request):

    cliente = Cliente.objects.get(usuario=request.user)

    if request.method == "POST":

        cliente.correo = request.POST.get("correo")
        cliente.telefono = request.POST.get("telefono")
        
        try:
            cliente.full_clean()   # ejecuta validadores
            cliente.save()
            messages.success(request, "Perfil actualizado correctamente")

        except ValidationError as e:
            messages.error(request, e.message_dict["telefono"][0])
        
        return redirect("menu")

    contexto = {
        "cliente": cliente
    }

    return render(request, "core/perfil.html", contexto)


#Paginas privadas, solo administrador

class ReportesView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):

    template_name = "core/reportes.html"
    permission_required = "core.view_reportes"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clientes = Cliente.objects.select_related("usuario", "cuenta").all()
        context["clientes"] = clientes
        context["total_clientes"] = clientes.count()

        return context






@permission_required('core.view_reportes', raise_exception=True)
def crear_usuario(request):

    if request.method == "POST":

        username = request.POST.get("username").strip()
        password = request.POST.get("password").strip()
        nombre = request.POST.get("nombre").strip()
        apellido = request.POST.get("apellido").strip()
        correo = request.POST.get("correo").strip()
        telefono = request.POST.get("telefono").strip()

        # 1 Validar campos vacíos básicos
        if not username or not password or not nombre or not apellido:
            messages.error(request, "Todos los campos obligatorios deben estar completos")
            return redirect("crear_usuario")

        #  2 Validar usuario duplicado
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe")
            return redirect("crear_usuario")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        try:
            cliente = Cliente(
                usuario=user,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono
            )

            cliente.full_clean() 
            cliente.save()

        except Exception as e:

            user.delete()
            messages.error(request, f"Error al crear cliente: {e}")
            return redirect("crear_usuario")

        messages.success(request, "Usuario creado correctamente")
        return redirect("reportes")

    return render(request, "core/crear_usuario.html")




@permission_required('core.view_reportes', raise_exception=True)
def desactivar_usuario(request, user_id):

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Usuario no encontrado")
        return redirect("reportes")

    if user.is_superuser:
        messages.error(request, "No puedes modificar al superusuario")
        return redirect("reportes")

    # 🔥 TOGGLE
    user.is_active = not user.is_active
    user.save()

    if user.is_active:
        messages.success(request, f"Usuario {user.username} activado")
    else:
        messages.success(request, f"Usuario {user.username} desactivado")

    return redirect("reportes")


#Consultas personalizadas
@permission_required('core.view_reportes', raise_exception=True)

def consultas_view(request):

    cuentas_mas_movimientos = Cuenta.objects.annotate(total_movimientos=Count("movimiento")).order_by("-total_movimientos")[:10]
    saldos_totales = Cuenta.objects.filter(saldo__gt=1000)

    contexto = {
        "cuentas": cuentas_mas_movimientos,
        "saldos": saldos_totales
    }

    return render(request, "core/consultas.html", contexto)




#CRUD para contactos

class ContactoListView(LoginRequiredMixin, ListView):
    model = Contacto
    template_name='core/contacto_list.html'
    context_object_name = 'contactos'

    def get_queryset(self):
        return Contacto.objects.filter(
            cliente=self.request.user.cliente
        )


class ContactoCreateView(LoginRequiredMixin,CreateView):
    model = Contacto
    fields = ['nombre', 'numero_cuenta']
    template_name = 'core/contacto_form.html'
    success_url = reverse_lazy('sendmoney')

    def form_valid(self, form):
        form.instance.cliente = self.request.user.cliente
        return super().form_valid(form)

class ContactoUpdateView(LoginRequiredMixin,UpdateView):
    model = Contacto
    fields = ['nombre', 'numero_cuenta']
    template_name = 'core/contacto_form.html'
    success_url = reverse_lazy('sendmoney')

    def get_queryset(self):
        return Contacto.objects.filter(
            cliente=self.request.user.cliente
        )

class ContactoDeleteView(LoginRequiredMixin,DeleteView):
    model = Contacto
    template_name = "core/contacto_confirm_delete.html"
    success_url = reverse_lazy("sendmoney")

    def get_queryset(self):
        return Contacto.objects.filter(
            cliente=self.request.user.cliente
        )









#Control de Errores (pruebas)
def test403(request): #sin permmisos suficientes
    raise PermissionDenied

def test500(request): #error de sistema 500
    x = 1 / 0