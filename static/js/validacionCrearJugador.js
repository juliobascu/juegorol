$(document).ready(function() {
    $("#formCrearPersonaje").validate({
        rules: {
            nombreJ: {
                required: true
            },
            nombreP: {
                required: true,
                minlength: 5
            },
            nivel: {
                required: true
            },
            estado: {
                required: true
            },
            raza: {
                required: true
            },
            habilidad1: {
                required: true
            },
            habilidad2: {
                required: true
            },
            poder: {
                required: true
            },
            equipamiento: {
                required: true
            }
        }
    })

    jQuery.extend(jQuery.validator.messages, {
        required: "Este campo es obligatorio.",
        number : "Este campo debe contener solo números",
        minlength: jQuery.validator.format("Ingresa al menos {0} carácteres."),
        min: jQuery.validator.format("Ingresa un valor minimo de {0}."),
    })
})