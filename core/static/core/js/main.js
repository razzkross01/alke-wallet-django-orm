// ========================================
// ALKE WALLET - JS LIMPIO (DJANGO)
// ========================================


// =============================
// MENÚ DESPLEGABLE
// =============================
function toggle_menu() {
    $("#menu-dropdown").stop(true, true).fadeToggle(150);
}


// =============================
// DOCUMENT READY
// =============================
$(document).ready(function () {

    // =============================
    // MENÚ USUARIO
    // =============================

    $("#menu-dropdown").hide();

    $("#btn-menu").on("click", function (e) {
        e.stopPropagation(); // evita que se cierre inmediatamente
        toggle_menu();
    });

    // Cerrar menú al hacer click fuera
   $(document).on("click", function (e) {
        if (!$(e.target).closest(".menu-container").length) {
            $("#menu-dropdown").fadeOut(150);
        }
    });
    


    // =============================
    // TOGGLE CONTACTOS (SEND MONEY)
    // =============================
    $("#toggle-contactos").on("click", function () {

        const lista = $("#lista-contactos");

        lista.slideToggle(200);

        $(this).toggleClass("activo");

        if ($(this).hasClass("activo")) {
            $(this).text("Ocultar contactos");
        } else {
            $(this).text("Ver contactos");
        }

    });


    // =============================
    // AUTOCOMPLETAR CONTACTO
    // =============================
    $(".usar-contacto").on("click", function () {

        const cuenta = $(this).data("cuenta");
        const nombre = $(this).data("nombre");

        $("#numero_cuenta").val(cuenta);
        $("#nombre_destinatario").val(nombre);

    });

});


// =============================
// MENSAJES DJANGO (AUTO HIDE)
// =============================
setTimeout(function () {

    $("#contenedor-mensajes .alert").fadeOut(600);

}, 2000);   

//Funcion para redigir a paginas 
function redirigir(pagina_destino, tiempo = 2500) { 
    setTimeout(() => {
        window.location.href = pagina_destino;
    }, tiempo);
}
