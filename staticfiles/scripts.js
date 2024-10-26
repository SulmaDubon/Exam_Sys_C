document.addEventListener('DOMContentLoaded', function () {
    var tiempoRestante = parseInt(document.getElementById('temporizador').getAttribute('data-tiempo-restante')) || 0;

    function iniciarTemporizador(duracion) {
        var display = document.getElementById('temporizador');
        var timer = duracion;
        var hours, minutes, seconds;

        var interval = setInterval(function () {
            hours = Math.floor(timer / 3600);
            minutes = Math.floor((timer % 3600) / 60);
            seconds = timer % 60;

            display.textContent = hours.toString().padStart(2, '0') + ":" +
                                  minutes.toString().padStart(2, '0') + ":" +
                                  seconds.toString().padStart(2, '0');

            if (--timer < 0) {
                clearInterval(interval);
                // Cuando el temporizador termine, envía el formulario automáticamente
                document.getElementById('formularioExamen').submit();
            }
        }, 1000);
    }

    iniciarTemporizador(tiempoRestante);
});
