$(document).ready(function () {
    $('.sidenav').sidenav();
});


$(document).ready(function () {
    var map = L.map('mapid').setView([25.734677, -80.162236], 6);

    var tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attributionControl: false
    });
    tileLayer.addTo(map);
    document.getElementsByClassName('leaflet-control-attribution')[0].style.display = 'none';

});