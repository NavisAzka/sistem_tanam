// I2C Scanner untuk ESP32 (framework Arduino)
// Dipakai di Modul 3 Percobaan 2 untuk memastikan alamat OLED (0x3C)
// dan MPU6500 (0x68) terdeteksi pada bus I2C yang sama.
#include <Arduino.h>
#include <Wire.h>

#define SDA_PIN 21
#define SCL_PIN 22

void setup() {
    Serial.begin(115200);
    Wire.begin(SDA_PIN, SCL_PIN);
    delay(1000);

    Serial.println("I2C Scanner siap");
}

void loop() {
    int found = 0;

    Serial.println("Memindai alamat I2C...");

    for (uint8_t address = 1; address < 127; address++) {
        Wire.beginTransmission(address);

        if (Wire.endTransmission() == 0) {
            Serial.printf("Perangkat ditemukan di alamat 0x%02X\n", address);
            found++;
        }
    }

    if (found == 0) {
        Serial.println("Tidak ada perangkat I2C yang ditemukan. Periksa kabel SDA, SCL, VCC, dan GND.");
    } else {
        Serial.printf("Selesai: %d perangkat ditemukan\n", found);
    }

    Serial.println();
    delay(3000);
}
