$(document).ready(function() {
  $("[type=checkbox]").change(function() {
   var url_nombre = "";
   var cuartos =["foco_cuarto1", "foco_cuarto2"]
   var puertas_y_dispositivos = ["puerta1","monitor1", "ventilador"]

   var nombre = $(this).attr("name");
   var estado = $(this).prop("checked");

if (cuartos.includes(nombre)){
    url_nombre = "/" + "Cuartos";
    }
if  (puertas_y_dispositivos.includes(nombre)){
    url_nombre = "/" + "Puertas";
    }

   $.ajax({
    url: url_nombre,
    type: "post",
     data: {nombre: nombre, estado: estado},
     success: function(response) {
      $(".status").html(response);
     },
     error: function(xhr) {
      //Do Something to handle error
     }
   });
   });
});