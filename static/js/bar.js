/* pie route */
var barUrl = "/list-count-json";
var chartTitle = "Listings per Neighbourhood";
var chartYaxis = "Number of Listings";
function buildPlot() {
  d3.json(barUrl, function(response) {
      //console.log(response);
    var myData = Object.values(response); 
    //console.log(myData);
    var data = [{
      y: myData.map(data => data.value),
      x: myData.map(data => data.neighbourhood),
      type: "bar"
    }];

    var layout = {
      title: chartTitle,
      yaxis: { title: chartYaxis}
    };

  Plotly.newPlot("bar_plot", data, layout);
  });
}
buildPlot();

// Submit Button handler
function handleSubmit1() {
  // Prevent the page from refreshing
  d3.event.preventDefault();
  // Build the plot with the new stock
  barUrl = "/list-count-json";
  chartTitle = "Listings per Neighbourhood"; 
  chartYaxis = "Number of Listings";
  buildPlot();
}

function handleSubmit2() {
  // Prevent the page from refreshing
  d3.event.preventDefault();
  // Build the plot with the new stock
  barUrl = "/maxprice-json";
  chartTitle = "Max Price per Neighbourhood";
  chartYaxis = "Max Price";
  buildPlot();
}

function updatePlotly(newdata) {
  Plotly.restyle("bar", "x", [newdata.x]);
  Plotly.restyle("bar", "y", [newdata.y]);
}

// // Add event listener for submit button
d3.select("#button1").on("click", handleSubmit1);
d3.select("#button2").on("click", handleSubmit2);