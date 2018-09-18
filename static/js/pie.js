/* pie route */
var url = "/pie-json";

function buildPlot() {
  d3.json(url, function(response) {

    //console.log(response);
    var data = [{
      values: response.map(data => data.id),
      labels: response.map(data => data.neighbourhood),
      type: "pie"
    }];
    var layout = {
      height: 400,
      width: 600,
      paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };
  Plotly.plot("pie", data, layout);
  });
}
buildPlot();
