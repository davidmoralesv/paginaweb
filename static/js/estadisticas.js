function estadistica(){
    $.ajax({
      type: "POST",
      url: "/Estadisticas",
      dataType: "json",
      contentType: "application/json;charset=utf-8"
    })
    .done(function(value){
        humedad = value.valor_humedad;
        humedad = humedad;
        console.log(humedad)
        $("#customer").click(function(){
            custom(humedad);
        });

        $("#customer").click();

        grados = value.data_value+"°C";
        altura = value.height+"%";

        $("#temperature").height(altura).attr("data-value", grados);
    });
}

$(document).ready(function(){
 setInterval(estadistica,1000*6);
});
