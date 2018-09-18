var url = "/avail-json";
d3.json(url, function(response){
    myData = Object.values(response); 
    var myChart = document.getElementById("avail").getContext('2d');

    var not_avail = [];
    var avail = [];
    myData.forEach(data => {
        if(data.available == 'f') {
            not_avail.push({
                y:data.count,
                // 'x': new Date(data.date)
                x: data.date
            });
        }
        else avail.push({
            y:data.count,
            // 'y': new Date(data.date)
            x: data.date
        });
    });
    console.log(avail);
    var theChart = new Chart(myChart, {
        type:'line', //bar, horizontalBar, pie, line, doughnut, radar, polarArea
        data: {
            //labels: myData.map(d => d.bedrooms),
            datasets: [{
                label: 'Listings',
                data: avail,
                //data: myData.map(d => d.value),
                backgroundColor: [
                    'LightSalmon',
                    'LightGray'
                ],
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