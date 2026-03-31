#  Alke Wallet - Aplicación Web con Django

Aplicación web desarrollada con Django que simula el funcionamiento de una billetera digital, permitiendo a los usuarios gestionar su cuenta, realizar transferencias, depósitos y visualizar movimientos, utilizando una base de datos relacional y el ORM de Django.

---

## Tecnologías utilizadas

- Python 3
- Django
- SQLite / PostgreSQL
- HTML5
- CSS3
- JavaScript (jQuery)
- Bootstrap 4

---

##  Funcionalidades principales

###  Autenticación de usuarios
- Inicio y cierre de sesión
- Validación de credenciales
- Protección de vistas con `login_required`

---

### Gestión de cuenta
- Visualización de saldo
- Depósito de dinero
- Transferencias entre cuentas
- Validación de saldo y operaciones

---

### Movimientos
- Registro automático de transacciones
- Historial de movimientos por usuario
- Ordenamiento por fecha

---

###  Gestión de contactos (CRUD)
- Crear contactos
- Editar contactos
- Eliminar contactos
- Listar contactos asociados al usuario

---

###  Panel administrativo
- Gestión de usuarios
- Asociación de clientes con cuentas
- Visualización de datos

---

### Control de permisos
- Acceso restringido a reportes
- Uso de permisos personalizados (`view_reportes`)
- Separación entre usuarios normales y administradores

---

### Consultas avanzadas
- Cuentas con más movimientos
- Cuentas con mayor saldo
- Uso de ORM con `annotate()` y `Count()`

---

## Arquitectura del proyecto

El proyecto sigue el patrón **MTV (Model - Template - View)** de Django:

- **Model** → Define la estructura de la base de datos
- **View** → Contiene la lógica de negocio
- **Template** → Presentación de datos al usuario

---

## Modelo de datos

Relaciones principales:

- Usuario → Cliente (1 a 1)
- Cliente → Cuenta (1 a 1)
- Cuenta → Movimiento (1 a muchos)
- Cliente → Contacto (1 a muchos)

---
