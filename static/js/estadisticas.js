function estadistica(){
    $.ajax({
      type: "POST",
      url: "/Estadisticas",
      dataType: "json",
      contentType: "application/json;charset=utf-8"
    })
    const units = {
	Celcius: "°C",
	Fahrenheit: "°F"
    };

    const config = {
	minTemp: -20,
	maxTemp: 50,
	unit: "Celcius"
    };

    $("#custom").click();
}

$(document).ready(function(){
 setInterval(estadistica,1000*6);
});
