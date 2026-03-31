from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('menu/', views.menu_view, name='menu'),
    path('logout/', views.logout_view, name='logout'),
    path('deposit/', views.deposit, name='deposit'),
    path('sendmoney/', views.sendmoney, name='sendmoney'),
    path('transactions/', views.transactions, name='transactions'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('desactivar-usuario/<int:user_id>/',views.desactivar_usuario,name='desactivar_usuario'),
    path('consultas/', views.consultas_view, name='consultas'),

    #CRUDContactos

    path('contactos/', ContactoListView.as_view(), name='contacto_list'),
    path('contactos/crear/', ContactoCreateView.as_view(), name='contacto_create'),
    path('contactos/editar/<int:pk>/', ContactoUpdateView.as_view(), name='contacto_update'),
    path('contactos/eliminar/<int:pk>/', ContactoDeleteView.as_view(), name='contacto_delete'),

    #pruebas
    path('test403/', views.test403),
    path("test500/", views.test500)
]