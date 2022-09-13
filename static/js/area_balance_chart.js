$(function () {
    var $areaBalanceChart = $("#area_balance_chart");
    $.ajax({
        url: $areaBalanceChart.data("url"),
        success: function (data) {
            var ctx = $areaBalanceChart[0].getContext("2d");
            var myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: data.data,
                        backgroundColor: [
                            "#25CCF7", "#FD7272", "#54a0ff", "#00d2d3",
                            "#1abc9c", "#2ecc71", "#3498db", "#9b59b6", "#34495e",
                            "#16a085", "#27ae60", "#2980b9", "#8e44ad", "#2c3e50",
                            "#f1c40f", "#e67e22", "#e74c3c", "#ecf0f1", "#95a5a6",
                            "#f39c12", "#d35400", "#c0392b", "#bdc3c7", "#7f8c8d",
                            "#55efc4", "#81ecec", "#74b9ff", "#a29bfe", "#dfe6e9",
                            "#00b894", "#00cec9", "#0984e3", "#6c5ce7", "#ffeaa7",
                            "#fab1a0", "#ff7675", "#fd79a8", "#fdcb6e", "#e17055",
                            "#d63031", "#feca57", "#5f27cd", "#54a0ff", "#01a3a4"
                        ],
                        label: 'Запасы месторождений по районам'
                    }],
                    labels: data.labels
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    onHover: (event, chartElement) => {
                        if (chartElement.length === 1) {
                            event.native.target.style.cursor = 'pointer';
                        }
                        ;
                        if (chartElement.length === 0) {
                            event.native.target.style.cursor = 'default';
                        }
                        ;
                    },
                    plugins: {
                        labels: {
                            // render: (context) => {
                            //     console.log(context.value)
                            //     return context.value
                            // },
                            // position: 'outside',
                            // textMargin: 6
                            render: 'none'
                        },
                        legend: {
                            onHover: handleHover,
                            onLeave: handleLeave,
                            position: (window.screen.width > 1400) ? 'right' : 'bottom',
                            // position: 'top',
                            display: true,
                            labels: {
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
                                                text: `${label} район (${(data.datasets[0].data[i] * 100 / max).toFixed(2)}%)`,
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
                                    var label = myChart.data.labels[tooltipItems.dataIndex] + ' район';
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
        }
    });
});