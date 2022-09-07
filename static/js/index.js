let stockChart;
const LINE_CHART_CONFIG = {
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
    },
};

function initializeLineChart(elementId, initialSeriesData = []) {
    let chart = echarts.init(document.getElementById(elementId));
    let chartConfig = Object.assign(LINE_CHART_CONFIG);
    chartConfig.series = initialSeriesData;
    chart.setOption(chartConfig);
    return chart;
}

function convertAssetsToChartSeries(assets, historyAttribute) {
    return assets.map(function (asset) {
        let seriesTemplate = getLineChartSeriesTemplate();
        asset[historyAttribute].reduce(function (updates, assetUpdate) {
            updates.push(toTimeSeriesDataFormat(assetUpdate['timestamp'], assetUpdate['value']));
            return updates;
        }, seriesTemplate.data);
        return seriesTemplate;
    });
}

function toTimeSeriesDataFormat(timestamp, value) {
    return {
        name: timestamp.toString(),
        value: [timestamp.toISOString(), value]
    };
}

function getLineChartSeriesTemplate() {
    return {
        type: 'line',
        showSymbol: false,
        data: []
    };
}

function getStockExampleData() {
    const MILLIS_PER_MINUTE = 60000;
    let currentDate = new Date();
    return [
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
    ];
}

stockChart = initializeLineChart('stock-chart', convertAssetsToChartSeries(getStockExampleData(), 'history'));