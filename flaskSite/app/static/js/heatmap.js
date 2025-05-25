document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('heatmap');

    // Инициализация тепловой карты
    const heatmapInstance = h337.create({
      container: container,
      radius: 60,
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
    function updateHeatmap() {
      fetch('/api/data')
        .then(response => response.json())
        .then(data => {
          // Обновление тепловой карты
          const points = data.map(sensor => ({
            x: Math.floor(sensor.x * (container.offsetWidth / 100)),
            y: Math.floor(sensor.y * (container.offsetHeight / 100)),
            value: sensor.temperature,
            radius: 100
          }));
          
          heatmapInstance.setData({
            // min: 20,
            // max: 40,
            data: points
          });
  
          // Обновление показаний датчиков
          updateSensorReadings(data);
        });
    }
  
    // Обновление показаний датчиков
    function updateSensorReadings(data) {
      const latestReadings = {};
      data.forEach(sensor => {
        if (!latestReadings[sensor.sensor_id] || 
            new Date(sensor.timestamp) > new Date(latestReadings[sensor.sensor_id].timestamp)) {
          latestReadings[sensor.sensor_id] = sensor;
        }
      });
  
      // Обновление UI
      document.querySelector('.current-temp').textContent = 
        `${Math.max(...Object.values(latestReadings).map(s => s.temperature))}°C`;
      
      document.querySelector('#temp-indic').textContent =
        `${Math.max(...Object.values(latestReadings).map(s => s.temperature))}°C`;
      
      
      // Здесь можно добавить обновление меток конкретных датчиков
    }
  
    // Первоначальная загрузка и обновление каждые 5 секунд
    updateHeatmap();
    setInterval(updateHeatmap, 5000);
  });