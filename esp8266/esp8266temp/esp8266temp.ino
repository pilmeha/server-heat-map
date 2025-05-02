#include <ESP8266WiFi.h>
#include <GyverHTU21D.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

// Настройки Wi-Fi
const char* ssid = "Ayur";
const char* password = "12082005";

// Адрес сервера
// 172.20.10.2
const char* serverUrl = "http://172.20.10.2:5000/api/data";

// Датчик HTU21D
GyverHTU21D htu;

// Уникальный ID и координаты датчика
const String sensorId = "3esp8266-htu21d";
const float x = 75.0;  // координата x (% от ширины карты)
const float y = 75.0;  // координата y (% от высоты карты)

void setup() {
  Serial.begin(115200);
  
  // Инициализация датчика
  if (!htu.begin()) {
    Serial.println("HTU21D not found!");
    while (true) delay(10);
  }
  Serial.println("HTU21D initializes");

  // Подключение к Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi! IP: " + WiFi.localIP().toString());
}

void loop() {
  if (htu.readTick(5000)) {
    if (WiFi.status() == WL_CONNECTED) {

      // Чтение данных с датчиков
      float temperature = htu.getTemperature();
      float humidity = htu.getHumidity();

      // Проверка и отправка данных
      if (!isnan(temperature) && !isnan(humidity)) {
        sendSensorData(temperature, humidity);
      } else {
        Serial.print("Sensor read error!");
      }
    } else {
      Serial.println("WiFi disconnected, reconnecting...");
      WiFi.reconnect();
    }
  }
}

void sendSensorData(float temperature, float humidity) {
  WiFiClient client;
  HTTPClient http;

  // Формирование JSON
  DynamicJsonDocument doc(256);
  doc["sensor_id"] = sensorId;
  doc["temperature"] = round(temperature * 10) / 10.0; // 1 знак после запятой
  doc["humidity"] = round(humidity);
  doc["x"] = x;
  doc["y"] = y;

  // Отправка на сервер
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");

  String jsonStr;
  serializeJson(doc, jsonStr);

  Serial.print("Sending to ");
  Serial.print(serverUrl);
  Serial.println(": " + jsonStr);

  int httpCode = http.POST(jsonStr);

  if (httpCode > 0) {
    Serial.printf("HTTP code: %d\n", httpCode);
    if (httpCode == HTTP_CODE_OK) {
      String payload = http.getString();
      Serial.println("Response: " + payload);
    }
  } else {
    Serial.printf("Ошибка HTTP: %d\n", httpCode);
  }

  http.end();
}