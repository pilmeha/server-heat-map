document.addEventListener('DOMContentLoaded', () => {
  function getColorByTemp(temp) {
    if (temp < 25) return '#3E63DD';   // холодный — синий
    if (temp < 30) return '#46C2DB';   // умеренный — голубой
    if (temp < 35) return '#fca311';   // тёплый — оранжевый
    return '#dd3e3e';                  // горячий — красный
  }

  // Функция обновления меток
  function updateLabels() {
    fetch('/api/data')
      .then(res => res.json())
      .then(data => {
        // Из оставшихся данных выбираем последнее значение по каждому sensor_id
        const latest = {};
        data.forEach(s => {
          // пример s.sensor_id = "eltex-1"
          if (!latest[s.sensor_id] || new Date(s.timestamp) > new Date(latest[s.sensor_id].timestamp)) {
            latest[s.sensor_id] = s;
          }
        });

        // Для каждого ключа latest обновляем span#temp-point-{n}
        Object.entries(latest).forEach(([sensorId, sensor]) => {
          const match = sensorId.match(/(\d+)/); // eltex-1 -> 1
          if (match) {
            const idx = match[1];
            const label = document.getElementById(`temp-point-${idx}`);
            const circle = document.querySelector(`.circle-${idx}`);
            if (label) {
              label.textContent = `${sensor.temperature.toFixed(1)}°C`;
            }
            if (circle) {
              circle.style.backgroundColor = getColorByTemp(sensor.temperature);
            }
          }
        });
      })
      .catch(err => console.error('Error fetching sensor data:', err));
  }

  // Запускем сразу и потом каждую N-ую секунду
  updateLabels();
  setInterval(updateLabels, 5000);
});

