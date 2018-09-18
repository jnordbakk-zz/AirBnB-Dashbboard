
function chooseColor(price) {
  if(price<100){ return "#C0C0C0";}
  else if(price < 200){ return "#FF66FF";}
  else if(price < 300){ return "#6666FF";}
  else if(price < 400){ return "#66FFFF";}
  else if(price < 500){ return "#66FF66";}
  else if(price < 600){ return "#FFFF66";}
  else if(price < 700){ return "#FF6666";}
  else if(price > 800){ return "#330000";}

}

data = coord_data;

  // Once we get a response, send the data.features object to the createFeatures function
  //console.log(data);

  var myMap = L.map("map", {
    center: [37.7749, -122.4194],
    zoom: 12
  });

  // console.log(data.features);
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
    }).addTo(myMap);
  
  var featureList = data;

  featureList.forEach(feature =>{  
    var coords = [feature.latitude,feature.longitude];
    var price = feature.price;
    var image = feature.picture_url;
    //console.log(image);

    // var color = d3.scaleSequential(d3.interpolateLab("red", "black"))
    // .domain([0, 10]);
    var rad = 0;
    if (price > 175){ rad = 30 } else { rad = 15}
  //console.log(color(magnitude));
    var spot =  L.circle(coords, {
        color:chooseColor(parseInt(price)),
        fillColor: chooseColor(parseInt(price)),
        fillOpacity:0.8,
        radius: rad
      }).bindPopup("<h2>Price: " + price + "</h2>")
      .addTo(myMap);
  });

  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var colors = ["#C0C0C0","#FF66FF","#6666FF","#66FFFF","#66FF66","#FFFF66","#FF6666","#330000"];
    var labels = [" < 100 "," < 200 "," < 300 "," < 400 "," < 500 "," < 600 "," < 700 "," > 800"];
    
    for (var i = 0; i < labels.length; i++) {
      div.innerHTML +=
          '<i style="font-size: 10px; background-color:' + colors[i] + '">'+labels[i]+'</i><br>';
    }
    return div;
  };
  legend.addTo(myMap);