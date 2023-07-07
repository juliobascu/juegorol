function verificarSelectRaza() {
    var selectRaza = document.getElementById("selectRaza")
    var divHabilidadesYEquip = document.getElementById("habilidadEquipoJugador")
    var selectPoderes = document.getElementById("selectPoder")
    if (selectRaza.value != "") {
        divHabilidadesYEquip.hidden = false
        fetch('/actualizarPoderes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ raza : selectRaza.value })
        })
            .then(function (response) {
                return response.json()
            })
            .then(function (data) {
                let selectActualizado = "<option selected value=''>Seleccionar poder</option>"
                for (let i = 0; i < data.poderes.length; i++) {
                    selectActualizado += `<option value=${data.poderes[i][0]}>${data.poderes[i][0]}</option>`
                }
                console.log(selectActualizado)
                selectPoderes.innerHTML = selectActualizado
            })
            .catch(function (error) {
                console.log(error)
            });
    } else {
        divHabilidadesYEquip.hidden = true
    }
}

function actualizarSelectHabilidades(opcionSeleccionada, idOtroSelect) {
    var otroSelect = document.getElementById(idOtroSelect);


    for (let i = 0; i < otroSelect.options.length; i++) {
        if (otroSelect.options[i].value === opcionSeleccionada) {
            otroSelect.options[i].hidden = true
        } else {
            otroSelect.options[i].hidden = false
        }
    }
}

console.log("Funciona")