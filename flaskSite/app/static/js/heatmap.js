document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('heatmap-container');

    const heatmap = h337.create({
        container: container,
        radius: 30,
        maxOpacity: 0.8,
        gradient: {
            '0.4': 'blue',
            '0.6': 'cyan',
            '0.7': 'lime',
            '0.8': 'yellow',
            '1.0': 'red'
        }
    });

    // Функция обновления данных
    async function updateHeatmap() {
        try {
            const response = await fetch('/api/data');
            const data = await response.json();
            
            const points = data.map(item => ({
                x: Math.floor(item.x * (container.offsetWidth / 100)),
                y: Math.floor(item.y * (container.offsetHeight / 100)),
                value: item.temperature * 15,
                radius: 50
            }));
            
            heatmap.setData({
                data: points,
                min: -15,
                max: 65
            });
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // Обновление каждые 3 секунды
    updateHeatmap();
    setInterval(updateHeatmap, 3000);
});
