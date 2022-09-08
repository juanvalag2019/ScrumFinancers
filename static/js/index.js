let stockChart;
let stockData = [];
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
const ASSETS_URLS = {
    stock: '/stocks',
    stockUpdates: '/stocks/updates'
}

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

function getStockData() {
    getRequest(ASSETS_URLS.stock,
        function (stocks) {
            stocks.forEach(function (stock) {
                stock['history'].forEach(function (stockUpdate) {
                    stockUpdate.timestamp = new Date(stockUpdate.timestamp);
                })
            })
            stockData = stocks;
            stockChart = initializeLineChart('stock-chart', convertAssetsToChartSeries(stockData, 'history'));
        },
        function (errorInfo) {
            console.log(errorInfo);
        });
}

function insertTableRowData(tableId, values) {
    console.log(values);
    let htmlToInsert = '<tr>'
    let rows = values.forEach(function (cellValue) { htmlToInsert += '<td>' + cellValue + '</td>' });
    htmlToInsert += '</tr>'
    console.log(htmlToInsert);
    $('#' + tableId).append(htmlToInsert);
}

function transformAssetsHistoriesToRows(assets, historyAttribute) {
    let rows = [];
    let histories = assets.map(function (asset) { return asset[historyAttribute] });
    histories[0].forEach(function (assetUpdate, idx) {
        let timestamp = assetUpdate.timestamp;
        let value1 = assetUpdate.value;
        let value2 = histories[1][idx].value;
        rows.push([formatDate(timestamp), value1, value2]);
    });
    return rows;
}

function formatDate(date) {
    let hours = date.getHours() / 12 > 1 ? date.getHours() % 12 : date.getHours();
    return `${date.getDate()}/${date.getMonth()}/${date.getFullYear()} ${hours}:${date.getMinutes()}:${date.getSeconds()}`;
}

stockChart = initializeLineChart('stock-chart', convertAssetsToChartSeries(getStockExampleData(), 'history'));
let tableRows = transformAssetsHistoriesToRows(getStockExampleData(), 'history');
tableRows.forEach(function (row) {
    insertTableRowData('assets-table', row);
});
