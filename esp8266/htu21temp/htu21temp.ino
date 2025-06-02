#include <ESP8266WiFi.h>
#include <GyverHTU21D.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// Конфигурация сети
const char* ssid = "Ayur";
const char* password = "12082005";
const char* serverUrl = "http://172.20.10.3:5000/api/data";
// Адрес сервера
// 172.20.10.2

// Конфигурация датчика
const String sensorId = "eltex-1";
const float x = 50.0;  // координата x (% от ширины карты)
const float y = 50.0;  // координата y (% от высоты карты)

// Экземпляры объектов
GyverHTU21D htu;
WiFiClient client;
HTTPClient http;

void setup() {
  Serial.begin(115200);
  
  // Инициализация датчика
  if (!htu.begin()) {
    Serial.println("ERROR: HTU21D not found!");
    while (true) delay(1000);
  }
  Serial.println("HTU21D initializes");

  // Подключение к Wi-Fi
  connectToWiFi();
}

void loop() {
  if (htu.readTick(5000)) {
    if (WiFi.status() == WL_CONNECTED) {

      // Чтение данных с датчиков
      float temperature = htu.getTemperature();
      float humidity = htu.getHumidity();

      // Проверка и отправка данных
      if (!isnan(temperature) && !isnan(humidity)) sendSensorData(temperature, humidity);
      else Serial.print("ERROR: Invalid sensor readings");     
    } 
    else {
      Serial.println("WARNING: WiFi disconnected, reconnecting...");
      connectToWiFi();
    }
  }

  // Мягкая задержка для стабильности
  delay(100);
}

void connectToWiFi() {
  Serial.print("Connecting to ");
  Serial.print(ssid);

  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) Serial.println("\nConnected! IP: " + WiFi.localIP().toString());
  else Serial.println("\nERROR: WiFi connection failed"); 
}

void sendSensorData(float temperature, float humidity) {
  // Формирование JSON
  DynamicJsonDocument doc(256);
  doc["sensor_id"] = sensorId;
  doc["temperature"] = round(temperature * 10) / 10.0; // 1 знак после запятой
  doc["humidity"] = round(humidity);
  doc["x"] = x;
  doc["y"] = y;

  String jsonStr;
  serializeJson(doc, jsonStr);

  // Serial.print("Sending: ");
  Serial.println("Sending: " + jsonStr);

  // Отправка на сервер
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(jsonStr);

  if (httpCode > 0) {
    Serial.printf("HTTP status: %d\n", httpCode);
    if (httpCode == HTTP_CODE_OK) Serial.println("Response: " + http.getString());
  } 
  else Serial.printf("HTTP error: %d\n", http.errorToString(httpCode).c_str());

  http.end();
}