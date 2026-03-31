// --- Variable Global ---
let contacto_actual = null;

//Funciones generales

// Formatea números 800000 -> 800.000
function formatear_moneda(monto) {
    return monto.toLocaleString("es-CL");
}

//Funcion para redigir a paginas 
function redirigir(pagina_destino, tiempo = 2500) { 
    setTimeout(() => {
        window.location.href = pagina_destino;
    }, tiempo);
}


//funcion para obtener saldo base| si no existe crea uno
function saldo_base(){
     let saldo = localStorage.getItem("saldo");
        if (saldo === null) {
            localStorage.setItem("saldo", "1000000");
            saldo = "1000000"; 
        }

        return parseInt(saldo);  
}


//Funciones de Login 

//Funcion para verificar el inicio de sesion y mostrar alertas de mensajes
function verificador() {

    const correo = $("#email").val().trim();
    const contraseña = $("#password").val().trim();

    const $mensaje = $("#mensajeVerificador");
    $mensaje
        .removeClass("alert-success alert-danger alert-warning")
        .addClass("d-none");

    if (correo === "" || contraseña === "") {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-warning")
            .text("Por favor escriba sus credenciales");
        return false;
    }

    if (!correo.includes("@") || !correo.includes(".")) {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-danger")
            .text("Su correo está incorrecto");
        return false;
    }

    if (correo === "correo@prueba.com" && contraseña === "123456") {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-success")
            .text("Credenciales correctas");

        redirigir("/menu/", 1500);
        return false;
    }

    $mensaje
        .removeClass("d-none")
        .addClass("alert-danger")
        .text("Credenciales incorrectas");

    return false;
}


//Funciones de saldo / deposito

//funcion para mostrar saldo en pantalla en Menu 
function mostrar_saldo() {
    const $saldo = $("#saldo");

    if ($saldo.length) {
        $saldo.text(formatear_moneda(saldo_base()));
    }
}

//Funcion para depositar
function depositar() {

    const saldo_actual = saldo_base();
    const monto = Number($("#monto").val());
    const nuevo_saldo = saldo_actual + monto;

    const $mensaje = $("#mensajeDeposito");
    $mensaje
        .removeClass("alert-success alert-danger alert-warning")
        .addClass("d-none");

    if (isNaN(monto) || monto <= 0) {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-warning")
            .text("Por favor ingrese un monto válido");
        return false;
    }

    let transacciones = JSON.parse(localStorage.getItem("transacciones")) || [];

    transacciones.push({
        tipo: "deposito",
        monto: monto,
        fecha: new Date().toLocaleString()
    });

    localStorage.setItem("transacciones", JSON.stringify(transacciones));
    localStorage.setItem("saldo", nuevo_saldo.toString());

    $mensaje
        .removeClass("d-none")
        .addClass("alert-success")
        .text(
            "Depósito realizado correctamente. Nuevo saldo: $" +
            formatear_moneda(nuevo_saldo)
        );

    redirigir("/menu/", 3000);

    return false;
}


//Funciones de contactos

//Mostrar/Ocultar formularios
function ocultar_formulario() {
    $("#formulario_agregar").slideToggle(200);
    return false;
}

//Agregar contacto
function agregar_contacto() {

    const nombre = $("#nombre_completo").val().trim();
    const cuenta_bancaria = $("#cuenta").val().trim();
    const alias = $("#alias_nombre").val().trim();
    const banco = $("#nombre_banco").val().trim();

    let contactos = JSON.parse(localStorage.getItem("contactos")) || [];

    const nuevo_contacto = {
        nombre: nombre,
        alias: alias,
        cuenta: cuenta_bancaria,
        banco: banco
    };

    const existe = contactos.some(c =>
        c.nombre === nombre ||
        c.alias === alias ||
        c.cuenta === cuenta_bancaria
    );

    const $mensaje = $("#verifacador_agregar_contacto");

    if (existe) {
        $mensaje
            .removeClass("d-none alert-success")
            .addClass("alert-danger")
            .text("El contacto ya existe");
        return false;
    }

    contactos.push(nuevo_contacto);
    localStorage.setItem("contactos", JSON.stringify(contactos));

    $mensaje
        .removeClass("d-none alert-danger")
        .addClass("alert-success")
        .text("Se agregó el contacto exitosamente");

    $("#form-agregar-contacto")[0].reset();

    setTimeout(() => {
        $mensaje.addClass("d-none");
    }, 3000);

    return false;
}

//Buscar contactos
function buscar_contactos() {

    const contactos = JSON.parse(localStorage.getItem("contactos")) || [];
    const texto_buscar = $("#buscador").val().trim().toLowerCase();

    const contacto_encontrado = contactos.find(contacto =>
        contacto.nombre.toLowerCase() === texto_buscar ||
        contacto.alias.toLowerCase() === texto_buscar
    );

    const $mensaje = $("#mensaje_verificador_buscar");

    if (!contacto_encontrado) {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-danger")
            .text("Contacto no encontrado");

        setTimeout(() => {
            $mensaje.addClass("d-none");
        }, 2000);

        return false;
    }

    contacto_actual = contacto_encontrado;

    $("#datosContacto").html(`
        <p><strong>Nombre:</strong> ${contacto_encontrado.nombre}</p>
        <p><strong>Alias:</strong> ${contacto_encontrado.alias}</p>
        <p><strong>Cuenta:</strong> ${contacto_encontrado.cuenta}</p>
        <p><strong>Banco:</strong> ${contacto_encontrado.banco}</p>
    `);

    $("#mostrar")
        .removeClass("d-none")
        .addClass("alert-success");

    return false;
}

//Funciones de Transferencia

//Funcion para transferir
function transferir() {

    const monto_transferir = Number($("#dinero").val());
    const saldo_actual = Number(localStorage.getItem("saldo"));
    let transacciones = JSON.parse(localStorage.getItem("transacciones")) || [];

    const $mensaje = $("#mensaje_verificador_transferir");

    $mensaje
        .removeClass("alert-success alert-warning alert-danger")
        .addClass("d-none");

    
    if (!contacto_actual) {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-warning")
            .text("Debe seleccionar un contacto antes de transferir");
        return false;
    }

   
    if (isNaN(monto_transferir) || monto_transferir <= 0) {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-warning")
            .text("Ingrese un monto válido para transferir");
        return false;
    }

 
    if (monto_transferir > saldo_actual) {
        $mensaje
            .removeClass("d-none")
            .addClass("alert-warning")
            .text("Su saldo actual es menor al monto que quiere transferir");
        return false;
    }


    const nuevo_saldo = saldo_actual - monto_transferir;

    const nueva_transaccion = {
        contacto: contacto_actual,
        monto: monto_transferir,
        tipo: "envio",
        fecha: new Date().toLocaleString()
    };

    transacciones.push(nueva_transaccion);

    localStorage.setItem("transacciones", JSON.stringify(transacciones));
    localStorage.setItem("saldo", nuevo_saldo.toString());

    $mensaje
        .removeClass("d-none")
        .addClass("alert-success")
        .text(
            "Transferencia realizada correctamente a " +
            contacto_actual.nombre +
            " por $" +
            formatear_moneda(monto_transferir)
        );

    setTimeout(() => {
        $("#mostrar").addClass("d-none");
        $mensaje.addClass("d-none");
    }, 4000);

    $("#dinero").val("");
    $("#buscador").val("");

    return false;
}


//Historial

//Funcion para mostrar ulitmos movimientos

function cargar_transacciones() {

    const transacciones = JSON.parse(localStorage.getItem("transacciones")) || [];
    const $cuerpo_tabla = $("#listaTransacciones");

    $cuerpo_tabla.empty();

    if (transacciones.length === 0) {
        $cuerpo_tabla.html(`
            <tr>
                <td colspan="2" class="text-center text-muted">
                    No hay transacciones registradas
                </td>
            </tr>
        `);
        return;
    }

    transacciones.forEach(transaccion => {

        let tipo_movimiento = "";
        let clase_monto = "";
        let signo = "";

        if (transaccion.tipo === "envio") {
            tipo_movimiento = `📤 Transferencia a: ${transaccion.contacto.nombre}`;
            clase_monto = "amount-negative";
            signo = "-";
        } else {
            tipo_movimiento = "💰 Depósito";
            clase_monto = "amount-positive";
            signo = "+";
        }

        $cuerpo_tabla.append(`
            <tr>
                <td>
                    ${tipo_movimiento}
                    <br>
                    <small class="text-muted">${transaccion.fecha}</small>
                </td>
                <td class="text-end ${clase_monto}">
                    ${signo}$${formatear_moneda(transaccion.monto)}
                </td>
            </tr>
        `);
    });
}


//Funciones de Menu

// Mostrar / ocultar menú de sesión
function toggle_menu() {
    $("#menu-dropdown").fadeToggle(150);
}

// Cerrar sesión
function cerrar_sesion() {
     window.location.href = "/";
}


//JQUERY
//Eventos de JQuery

$(document).ready(function () {

    //Login

    $("#form-login").on("submit", function (e) {
        e.preventDefault(); // evita recarga
        verificador();
    });

    //Deposit

    $("#form-deposito").on("submit", function (e) {
        e.preventDefault();
        depositar();
    });

    //Ocultar formulario (agregar contacto)en sendmoney

    $("#btn-toggle-contacto").on("click", function () {
        ocultar_formulario();
    });

    //Agregar contacto en sendmoney

    $("#form-agregar-contacto").on("submit", function (e) {
        e.preventDefault();
        agregar_contacto();
    });

    //Buscar contacto en sendmoney

    $("#form-buscar-contacto").on("submit", function (e) {
        e.preventDefault();
        buscar_contactos();
    });

    //Transferir en sendmoney

    $("#form-transferir").on("submit", function (e) {
        e.preventDefault();
        transferir();
    });

    //Ver transacciones

    if ($("#listaTransacciones").length) {
        cargar_transacciones();
    }

    //Menu esquina superior 
    $("#btn-menu").on("click", function (e) {
        e.stopPropagation(); 
        toggle_menu();
    });

    //Mostrar saldo en pantalla menu
    if ($("#saldo").length) {
        mostrar_saldo();
    }

    //Cerrar sesion btn
    $("#btn-cerrar-sesion").on("click", function () {
        cerrar_sesion();
    });
});
