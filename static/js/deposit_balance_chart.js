$(function () {
    var $depositBalanceChart = $("#deposit_balance_chart");
    $.ajax({
        url: $depositBalanceChart.data("url"),
        success: function (data) {
            const ctx = $depositBalanceChart[0].getContext("2d");
            new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: data.data,
                        backgroundColor: [
                            '#FF7400', '#FF9E00', '#FFBE00', '#FFDD00', '#FFF400', '#FFFF40'
                        ],
                        label: 'Запасы месторождений у недропользователя'
                    }],
                    labels: data.labels
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: (window.screen.width > 1400) ? 'right' : 'bottom',
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
                            },
                        },
                    },
                },
            });
        }
    });
});