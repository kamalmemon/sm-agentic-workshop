// Star Wars color palette
const starwarsColors = {
    yellow: '#FFE81F',
    jedi: '#00BFFF',
    blue: '#0080FF',
    green: '#00FF00',
    red: '#FF0000',
    sith: '#8B0000',
    space: '#1a1a2e',
    steel: '#4a4a4a'
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
                borderColor: starwarsColors.jedi,
                backgroundColor: 'rgba(0, 191, 255, 0.1)',
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointBackgroundColor: starwarsColors.yellow,
                pointBorderColor: starwarsColors.jedi,
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 191, 255, 0.15)' },
                    ticks: { color: starwarsColors.jedi }
                },
                x: {
                    grid: { color: 'rgba(0, 191, 255, 0.1)' },
                    ticks: { color: starwarsColors.jedi }
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
                    starwarsColors.jedi,
                    starwarsColors.green,
                    starwarsColors.yellow,
                    starwarsColors.red,
                    starwarsColors.blue
                ],
                borderRadius: 4,
                borderWidth: 1,
                borderColor: 'rgba(255, 255, 255, 0.2)'
            }]
        },
        options: {
            responsive: true,
            indexAxis: 'y',
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    grid: { color: 'rgba(0, 191, 255, 0.15)' },
                    ticks: { color: starwarsColors.jedi }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: starwarsColors.yellow }
                }
            }
        }
    });
};
