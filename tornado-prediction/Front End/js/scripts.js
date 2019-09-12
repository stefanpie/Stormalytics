//First things first the radar location
/*
csvParser is an object from the jquery-csv library that parses
csvs into arrays. gotta make this object to use it.
Needs the jquer-csv API
*/
var csvParser = jQuery = require('jquery');
require('./jquery.csv.js');
var userLoc = []; //user's location, long, then lat.
var radars = []; //list of all radars
radars = csvParser.csv.toArrays(csv); //puts 2d array into radars.
//binary search modified to find point where a value should be inserted
//in an decreasing list. Returns the index
function modBinarySearch (list, value) {
  // initial values for start, middle and end
  let start = 0
  let stop = list.length - 1
  let middle = Math.floor((start + stop) / 2)

  // While the middle is not what we're looking for and the list does not have a single item
  while ((stop - start) > 1) {
    if (value <= list[middle]) {
      stop = middle
    } else {
      start = middle
    }

    // recalculate middle on every iteration
    middle = Math.floor((start + stop) / 2)
  }

  if (list[start] > value) {
    return start;
  } else {
    return stop;
  }

  return null;
}

function findCloseRadars(radars, location) {
    var i;
    var closeRadarsDist = [1000000000]; //purposely high initial seed val.
    var closeRadarsIndex = [];

    for(i = 0; i < radars.length; i++){
        // 3rd entry in 2nd array of radars is longitude, 4th entry is lat
        // compare to userloc values for differences.
        var latDiff = location[0] - radars[i][3]; 
        var longDiff = location[1] - radars[i][4];
        var dist = Math.sqrt(latDiff**2 + longDiff**2);

        radarIndexPostition = modBinarySearch(closeRadars, dist);
        closeRadarsDist.splice(radarIndexPostition, 0, dist);
        closeRadarsIndex.splice(radarIndexPostition, 0, i);
        // A radar's identity in the closest radar list is its index in original radars[].
        // Find the smallest distance, and return the radars corresponding

    }
    var closeRadars = [];
    var j;
    for (j = 0; j < closeRadarsIndex.length; j++){
        var index = closeRadarsIndex[j];
        closeRadars.push(radars[index]);
    }

    return closeRadars;
//figure out how to sort by the dist and then return the station
//associated with that dist. This is like 1301 come on now.
}

var closeRadars = findCloseRadars(radars, userLoc);

function makeRadarUL(listHTMLID, list){
    var a = '<ol>',
        b = '</ol>',
        m = [];

    // Right now, this loop only works with one
    // explicitly specified array (options[0] aka 'set0')
    for (i = 0; i < list.length; i += 1){
        m[i] = '<li>' + list[i][0] + " " + list[i][1] + ", " + list[i][2] + '</li>';
    }

    document.getElementById(listHTMLID).innerHTML = a + m + b;
}

ulListID = "radarlist";
makeRadarUL(ulListID, closeRadars);
//---------------------------------------------------------------------

var mymap = L.map('mapid').setView([33.7762, -84.40], 15);
//Classroom coords 33.7791, -84.40401, zoom 19
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoid2NuMjAxOCIsImEiOiJjanMzdXQ0ZG8wNjVoNDVvNnRjZms2ZTR1In0.e7_eAXyA1XghoAgg-Vutmg'
}).addTo(mymap);
