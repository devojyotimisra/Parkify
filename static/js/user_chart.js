const chartData = JSON.parse(document.getElementById("chart-data").dataset.chart);

const costCtx = document.getElementById('costChart').getContext('2d');
const costChart = new Chart(costCtx, {
    type: 'bar',
    data: {
        labels: chartData.dates,
        datasets: [{
            label: 'Cost (₹)',
            data: chartData.costs,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Cost (₹)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Date'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Your parking costs'
            }
        }
    }
});

const durationCtx = document.getElementById('durationChart').getContext('2d');
const durationChart = new Chart(durationCtx, {
    type: 'line',
    data: {
        labels: chartData.dates,
        datasets: [{
            label: 'Duration (hours)',
            data: chartData.durations,
            backgroundColor: 'rgba(75, 192, 192, 0.7)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false,
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: 'Duration (hours)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Date'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Your parking duration'
            }
        }
    }
});