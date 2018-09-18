var lineURL = "/avail-json";

function buildLine() {
  d3.json(lineURL, function(lineResponse) {
      //console.log(response);
    var LineData = Object.values(lineResponse); 
    //console.log(myData);

    var not_avail = [];
    var avail = [];
    LineData.forEach(ldata => {
        if(ldata.available == 'f') {
            not_avail.push({
                'count':ldata.count,
                'dateString': ldata.date,
                'date': new Date(ldata.date)
            });
        }
        else avail.push({
            'count':ldata.count,
            'dateString': ldata.date,
            'date': new Date(ldata.date)
        });
    });
    //console.log(avail);
    var lineDatasets = [
        {
            y: avail.map(adata => adata.count),
            x: avail.map(adata => adata.date),
            type: "line",
            name: "Available Listings"
        },
        {
            y: not_avail.map(bdata => bdata.count),
            x: not_avail.map(bdata => bdata.date),
            type: "line",
            name: "Unavailable Listings"
        },
    ];
    var lineTitle = "Availability over time";
    var lineYaxis = "Listings available/unavailable";
    var lineLayout = {
    title: lineTitle,
    yaxis: { title: lineYaxis}
    };
  
    Plotly.newPlot("linePlot", lineDatasets, lineLayout);
  });
}
buildLine();