String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1)
}

var my_map = null;
$(document).ready(function() {
    my_map = L.map('leaflet-map').setView([27, -78], 5);

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

var current_hurricane_data = null;
var current_hurricane_layer = null;

var hurdat_data = [];
axios.get("./hurdat2_1950.json")
    .then(function(response) {
        hurdat_data = response.data;
        updateHurricaneSelectTable();
    })
    .catch(function(error) {
        console.log(error);
    });


$("input[name='storm-name'], input[name='storm-year']").on('input', function() {
    // console.log("filter input chnaged");
    updateHurricaneSelectTable();
});

function updateHurricaneSelectTable() {
    var storm_name = $("input[name='storm-name']").val().replace(' ', '').toLowerCase();
    var storm_year = $("input[name='storm-year']").val().replace(' ', '').toLowerCase();
    storm_year = parseInt(storm_year);

    var filtered_data = hurdat_data;

    if (storm_year) {
        filtered_data = filtered_data.filter(function(element) {
            return element['fixes'][0]['year'] === storm_year;
        });
    }

    if (storm_name) {
        filtered_data = filtered_data.filter(function(element) {
            return element['storm_name'].replace(' ', '').toLowerCase().includes(storm_name.replace(' ', '').toLowerCase());
        });
    }
    console.log(filtered_data);

    // $("#strom-select-table > tbody").html("");
    $("#strom-select-table > tbody").empty();

    filtered_data.forEach(function(element) {
        $("#strom-select-table > tbody").append('<tr id="' + element['ATCF_code'] + '"><td>' + element['storm_name'].toLowerCase().capitalize() + '</td><td>' + element['fixes'][0]['year'] + '</td></tr>');
    });


    $("#strom-select-table>tbody>tr").click(function() {
        console.log("clicked");
        $(this).addClass("selected").siblings().removeClass("selected");
        var selected_storm_id = $(this).attr('id');
        var selected_strom_data = filtered_data.filter(function(element) {
            return element['ATCF_code'] === selected_storm_id;
        });
        selected_strom_data = selected_strom_data[0];
        current_hurricane_data = selected_strom_data;
        console.log(current_hurricane_data);

        updateCurrentHurricaneLayer();
    });
}

function updateCurrentHurricaneLayer() {
    if (current_hurricane_layer !== null) {
        my_map.removeLayer(current_hurricane_layer);
    }
    current_hurricane_layer = L.layerGroup();
    current_hurricane_data['fixes'].forEach(function(element) {
        var marker_svg = `
        <svg viewBox="0 0 100 100">
            <circle cx="50" cy="50" r="25" fill="${hurricneScaleColorCalculator(element['max_sus_wind'])}" stroke="black" stroke-width="5" stroke-alignment="inner"/>
        </svg>`
        console.log(marker_svg);
        var divIcon = L.divIcon({
            className: "leaflet-data-marker",
            html: marker_svg,
            // iconAnchor: [18, 42],
            iconSize: [20, 20]
        });
        var marker = L.marker([element['latitude'], element['longitude']], { icon: divIcon });
        marker.addTo(current_hurricane_layer);
    });

    var polylinePoints = current_hurricane_data['fixes'].map(function(element) {
        return [element['latitude'], element['longitude']];
    });
    var polyline = L.polyline(polylinePoints);
    polyline.addTo(current_hurricane_layer);

    current_hurricane_layer.addTo(my_map);
}

function hurricneScaleColorCalculator(wind_speed) {
    function between(x, min, max) {
        return x >= min && x <= max;
    }

    if (between(wind_speed, 0, 33)) {
        return "#5ebaff";
    }
    if (between(wind_speed, 33, 63)) {
        return "#00faf4";
    }
    if (between(wind_speed, 63, 82)) {
        return "#ffffcc";
    }
    if (between(wind_speed, 82, 95)) {
        return "#ffe775";
    }
    if (between(wind_speed, 95, 112)) {
        return "#ffc140";
    }
    if (between(wind_speed, 112, 136)) {
        return "#ff8f20";
    }
    if (between(wind_speed, 136, 999)) {
        return "#ff6060";
    }

}