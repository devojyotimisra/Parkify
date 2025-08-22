const chartData = JSON.parse(document.getElementById("chart-data").dataset.chart);

const revenueCtx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenueCtx, {
    type: 'bar',
    data: {
        labels: chartData.revenue.labels,
        datasets: [{
            label: 'Revenue (₹)',
            data: chartData.revenue.data,
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
                    text: 'Revenue (₹)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Parking Lots'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Revenue from each parking lot'
            }
        }
    }
});

const occupancyCtx = document.getElementById('occupancyChart').getContext('2d');
const occupancyChart = new Chart(occupancyCtx, {
    type: 'bar',
    data: {
        labels: chartData.occupancy.labels,
        datasets: [
            {
                label: 'Available Spots',
                data: chartData.occupancy.available,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Occupied Spots',
                data: chartData.occupancy.occupied,
                backgroundColor: 'rgba(255, 99, 132, 0.7)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                stacked: true,
                title: {
                    display: true,
                    text: 'Number of Spots'
                }
            },
            x: {
                stacked: true,
                title: {
                    display: true,
                    text: 'Parking Lots'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Occupancy of overall parking lots'
            }
        }
    }
});