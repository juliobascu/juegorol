$(document).ready(function() {
    $('.tarjeta').click(function() {
        
        var nombrePersonaje = $(this).find('.item:nth-child(1)').text();
        var razaPersonaje = $(this).find('.item:nth-child(2)').text();
        var nivelPersonaje = $(this).find('.item:nth-child(3)').text();

        
        $('#nombrePersonaje').val(nombrePersonaje);
        $('#razaPersonaje').val(razaPersonaje);
        $('#nivelPersonaje').val(nivelPersonaje);

        
        $('#formularioModal').modal('show');
    });
});