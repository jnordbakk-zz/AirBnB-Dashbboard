
var url = "/bedroomprice-json";
d3.json(url, function(response){
    myData = Object.values(response); 
    var myChart = document.getElementById("myChartjs").getContext('2d');

    var theChart = new Chart(myChart, {
        type:'doughnut', //bar, horizontalBar, pie, line, doughnut, radar, polarArea
        data: {
            labels: myData.map(d => d.bedrooms),
            datasets: [{
                label: 'Listings',
                data: myData.map(d => d.value),
                backgroundColor: [
                    'LightSalmon',
                    'LightPink',
                    'Tomato',
                    'SteelBlue',
                    'BurlyWood',
                    'PeachPuff',
                    'LightGreen',
                    'LightGray',
                    'Olive'
                ],
                borderWidth: 1,
                borderColor: 'White',
                hoverBorderWidth: 2,
                hoverBorderColor: 'Teal'
            }]
        },
        options: {
            title:{
                text: 'Number of Listings Per Number of Bedrooms'
            },
            legend: {
                position: 'left' //left, top, bottom, right
            }
        } 
    });
});
    
