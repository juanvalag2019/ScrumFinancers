let myChart = echarts.init(document.getElementById('stock-chart'));
const MILLIS_PER_MINUTE = 60000;
let currentDate = new Date();
let value = 100;

let exampleData = [
    {
        "stock": "GOOGL",
        "history": [
            {
                "value": 180.10,
                "timestamp": new Date(currentDate - 5 * MILLIS_PER_MINUTE)
            },
            {
                "value": 215.10,
                "timestamp": new Date(currentDate)
            }
        ]
    },
    {
        "stock": "AMZN",
        "history": [

            {
                "value": 150.10,
                "timestamp": new Date(currentDate - 5 * MILLIS_PER_MINUTE)
            },
            {
                "value": 202.10,
                "timestamp": new Date(currentDate)
            }
        ]
    }
]

let series = exampleData.map(function (stock) {
    return {
        type: 'line',
        showSymbol: false,
        data: stock['history'].reduce(function (acc, curr) {
            acc.push({
                name: curr.timestamp.toString(),
                value: [curr.timestamp.toISOString(), curr.value]
            })
            return acc
        }, [])
    }
})


// Specify the configuration items and data for the chart
let option = {
    title: {
        text: 'Stock values'
    },
    xAxis: {
        type: 'time',
        splitLine: {
            show: false
        }
    },
    yAxis: {
        type: 'value'
    },
    tooltip: {
        order: 'valueDesc',
        trigger: 'axis'
    }
    ,
    series: series
};

function randomData(last) {
    if (!last) {
        currentDate = new Date(+currentDate + 1000 * 60);
    }
    value = value + Math.random() * 21 - 10;
    return {
        name: currentDate.toString(),
        value: [
            currentDate.toISOString(),
            Math.round(value)
        ]
    };
}

setInterval(function () {
    series[0].data.push(randomData());
    series[1].data.push(randomData(true));

    myChart.setOption({
        series: series
    });
}, 1000);

// Display the chart using the configuration items and data just specified.
myChart.setOption(option);