var user_location = [33.775620, -84.396286]
var user_location_marker = null;
var stations = []
var current_station = null;
var current_station_marker = null;
var national_composite_layer = null;
var individual_dopplar_layer = null;
var nexrad_layer = null;


var map = L.map('map').setView(user_location, 8);
var tile_layer = L.tileLayer('http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
	attributionControl: false
}).addTo(map);

nexrad_layer = L.tileLayer('http://www.mesonet.agron.iastate.edu/cache/tile.py/1.0.0/nexrad-n0q-900913/{z}/{x}/{y}.png', {
	opacity: 0.5
}).addTo(map);
L.control.scale().addTo(map);


var baseLayers = {
	"OpenStreetMap": tile_layer
};
var overlays = {
	"Doppler Weather Radar": nexrad_layer
};
L.control.layers(baseLayers, overlays,{hideSingleBase: true}).addTo(map);

if ("geolocation" in navigator) {
	/* geolocation is available */
} else {
	/* geolocation IS NOT available */
	console.log("Geolocation is not available");
}

navigator.geolocation.getCurrentPosition(function (position) {
	user_location = [position.coords.latitude, position.coords.longitude];
	map.setView(user_location, 8);
	user_location_marker = L.marker(user_location).addTo(map).bindPopup("User Location");
	calculate_and_set_nearest_staion()
});

Papa.parse("./stations.csv", {
	download: true,
	header: true,
	dynamicTyping: true,
	complete: function (results) {
		stations = results.data;
		calculate_and_set_nearest_staion();
	}
});

function distance(lat1, lon1, lat2, lon2) {
	if ((lat1 == lat2) && (lon1 == lon2)) {
		return 0;
	} else {
		var radlat1 = Math.PI * lat1 / 180;
		var radlat2 = Math.PI * lat2 / 180;
		var theta = lon1 - lon2;
		var radtheta = Math.PI * theta / 180;
		var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
		if (dist > 1) {
			dist = 1;
		}
		dist = Math.acos(dist);
		dist = dist * 180 / Math.PI;
		dist = dist * 60 * 1.1515;
		dist = dist * 1.609344
		return dist; // in km
	}
}

function nearest_station() {
	var stations_with_distance = stations.map(function (x) {
		var d = distance(x['LATITUDE'], x['LONGITUDE'], user_location[0], user_location[1])
		x.d = d;
		return x
	});
	// console.log(stations_with_distance);
	var sorted_stations = stations_with_distance.sort(function (a, b) {
		return a.d - b.d;
	});
	// console.log(sorted_stations);
	var s = sorted_stations[0];
	delete s['d'];
	return s;
}

function calculate_and_set_nearest_staion() {
	current_station = nearest_station();
	if (current_station_marker != null) {
		map.removeLayer(current_station_marker);
	}

	current_station_marker = L.marker([current_station['LATITUDE'], current_station['LONGITUDE']]).addTo(map);
	current_station_marker.bindPopup("Selected Radar:<br>" + current_station['STATION_ID'] + " - " + current_station['STATION']);
	$('#current-station-data').text(current_station['STATION_ID'] + " - " + current_station['STATION']);

}

