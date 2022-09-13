$(function () {
    var $depositBalanceChart = $("#deposit_balance_chart");
    $.ajax({
        url: $depositBalanceChart.data("url"),
        success: function (data) {
            var ctx = $depositBalanceChart[0].getContext("2d");
            var myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: data.data,
                        backgroundColor: [
                            '#FF7400', '#FF9E00', '#FFBE00', '#FFDD00', '#FFF400', '#FFFF40'
                        ],
                        label: 'Запасы месторождений у недропользователя'
                    }],
                    labels: data.labels,
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    onHover: (event, chartElement) => {
                        if(chartElement.length === 1) {
                            event.native.target.style.cursor = 'pointer';
                        };
                        if (chartElement.length === 0) {
                            event.native.target.style.cursor = 'default';
                        };
                    },
                    plugins: {
                        legend: {
                            onHover: handleHover,
                            onLeave: handleLeave,
                            position: (window.screen.width > 1400) ? 'right' : 'bottom',
                            // align: 'start',
                            ltr: true,
                            // position: 'top',
                            display: true,
                            labels: {
                                textAlign: 'left',
                                font: {
                                    size: (window.screen.width > 1400) ? 9 : 7
                                },
                                usePointStyle: true,
                                pointStyle: 'circle',
                                generateLabels: function (chart) {
                                    const data = chart.data;
                                    if (data.labels.length && data.datasets.length) {
                                        const {
                                            labels: {
                                                pointStyle
                                            }
                                        } = chart.legend.options;
                                        const max = data.datasets[0].data.reduce((a, b) => (a + b), 0);
                                        return data.labels.map((label, i) => {
                                            const meta = chart.getDatasetMeta(0);
                                            const style = meta.controller.getStyle(i);
                                            return {
                                                text: `${label} (${(data.datasets[0].data[i] * 100 / max).toFixed(2)}%)`,
                                                fillStyle: style.backgroundColor,
                                                strokeStyle: style.borderColor,
                                                lineWidth: style.borderWidth,
                                                pointStyle: pointStyle,
                                                hidden: !chart.getDataVisibility(i),
                                                index: i
                                            };
                                        });
                                    }
                                    return [];
                                }
                            },
                        },
                        tooltip: {
                            bodyFont: {
                                size: (window.screen.width > 1400) ? 12 : 7
                            },
                            usePointStyle: true,
                            callbacks: {
                                labelPointStyle: function (context) {
                                    return {
                                        pointStyle: 'circle',
                                        rotation: 0
                                    };
                                },
                                label: function (tooltipItems) {
                                    var label = myChart.data.labels[tooltipItems.dataIndex];
                                    var value = myChart.data.datasets[tooltipItems.datasetIndex].data[tooltipItems.dataIndex] + ' кг';
                                    return label + ': ' + value;
                                },
                            },
                        },
                    },
                },
            });
            function handleHover(evt, item, legend) {
                legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
                    colors[index] = index === item.index || color.length === 9 ? color : color + '4D';
                });
                legend.chart.update();
            };

            function handleLeave(evt, item, legend) {
                legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
                    colors[index] = color.length === 9 ? color.slice(0, -2) : color;
                });
                legend.chart.update();
            };
        },
    });
});
