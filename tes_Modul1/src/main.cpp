#include <Arduino.h>

#define JOY_VRX 34
#define JOY_VRY 35
#define JOY_SW  27
#define TOUCH_PIN 4  // OUT modul TTP223
#define HALL_PIN 26

void setup() {
  Serial.begin(115200);
  pinMode(JOY_SW, INPUT_PULLUP); // SW terhubung ke GND saat ditekan
  pinMode(TOUCH_PIN, INPUT);
  pinMode(HALL_PIN, INPUT);
}

void loop() {
  int vrx = analogRead(JOY_VRX);
  int vry = analogRead(JOY_VRY);
  bool pressed = (digitalRead(JOY_SW) == LOW); // aktif LOW (internal pull-up)

  bool touched = (digitalRead(TOUCH_PIN) == HIGH); // TTP223 umumnya aktif HIGH
  bool magnetDetected = (digitalRead(HALL_PIN) == LOW); // umumnya aktif LOW, cek datasheet modul

  Serial.printf("Joystick VRx: %d | VRy: %d | SW: %s | Touch (TTP223): %s | Hall Effect: %s\n",
                vrx, vry,
                pressed ? "DITEKAN" : "idle",
                touched ? "TERSENTUH" : "idle",
                magnetDetected ? "MAGNET TERDETEKSI" : "idle");
  delay(300);
}