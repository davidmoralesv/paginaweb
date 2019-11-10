/*
function countMyself() {
    // Check to see if the counter has been initialized
    if ( typeof countMyself.counter == 'undefined' ) {
        // It has not... perform the initialization
        countMyself.counter = 0;
    }
    return ++countMyself.counter;
}*/
function estadistica(){
    $.ajax({
      type: "POST",
      url: "/Estadisticas",
      dataType: "json",
      contentType: "application/json;charset=utf-8"
    })
    .done(function(value){
        humedad = value.valor_humedad;
//        humedad = humedad + countMyself();
        humedad = humedad;
        console.log(humedad)
        $("#customer").click(function(){
            custom(humedad);
        });

        $("#customer").click();

     /*   grados = value.data_value+countMyself()+"°C";
        altura = value.height+countMyself()+"%";*/

        grados = value.data_value+"°C";
        altura = value.height+"%";

        $("#temperature").height(altura).attr("data-value", grados);
    });
}

$(document).ready(function(){
 setInterval(estadistica,1000*6);
});
