#include <ESP8266WiFi.h>
#include <GyverBME280.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

// Конфигурация сети
const char* ssid = "Ayur";
const char* password = "12082005";
// const char* serverUrl = "http://172.20.10.3:5000/api/data";
const char* serverUrl = "http://82.202.141.26:5100/api/data";

// Конфигурация датчика
const String sensorId = "eltex-2";
const float x = 50;  // координата x (% от ширины карты)
const float y = 50;  // координата y (% от высоты карты)
const unsigned long sendInterval = 5000;  // интервал отправки (мс)

// Экземпляры объектов
GyverBME280 bme;
WiFiClient wifiClient;
HTTPClient http;

void setup() {
  Serial.begin(115200);
  Serial.println("\nStarting Server Room Monitor");

  // Инициализация датчика
  if (!bme.begin()) {
    Serial.println("ERROR: BME280 not found!");
    while (true) delay(1000);
  }

  // Настройка параметров датчика
  bme.setStandbyTime(0);       // Без периода ожидания
  bme.setFilter(4);            // Максимальное сглаживание
  bme.setTempOversampling(2);  // Оптимальный режим
  
  Serial.println("BME280 initialized");
  
  // Подключение к Wi-Fi
  connectToWiFi();
}

void loop() {
  static unsigned long lastSend = 0;
  
  if (millis() - lastSend >= sendInterval) {
    lastSend = millis();
    
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("WARNING: WiFi disconnected, reconnecting...");
      connectToWiFi();
    }
    
    // Чтение данных с датчиков
    if (WiFi.status() == WL_CONNECTED) {
      float temperature = bme.readTemperature();
      float humidity = bme.readHumidity();
      
      if (!isnan(temperature) && !isnan(humidity)) sendSensorData(temperature, humidity);
      else Serial.println("ERROR: Invalid sensor readings");
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
  doc["temperature"] = round(temperature * 10) / 10.0;  // 1 decimal
  doc["humidity"] = round(humidity);
  doc["x"] = x;
  doc["y"] = y;
  
  String jsonStr;
  serializeJson(doc, jsonStr);
  
  Serial.println("Sending: " + jsonStr);
  
  // Отправка данных
  http.begin(wifiClient, serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonStr);
  
  if (httpCode > 0) {
    Serial.printf("HTTP status: %d\n", httpCode);
    if (httpCode == HTTP_CODE_OK) Serial.println("Response: " + http.getString());   
  } 
  else Serial.printf("HTTP error: %s\n", http.errorToString(httpCode).c_str());
  
  
  http.end();
}