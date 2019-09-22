var test = "Hello World!";
console.log(test);

var hurricane_map = L.map('hurricane-map').setView([33.774432, -84.396404], 10);

var tile_layer = L.tileLayer('http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
	attributionControl: false
}).addTo(hurricane_map);
