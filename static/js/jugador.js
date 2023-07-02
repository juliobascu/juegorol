function actualizarSelectHabilidades(opcionSeleccionada, idOtroSelect) {
    var otroSelect = document.getElementById(idOtroSelect);


    for (var i = 0; i < otroSelect.options.length; i++) {
        if (otroSelect.options[i].value === opcionSeleccionada) {
            console.log("FUNCIONA")
            otroSelect.options[i].hidden = true
        } else {
            otroSelect.options[i].hidden = false
        }
    }
}

console.log("Funciona")