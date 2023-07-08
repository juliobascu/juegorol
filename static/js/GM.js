function buscarPersonaje() {
    var id = document.getElementById('idpj').value;
    var url = '/personaje/' + id;

    $.ajax({
        url: url,
        method: 'GET',
        success: function(response) {
            mostrarDetallesPersonaje(response);
            console.log(response)
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function mostrarDetallesPersonaje(personaje) {
    var modalBody = document.querySelector('#personajemodal .modal-body');
    var poderesJugador = personaje[7];
    var poderesBase = personaje[8]; 
    var formularioHTML = "";
    formularioHTML += '<form class="row">';

    formularioHTML += '<div class="mb-3">';
    formularioHTML += '<label for="idP">Id Personaje:</label>';
    formularioHTML += '<input type="text" class="form-control" id="idP" disabled value="' + personaje[0] + '">';
    formularioHTML += '</div>';

    formularioHTML += '<div class="mb-3">';
    formularioHTML += '<label for="nombre">Nombre:</label>';
    formularioHTML += '<input type="text" class="form-control" id="nombre" value="' + personaje[3] + '">';
    formularioHTML += '</div>';

    formularioHTML += '<div class="mb-3">';
    formularioHTML += '<label for="raza">Raza:</label>';
    formularioHTML += '<input type="text" class="form-control" id="raza" value="' + personaje[4] + '">';
    formularioHTML += '</div>';

    formularioHTML += '<div class="mb-3">';
    formularioHTML += '<label for="nivel">Nivel:</label>';
    formularioHTML += '<input type="text" class="form-control" id="nivel" value="' + personaje[5] + '">';
    formularioHTML += '</div>';

    formularioHTML += '<div class="mb-3">';
    formularioHTML += '<label for="estado">Estado:</label>';
    formularioHTML += '<input type="text" class="form-control" id="estado" value="' + personaje[6] + '">';
    formularioHTML += '</div>';

    for (var i = 1; i <= 4; i++) {
        formularioHTML += '<div class="mb-3 col-6">';
        formularioHTML += '<label>Poder ' + i + ':</label>';

        if (i === 1) {
            formularioHTML += '<select class="form-control" id="select' + i + '" disabled> <option value="' + poderesJugador[0] + '">' + poderesJugador[0] + '</option>';
        } else if (i > 1 && i <= 4) {
            formularioHTML += '<select class="form-control" id="select' + i + '">';
            for (var j = 1; j < poderesJugador.length; j++) {
                formularioHTML += '<option value="' + poderesJugador[j] + '">' + poderesJugador[j] + '</option>';
                for (var b = 0; b < poderesBase.length; b++) {
                    if (poderesJugador[b] === poderesBase[b]){
                        formularioHTML += '<option value="El Julio hace caca"</option>';
                        formularioHTML += '<option value="' + poderesBase[b] + '">' + poderesBase[b] + '</option>';
                        console.log(poderesBase[b])
                        console.log(poderesJugador)
                    }else{
                        formularioHTML += '<select class="form-control" id="select">';
                        formularioHTML += '<option value=""></option>'
                        for (var j = 0; j < poderesBase.length; j++) {
                        formularioHTML += '<option value="' + poderesBase[j] + '">' + poderesBase[j] + '</option>';
                        }
                    }
                }
            }

        }

        formularioHTML += '</select>';
        formularioHTML += '</div>';
    }

    formularioHTML += '</form>';

    modalBody.innerHTML = formularioHTML;
}


  