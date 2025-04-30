document.addEventListener('DOMContentLoaded', () => {
    const heatmap = h337.create({
        container: document.getElementById("heatmap-container"),
        radius: 30,
        maxOpacity: 0.8
    });

    // Обновление данных каждые 3 секунды
    function updateHeatmap() {
        fetch("/api/data")
            .then(response => response.json())
            .then(data => {
                const points = data.map(item => ({
                    x: item.x * 8,  // Масштабирование под картинку
                    y: item.y * 8,
                    value: item.temperature * 10  // Усиление для визуализации
                }));
                heatmap.setData({ data: points });
            });
    }

    setInterval(updateHeatmap, 3000);
    updateHeatmap();
});
