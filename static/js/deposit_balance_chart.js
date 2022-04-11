$(function () {

    var $depositBalanceChart = $("#deposit_balance_chart");
    $.ajax({
        url: $depositBalanceChart.data("url"),
        success: function (data) {
            var ctx = $depositBalanceChart[0].getContext("2d");
            new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: data.data,
                        backgroundColor: [
                            '#FF7400', '#FF9E00', '#FFBE00', '#FFDD00', '#FFF400'
                        ],
                        label: 'Запасы месторождений'
                    }],
                    labels: data.labels
                },
                options: {
                    responsive: true
                },
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Population Bar Chart'
                }
            });

        }
    });

});