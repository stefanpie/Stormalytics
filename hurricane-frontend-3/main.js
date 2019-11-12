var my_map = null;
$(document).ready(function() {
    my_map = L.map('leaflet-map').setView([25.734677, -80.162236], 6);

    var tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attributionControl: false,
        timeDimension: true,
        timeDimensionOptions: {
            timeInterval: "2014-09-30/2014-10-30",
            period: "PT1H"
        }
    });
    tileLayer.addTo(my_map);
    document.getElementsByClassName('leaflet-control-attribution')[0].style.display = 'none';
    // var timeDimension = L.timeDimension();
    // timeDimension.addTo(map);



});

$("#strom-select-table>tbody>tr").click(function() {
    console.log("clicked");
    $(this).addClass("selected").siblings().removeClass("selected");
});