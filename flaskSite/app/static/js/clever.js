document.addEventListener('DOMContentLoaded', () => {
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
        Object.entries(latest).forEach(sensor => {
          const idx = sensor.sensor_id.split(/[-_]/)[1];
          const label = document.getElementById(`temp-point-${idx}`);
          const circle = document.querySelector(`.circle-${idx}`);
          const point = document.getElementById(`point-${sensor.sensor_id}`);
          if (label) label.textContent = `${sensor.temperature.toFixed(1)}°C`;
          if (circle) circle.style.backgroundColor = getColorByTemp(sensor.temperature);
          if (point && sensor.x != null && sensor.y != null) {
            point.style.left = `${sensor.x}%`;
            point.style.top = `${sensor.y}%`;
          }
        });
      })
      .catch(err => console.error('Error fetching sensor data:', err));

    // Вручную указываем координаты точек
    // document.getElementById("point-eltex-1").style.left = "50%";
    // document.getElementById("point-eltex-1").style.top = "10%";

    document.getElementById("point-eltex-2").style.left = "50%";
    document.getElementById("point-eltex-2").style.top = "50%";

    document.getElementById("point-eltex-3").style.left = "50%";
    document.getElementById("point-eltex-3").style.top = "50%";

    document.getElementById("point-eltex-4").style.left = "50%";
    document.getElementById("point-eltex-4").style.top = "50%";

  }

  function getColorByTemp(temp) {
    if (temp < 25) return '#3E63DD';   // холодный — синий
    if (temp < 30) return '#46C2DB';   // умеренный — голубой
    if (temp < 35) return '#fca311';   // тёплый — оранжевый
    return '#dd3e3e';                  // горячий — красный
  }

  // Запускем сразу и потом каждую 5-ую секунду
  updateLabels();
  setInterval(updateLabels, 5000);
});

