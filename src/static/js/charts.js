// Finnish-inspired color palette
const finnishColors = {
    blue: '#003580',
    lightBlue: '#4A90D9',
    ice: '#E8F4FC',
    forest: '#1B4D3E',
    aurora: '#5BC0BE',
    berry: '#8B1E3F',
    snow: '#F8FAFC'
};

window.createLineChart = function(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (ctx.chart) ctx.chart.destroy();

    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: finnishColors.blue,
                backgroundColor: 'rgba(0, 53, 128, 0.1)',
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointBackgroundColor: finnishColors.blue,
                pointBorderColor: finnishColors.snow,
                pointBorderWidth: 2,
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 53, 128, 0.1)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
};

window.createBarChart = function(canvasId, labels, data, label) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    if (ctx.chart) ctx.chart.destroy();

    ctx.chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: [
                    finnishColors.blue,
                    finnishColors.lightBlue,
                    finnishColors.forest,
                    finnishColors.aurora,
                    finnishColors.berry
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: 'rgba(0, 53, 128, 0.1)' } },
                y: { grid: { display: false } }
            }
        }
    });
};
