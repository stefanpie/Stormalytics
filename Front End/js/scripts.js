var mymap = L.map('mapid').setView([33.7762, -84.40], 15);
//Classroom coords 33.7791, -84.40401, zoom 19
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoid2NuMjAxOCIsImEiOiJjanMzdXQ0ZG8wNjVoNDVvNnRjZms2ZTR1In0.e7_eAXyA1XghoAgg-Vutmg'
}).addTo(mymap);
//This is to pass the list of satellites into html:
var radars = [
        //pass in the list of nearest radars here, ordered.
        ]

function makeUL(){
    var a = '<ol>',
        b = '</ol>',
        m = [];

    // Right now, this loop only works with one
    // explicitly specified array (options[0] aka 'set0')
    for (i = 0; i < radars.length; i += 1){
        m[i] = '<li>' + radars[i] + '</li>';
    }

    document.getElementById('radarlist').innerHTML = a + m + b;
}
