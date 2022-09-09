let stockChart;
let cryptoChart;
let cryptoData = [];
let stocksData = [];
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
    grid: {
        right: 140
    }
};
const ASSETS_URLS = {
    stock: '/stocks',
    stockUpdates: '/stocks/updates',
    crypto: '/cryptos',
    cryptoUpdates: '/cryptos/updates'
}

function initializeLineChart(elementId, title, initialSeriesData = []) {
    let chart = echarts.init(document.getElementById(elementId));
    let chartConfig = Object.assign({}, LINE_CHART_CONFIG);
    chartConfig['title'] = {
        text: title
    };
    chartConfig.series = initialSeriesData;
    chart.setOption(chartConfig);
    return chart;
}

function convertAssetsToChartSeries(assets, historyAttribute) {
    return assets.map(function (asset) {
        let seriesTemplate = getLineChartSeriesTemplate();
        asset[historyAttribute].reduce(function (updates, assetUpdate) {
            updates.push(toTimeSeriesDataFormat(asset['name'], assetUpdate['timestamp'], assetUpdate['value']));
            return updates;
        }, seriesTemplate.data);
        return seriesTemplate;
    });
}

function toTimeSeriesDataFormat(name, timestamp, value) {
    return {
        name: timestamp.toString(),
        value: [timestamp.toISOString(), value],
        assetName: name,
        assetValue: value
    };
}

function getLineChartSeriesTemplate() {
    return {
        type: 'line',
        showSymbol: false,
        endLabel: {
            show: true,
            formatter: function (params) {
                return params.data.assetName + ': $' + params.data.assetValue;
            }
        },
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
                    stockUpdate.value = stockUpdate.value.toFixed(2);
                })
            })
            stocksData = stocks;
            stockChart = initializeLineChart('stock-chart', 'Stock values', convertAssetsToChartSeries(stocksData, 'history'));
        },
        function (errorInfo) {
            console.log(errorInfo);
        });
}

function getCryptoData() {
    getRequest(ASSETS_URLS.crypto,
        function (cryptos) {
            cryptos.forEach(function (crypto) {
                crypto['history'].forEach(function (cryptoUpdate) {
                    cryptoUpdate.timestamp = new Date(cryptoUpdate.timestamp);
                    cryptoUpdate.value = cryptoUpdate.value.toFixed(2);
                })
            })
            cryptoData = cryptos;
            cryptoChart = initializeLineChart('crypto-chart', 'Crypto values', convertAssetsToChartSeries(cryptoData, 'history'));
            configTable();
        },
        function (errorInfo) {
            console.log(errorInfo);
        });
}

function insertTableRowData(tableId, values) {
    let htmlToInsert = '<tr>'
    values.forEach(function (cellValue) { htmlToInsert += '<td>' + cellValue + '</td>' });
    htmlToInsert += '</tr>'
    $('#' + tableId).append(htmlToInsert);
}

function transformAssetsHistoriesToRows(assets, historyAttribute) {
    let rows = [];
    let histories = assets.map(function (asset) { return asset[historyAttribute] });
    console.log(assets.toString());
    histories[0].forEach(function (assetUpdate, idx) {
        let timestamp = assetUpdate.timestamp;
        let value1, value2, value3, value4, value5, value6 = '';
        value1 = '$' + assetUpdate.value;
        value2 = histories[1].length > idx ? '$' + histories[1][idx].value : '';
        value3 = histories[2].length > idx ? '$' + histories[2][idx].value : '';
        value4 = histories[3].length > idx ? '$' + histories[3][idx].value : '';
        value5 = histories[4].length > idx ? '$' + histories[4][idx].value : '';
        value6 = histories[5].length > idx ? '$' + histories[5][idx].value : '';
        rows.push([formatDate(timestamp), value1, value2, value3, value4, value5, value6]);
    });
    return rows;
}

function formatDate(date) {
    let isEvening = date.getHours() / 12 > 1;
    let hours = isEvening ? date.getHours() % 12 : date.getHours();
    let ampm = isEvening ? 'pm' : 'am';
    return `${date.getDate()}/${date.getMonth()}/${date.getFullYear()} ${hours}:${date.getMinutes()}:${date.getSeconds()} ${ampm}`;
}

function configTable() {
    console.log(stocksData[0], cryptoData[0]);
    let rows = transformAssetsHistoriesToRows(stocksData.concat(cryptoData), 'history');
    rows.forEach(function (row) {
        insertTableRowData('assets-table', row);
    });
}

function runIfDataIsPresent(callback) {
    setTimeout(function () {
        if (stocksData.length > 1 && cryptoData > 1) {
            callback();
        } else {
            runIfDataIsPresent(callback);
        }
    }, 2000);
}

getStockData();
getCryptoData();
runIfDataIsPresent(configTable);
setInterval(function () {
    location.reload();
}, 1000 * 60 * 5);
