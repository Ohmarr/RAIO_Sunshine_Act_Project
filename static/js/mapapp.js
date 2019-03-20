
 //Creating our initial map object
 // We set the longitude, latitude, and the starting zoom level
 // This gets inserted into the div with an id of 'map'
 var myMap = L.map("map", {
   center: [41.850033, -87.6500523],
   zoom: 6
 });
 
 // Adding a tile layer (the background map image) to our map
 // We use the addTo method to add objects to our map
 L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
   attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
   maxZoom: 18,
   id: "mapbox.light",
   accessToken: API_KEY,
   zoom: 5,
   center: {lat: 41.443369776524136, lng: -87.25358963012695}
 }).addTo(myMap);
 

 // Loop to get State Name and border coordinates from GeoJson

 // Console.logging to make sure json data is there and then filter through data from console in browser to spot check
console.log(Object.entries(geoData))

function drawMap(state){
  // Create list variables
  var stateName = []
  var stateCoordinates = []
  var mapGeoJson = geoData
  var colorScale = chroma.scale('Set2').domain([0,51]).out('hex')
  // Actual loop to get state name and border coordinates
  for (var i = 0; i < geoData.features.length; i++) {
    mapGeoJson.features[i].properties.fillColor = colorScale(i)
    stateName.push(geoData.features[i].properties.NAME);
    stateCoordinates.push(geoData.features[i].geometry.coordinates);
  }

  // Console.logging to check that lists populated correctly from loop
  console.log(stateName)
  console.log(stateCoordinates[3])

  // Plot state coordinates list of border coordinates
  // var polygon = L.polygon([
  //   stateCoordinates[0]
  // ]).addTo(myMap);

  // var geoLayer = L.geoJson(geoData, {
  // 	style: function (feature) {
  // return {color: feature.properties.color};
  // 	},
  // 	onEachFeature: function (feature, layer) {
  // layer.bindPopup(feature.properties.description);
  // 	}
  // }).addTo(myMap);
  var geoLayer = L.geoJson(geoData, {
    style: function(feature) {return {fillColor: feature.properties.fillColor, color: feature.properties.fillColor}},
    //  style: console.log,
    onEachFeature: function (feature, layer) {
  layer.bindPopup(`${feature.properties.NAME}: ${feature.properties.STUSPS}`);
    }
  }).addTo(myMap);
}

drawMap("")

// d3.select("dropdown").on("change", function(){
//   state = "Texas"
//   drswMap(state)
// })