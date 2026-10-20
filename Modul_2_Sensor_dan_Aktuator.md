# MODUL 2
# SENSOR BERDASARKAN BASIS PENGUKURAN & AKTUATOR MOTOR

**Mata Kuliah:** Praktikum Mikrokontroler & Embedded System
**Alokasi Waktu:** 6 x Percobaan (@ 100–150 menit)
**Platform:** ESP32 (Framework Arduino)
**IDE:** VSCode + PlatformIO

> **Catatan:** Modul ini melanjutkan penggunaan ESP32 dengan framework Arduino seperti pada Percobaan 3–5 Modul 1. Langkah instalasi VSCode, PlatformIO, dan driver USB-to-Serial tidak diulang di sini — lihat **[setup_vscode_platformio.md](setup_vscode_platformio.md)**.

---

## Daftar Isi
- [MODUL 2](#modul-2)
- [SENSOR BERDASARKAN BASIS PENGUKURAN \& AKTUATOR MOTOR](#sensor-berdasarkan-basis-pengukuran--aktuator-motor)
  - [Daftar Isi](#daftar-isi)
  - [A. Capaian Pembelajaran](#a-capaian-pembelajaran)
  - [B. Alat dan Bahan](#b-alat-dan-bahan)
  - [C. Dasar Teori](#c-dasar-teori)
    - [C.1 Sensor Resistif — Joystick 2-Axis sebagai Input Kontrol](#c1-sensor-resistif--joystick-2-axis-sebagai-input-kontrol)
    - [C.2 Sensor Kapasitif](#c2-sensor-kapasitif)
    - [C.3 Sensor Induktif](#c3-sensor-induktif)
    - [C.4 Sensor Basis Lain (Akustik \& Optik)](#c4-sensor-basis-lain-akustik--optik)
    - [C.5 PWM (Pulse Width Modulation) — Kontrol Kecepatan Motor DC](#c5-pwm-pulse-width-modulation--kontrol-kecepatan-motor-dc)
    - [C.6 Kontrol Posisi Motor Servo](#c6-kontrol-posisi-motor-servo)
    - [C.7 Motor Stepper](#c7-motor-stepper)
    - [C.8 ESC (Electronic Speed Controller) dan Motor Brushless](#c8-esc-electronic-speed-controller-dan-motor-brushless)
  - [D. Persiapan Sebelum Praktikum](#d-persiapan-sebelum-praktikum)
  - [E. Kegiatan Praktikum](#e-kegiatan-praktikum)
    - [PERCOBAAN 1 — Sensor Resistif, Kapasitif, dan Induktif](#percobaan-1--sensor-resistif-kapasitif-dan-induktif)
    - [PERCOBAAN 2 — Sensor Basis Lain (Ultrasonik \& IR Obstacle)](#percobaan-2--sensor-basis-lain-ultrasonik--ir-obstacle)
    - [PERCOBAAN 3 — Aktuator Motor DC](#percobaan-3--aktuator-motor-dc)
    - [PERCOBAAN 4 — Aktuator Motor Stepper](#percobaan-4--aktuator-motor-stepper)
    - [PERCOBAAN 5 — Aktuator Motor Servo](#percobaan-5--aktuator-motor-servo)
    - [PERCOBAAN 6 — Aktuator ESC \& Motor Brushless (BLDC) (Dikendalikan Joystick)](#percobaan-6--aktuator-esc--motor-brushless-bldc-dikendalikan-joystick)
  - [F. Tugas Modul](#f-tugas-modul)
  - [G. Referensi](#g-referensi)

---

## A. Capaian Pembelajaran

Setelah menyelesaikan Modul 2, praktikan mampu:
1. Menjelaskan prinsip kerja sensor berdasarkan basis transduksi (resistif — sebagai aplikasi kontrol interaktif melalui joystick 2-axis, kapasitif, induktif, dan basis lain) — melanjutkan basis resistif yang sudah diperkenalkan di Modul 1
2. Mengimplementasikan joystick 2-axis (KY-023) sebagai input kontrol interaktif untuk mengendalikan aktuator motor
3. Mengimplementasikan pembacaan sensor kapasitif dan induktif
4. Mengimplementasikan pembacaan sensor berbasis akustik (ultrasonik) dan optik (inframerah)
5. Mengimplementasikan kontrol kecepatan dan arah motor DC menggunakan sinyal PWM, dikendalikan secara interaktif melalui joystick
6. Mengimplementasikan kontrol motor stepper 4-fasa melalui driver ULN2003 untuk memutar motor sejauh sudut tertentu berdasarkan jumlah step
7. Mengimplementasikan kontrol posisi motor servo menggunakan sinyal PWM untuk menggerakkan servo bolak-balik antara dua sudut
8. Menjelaskan prinsip kerja ESC (Electronic Speed Controller) serta mengimplementasikan proses arming dan kontrol kecepatan motor brushless (BLDC) menggunakan sinyal PWM, dikendalikan secara interaktif melalui joystick

---

## B. Alat dan Bahan

| No | Nama Komponen | Spesifikasi | Jumlah |
|---|---|---|---|
| 1 | Board ESP32 DevKit | ESP32 DevKit v1 | 1 |
| 2 | Kabel USB Micro/USB-C | untuk ESP32 ke PC | 1 |
| 3 | Breadboard | 830 titik | 1 |
| 4 | Kabel jumper male-male | — | secukupnya |
| 5 | Modul joystick 2-axis KY-023 | Dual potensiometer (VRx/VRy) + tombol tekan (SW) | 1 |
| 6 | Modul touch sensor TTP223 | Capacitive touch sensor, output digital | 1 |
| 7 | Hall effect sensor module | mis. A3144/KY-003 | 1 |
| 8 | Magnet kecil | untuk uji hall effect | 1 |
| 9 | Sensor ultrasonik | HC-SR04 | 1 |
| 10 | Sensor IR obstacle | — | 1 |
| 11 | Motor DC + driver | Motor: JGA25-370 12V (1000RPM), kabel M1 (Merah, +) / M2 (Putih, −); Driver: L298N | 1 |
| 12 | Motor stepper | 28BYJ-48 (unipolar, 5V) — sesuai kode Percobaan 4 | 1 |
| 13 | Driver motor stepper | ULN2003 (modul driver 4-fasa bawaan 28BYJ-48) — sesuai kode Percobaan 4 | 1 |
| 14 | Servo motor | SG90 | 1 |
| 15 | Catu daya eksternal | 12V untuk motor DC dan sesuai kebutuhan stepper (jangan gunakan pin 3.3V ESP32 untuk menyuplai motor) | sesuai kebutuhan |
| 16 | ESC (Electronic Speed Controller) | ESC brushless 20A (RC hobby) | 1 |
| 17 | Motor brushless (BLDC) | Motor brushless RC 2200KV, **tanpa propeller/baling-baling terpasang** | 1 |
| 18 | Baterai LiPo | 2S–3S (7.4V–11.1V), sesuai spesifikasi ESC dan motor | 1 |
| 19 | Laptop/PC | VSCode + PlatformIO terinstal | 1 |

---

## C. Dasar Teori

### C.1 Sensor Resistif — Joystick 2-Axis sebagai Input Kontrol
**Modul 1 Percobaan 5** telah memperkenalkan sensor resistif melalui LDR — sebuah resistor variabel yang dibaca lewat rangkaian pembagi tegangan ke ADC. **Joystick 2-axis (mis. modul KY-023)** bekerja dengan basis transduksi yang **sama persis (resistif)**, namun memperluas penerapannya: di dalam modul terdapat **dua potensiometer** (masing-masing untuk sumbu X dan sumbu Y) yang porosnya digerakkan secara mekanis oleh gerakan stick, ditambah satu **tombol tekan (push button, SW)** yang aktif saat stick ditekan ke bawah.

Perbedaan mendasar dengan LDR terletak pada **peran** sensor tersebut dalam sistem: LDR di Modul 1 murni berfungsi sebagai sensor pasif (membaca besaran lingkungan berupa intensitas cahaya), sedangkan joystick di sini berfungsi sebagai **input kontrol interaktif (Human-Machine Interface/HMI)** — nilai ADC yang dihasilkan tidak merepresentasikan besaran fisik lingkungan, melainkan **perintah** yang diberikan pengguna secara langsung untuk mengendalikan aktuator (motor DC dan BLDC pada Percobaan 3 dan 6 modul ini).

Setiap sumbu joystick menghasilkan nilai ADC 12-bit (0–4095) dengan **titik tengah (netral)** di sekitar nilai 2048 saat stick tidak disentuh — nilai ini umumnya tidak presisi tepat 2048 karena toleransi komponen, sehingga diperlukan **dead zone** (rentang toleransi di sekitar titik tengah yang dianggap "netral") agar motor tidak bergerak sendiri akibat noise pembacaan ADC saat stick dalam posisi diam.

<img src="img/modul_joystick_ky023.png" alt="Gambar 1: Foto modul joystick 2-axis KY-023 (label pin VRx/VRy/SW/VCC/GND)" width="35%">

*Gambar 1: Foto modul joystick 2-axis KY-023 (label pin VRx/VRy/SW/VCC/GND)*

### C.2 Sensor Kapasitif
Sensor kapasitif mendeteksi besaran fisik (sentuhan, kelembapan, jarak dekat) melalui **perubahan nilai kapasitansi**. Pada praktikum ini digunakan modul **touch sensor TTP223** — modul berbasis IC TTP223 yang sudah mengintegrasikan rangkaian deteksi kapasitansi dan pembanding ambang batas (threshold) secara internal, sehingga cukup menghasilkan **output digital HIGH/LOW** siap pakai (umumnya aktif HIGH saat pad disentuh) tanpa perlu kalibrasi nilai analog secara manual — berbeda dengan fitur *touch* bawaan ESP32 (`touchRead()`) yang mengembalikan nilai mentah dan memerlukan penentuan threshold sendiri. Sensor kapasitif lain (mis. capacitive soil moisture, capacitive proximity) bekerja dengan prinsip serupa — mengukur perubahan kapasitansi pada elektroda sensor — namun umumnya berbentuk modul terpisah dengan output analog.

<img src="img/modul_touch_ttp223.png" alt="Gambar 2: Foto modul touch sensor TTP223 beserta label pin VCC/GND/OUT" width="45%">

*Gambar 2: Foto modul touch sensor TTP223 beserta label pin VCC/GND/OUT*

### C.3 Sensor Induktif
Sensor induktif mendeteksi objek logam atau perubahan medan magnet melalui **perubahan induktansi/medan magnet**. Pada praktikum ini digunakan **hall effect sensor**, yang mendeteksi keberadaan/kekuatan medan magnet secara langsung — umum digunakan untuk mendeteksi posisi magnet atau kecepatan putar (bersama magnet pada objek berputar). Contoh sensor induktif lain adalah *inductive proximity sensor*, yang menghasilkan medan elektromagnetik osilasi dan mendeteksi benda logam melalui redaman (eddy current) pada medan tersebut.

<img src="img/modul_hall_effect.png" alt="Gambar 3: Foto modul hall effect sensor (mis. A3144/KY-003) beserta magnet uji" width="40%">

*Gambar 3: Foto modul hall effect sensor (mis. A3144/KY-003) beserta magnet uji*

### C.4 Sensor Basis Lain (Akustik & Optik)
- **Ultrasonik (akustik):** mengukur jarak berdasarkan waktu tempuh gelombang suara (pulsa dipancarkan, dipantulkan objek, lalu diterima kembali); jarak dihitung dari selisih waktu dan kecepatan suara di udara
- **Inframerah/optik:** mendeteksi objek berdasarkan pantulan cahaya inframerah; umum digunakan sebagai sensor jarak dekat/obstacle dengan output digital

<img src="img/sensor_ultrasonik_ir.png" alt="Gambar 4: Foto modul sensor ultrasonik HC-SR04 (label pin Trig/Echo) berdampingan dengan modul sensor IR obstacle" width="65%">

*Gambar 4: Foto modul sensor ultrasonik HC-SR04 (label pin Trig/Echo) berdampingan dengan modul sensor IR obstacle*

### C.5 PWM (Pulse Width Modulation) — Kontrol Kecepatan Motor DC
PWM adalah teknik menghasilkan sinyal digital yang menyerupai sinyal analog dengan mengatur **duty cycle** (persentase waktu sinyal HIGH dalam satu periode). Semakin besar duty cycle, semakin besar "rata-rata" tegangan yang dirasakan oleh beban (mis. motor DC), sehingga kecepatan putarnya meningkat. Pada ESP32 framework Arduino, PWM diakses melalui API **LEDC** berbasis **channel**: `ledcSetup(channel, freq, resolution)` untuk mengonfigurasi sebuah channel PWM (frekuensi & resolusi), `ledcAttachPin(pin, channel)` untuk menghubungkan channel tersebut ke pin fisik, dan `ledcWrite(channel, duty)` untuk mengatur duty cycle-nya berdasarkan nomor channel (bukan nomor pin). Arah putar motor DC diatur secara terpisah melalui driver motor (mis. L298N) menggunakan dua pin digital (IN1/IN2).

> **Catatan versi:** Seluruh contoh kode pada modul ini (dan modul-modul lain dalam rangkaian praktikum) menggunakan **platform PlatformIO resmi `espressif32`** tanpa mengunci versi khusus, yang secara default membawa **Arduino-ESP32 core versi 2.0.x**. API LEDC berbasis channel (`ledcSetup`/`ledcAttachPin`) adalah API yang tersedia pada core versi ini. Core versi 3.x (dengan API LEDC berbasis pin seperti `ledcAttach()`) memerlukan platform komunitas terpisah (mis. fork *pioarduino*) dan **tidak dibahas** pada praktikum ini agar tetap konsisten dan kompatibel dengan library lain (mis. ESP32Servo) yang digunakan di modul-modul ini.

<img src="img/grafik_pwm_duty_cycle.png" alt="Gambar 5: Grafik sinyal PWM dengan beberapa nilai duty cycle berbeda (mis. 25%, 50%, 75%), menunjukkan hubungan duty cycle dengan tegangan rata-rata" width="60%">

*Gambar 5: Grafik sinyal PWM dengan beberapa nilai duty cycle berbeda (mis. 25%, 50%, 75%), menunjukkan hubungan duty cycle dengan tegangan rata-rata*

### C.6 Kontrol Posisi Motor Servo
Motor servo juga dikendalikan menggunakan sinyal PWM, namun dengan prinsip yang berbeda dari kontrol kecepatan motor DC — pada servo, **lebar pulsa (pulse width)** itu sendiri yang menentukan posisi sudut, bukan rata-rata duty cycle. Umumnya sinyal kontrol servo memiliki periode 20ms (frekuensi 50Hz), dengan lebar pulsa sekitar 1ms merepresentasikan sudut 0° dan 2ms merepresentasikan sudut 180°. Pada framework Arduino, detail ini diabstraksi oleh library seperti **ESP32Servo**, sehingga cukup memanggil fungsi `.write(angle)` untuk menggerakkan servo ke sudut tertentu.

<img src="img/diagram_pulsa_servo.png" alt="Gambar 6: Diagram lebar pulsa sinyal servo (1ms–2ms dalam periode 20ms) beserta sudut yang dihasilkan (0°–180°)" width="65%">

*Gambar 6: Diagram lebar pulsa sinyal servo (1ms–2ms dalam periode 20ms) beserta sudut yang dihasilkan (0°–180°)*

### C.7 Motor Stepper
Berbeda dengan motor DC yang berputar kontinu, motor stepper bergerak dalam **langkah-langkah diskret (step)** sesuai jumlah pulsa yang diberikan — misalnya 1.8° per step pada motor stepper standar (200 step per putaran penuh). Motor stepper dikendalikan melalui **driver motor stepper** (mis. A4988, DRV8825), yang menerima sinyal:
- **STEP:** setiap pulsa (transisi LOW→HIGH) menyebabkan motor berputar satu step
- **DIR:** menentukan arah putaran motor
- **EN (Enable):** mengaktifkan/menonaktifkan driver — saat dinonaktifkan, motor dapat diputar bebas secara manual
- **RESET/SLEEP:** beberapa driver memiliki pin ini untuk mereset atau menonaktifkan mode tidur driver, umumnya perlu ditarik HIGH agar driver aktif normal

<img src="img/wiring_motor_stepper.png" alt="Gambar 7: Contoh wiring motor stepper NEMA17 ke driver STEP/DIR (mis. A4988/DRV8825) dan mikrokontroler (board pada gambar ilustratif, prinsip pin STEP/DIR/EN sama pada ESP32)" width="70%">

*Gambar 7: Contoh wiring motor stepper NEMA17 ke driver STEP/DIR (mis. A4988/DRV8825) dan mikrokontroler — board pada gambar hanya ilustratif, prinsip pin STEP/DIR/EN berlaku sama saat dipasang ke ESP32*

### C.8 ESC (Electronic Speed Controller) dan Motor Brushless
Motor **brushless (BLDC — Brushless DC Motor)** tidak dapat dikendalikan langsung oleh driver H-bridge sederhana seperti motor DC biasa, karena memerlukan **komutasi elektronik** — pengaturan urutan pemberian arus ke tiga lilitan stator secara presisi agar rotor berputar. Tugas ini dilakukan oleh **ESC (Electronic Speed Controller)**, rangkaian elektronik yang menerima sinyal kontrol sederhana dari mikrokontroler dan menerjemahkannya menjadi pola komutasi 3-fasa untuk motor.

Sinyal kontrol ESC **identik dengan sinyal kontrol servo**: pulsa periodik 50Hz (periode 20ms), dengan lebar pulsa menentukan besar throttle — umumnya **1000µs merepresentasikan throttle minimum** (motor berhenti/idle) dan **2000µs merepresentasikan throttle maksimum**. Karena kesamaan format sinyal ini, ESC dapat dikendalikan menggunakan library yang sama dengan motor servo (mis. **ESP32Servo**), cukup menggunakan fungsi `writeMicroseconds()` untuk mengatur lebar pulsa secara langsung (dalam mikrodetik), alih-alih `write(angle)` yang bekerja dalam satuan derajat.

**Arming ESC:** hampir seluruh ESC mengharuskan proses **arming** sebelum dapat menjalankan motor — yaitu mengirim sinyal throttle minimum (1000µs) secara stabil selama beberapa detik setelah ESC dinyalakan. Ini adalah mekanisme keamanan: ESC akan menolak menjalankan motor pada throttle sembarang saat pertama kali menyala, untuk mencegah motor tiba-tiba berputar kencang akibat sinyal acak/tidak valid (mis. saat mikrokontroler baru boot). Banyak ESC memberikan bunyi *beep* khas sebagai indikasi proses arming berhasil.

**Catu daya:** ESC menerima daya utama untuk motor langsung dari baterai (umumnya **LiPo 2S–4S, 7.4V–14.8V**) melalui jalur terpisah dari jalur sinyal kontrol. Jalur sinyal tetap berada pada level logika rendah (3.3V/5V) yang aman bagi ESP32. **GND sinyal dan GND baterai harus disatukan (common ground)** agar referensi tegangan sinyal PWM konsisten dengan ESC.

> ⚠️ **Peringatan Keselamatan:** Motor brushless berputar sangat cepat dan bertenaga. **Selalu lepas propeller/baling-baling** sebelum menguji program, dan pastikan motor terpasang aman (tidak bisa terlempar) sebelum menyambungkan baterai. Jangan pernah menyentuh motor atau ESC saat baterai terhubung dan program sedang berjalan.

<img src="img/wiring_esc_brushless.png" alt="Gambar 8: Diagram wiring ESC ke ESP32 (sinyal PWM) dan ke baterai LiPo (daya utama), beserta motor brushless 3-fasa" width="60%">

*Gambar 8: Diagram wiring ESC ke ESP32 (sinyal PWM) dan ke baterai LiPo (daya utama), beserta motor brushless 3-fasa*

---

## D. Persiapan Sebelum Praktikum

Setiap percobaan menggunakan rangkaian tersendiri. Sebelum merakit percobaan berikutnya, matikan catu daya motor/ESC, lepaskan sambungan rangkaian percobaan sebelumnya dari breadboard dan GPIO, lalu pasang hanya komponen yang diperlukan pada percobaan aktif. Beberapa GPIO dipakai ulang oleh sensor dan driver yang berbeda.

1. Pastikan PlatformIO sudah terinstal (lihat **[setup_vscode_platformio.md](setup_vscode_platformio.md)**)
2. Buat project baru untuk Modul 2:
   - Name: `modul2-sensor-aktuator`
   - Board: **"Espressif ESP32 Dev Module"**
   - Framework: **Arduino**
3. Pastikan `platformio.ini` berisi:
   ```ini
   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   ```
4. Untuk Percobaan 5 (Motor Servo), tambahkan library **ESP32Servo** melalui PlatformIO Library Manager atau tambahkan pada `platformio.ini` (Percobaan 6/ESC tidak memerlukan library ini — lihat catatan pada Percobaan 6):
   ```ini
   lib_deps = madhephaestus/ESP32Servo@^3.0.0
   ```

---

## E. Kegiatan Praktikum

### PERCOBAAN 1 — Sensor Resistif, Kapasitif, dan Induktif

**Tujuan:**
Mahasiswa mampu memahami dan mengimplementasikan pembacaan sensor resistif melalui joystick 2-axis KY-023 (VRx, VRy, dan tombol SW), kapasitif (touch sensor TTP223), dan induktif (hall effect sensor).

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| Joystick KY-023 — VRx | GPIO 34 | Output analog sumbu X (ADC1) |
| Joystick KY-023 — VRy | GPIO 35 | Output analog sumbu Y (ADC1) |
| Joystick KY-023 — SW | GPIO 27 | Tombol tekan, aktif LOW (gunakan `INPUT_PULLUP`) |
| Joystick KY-023 — VCC/GND | 3.3V, GND | Sesuai datasheet modul |
| Modul TTP223 — OUT | GPIO 4 | Output digital, umumnya aktif HIGH saat pad disentuh |
| Modul TTP223 — VCC/GND | 3.3V, GND | Sesuai datasheet modul |
| Hall effect sensor module | GPIO 26 | Output digital |

> **Catatan:** Pin **GPIO 34, 35, 27** yang digunakan joystick pada Percobaan ini sengaja dipertahankan **konsisten** di Percobaan 3 dan 6 modul ini, karena joystick akan dipakai berulang sebagai input kontrol aktuator pada Percobaan-Percobaan tersebut.

<!-- <img src="img/wiring_joystick_touch.png" alt="Gambar 9: Diagram wiring joystick KY-023 dan modul touch TTP223 ke ESP32 (hall effect sensor tidak ditampilkan, rangkai sesuai tabel di atas)" width="60%"> -->

<!-- *Gambar 9: Diagram wiring joystick KY-023 dan modul touch TTP223 ke ESP32 (hall effect sensor tidak ditampilkan, rangkai sesuai tabel di atas)* -->

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang joystick KY-023: VCC, GND, VRx ke GPIO 34, VRy ke GPIO 35, SW ke GPIO 27
2. Pasang modul TTP223: VCC, GND, OUT ke GPIO 4
3. Pasang modul hall effect ke GPIO 26
4. Upload program gabungan, lalu lihat kelima nilai sensor di Serial Monitor
5. Coba tiap sensor: gerakkan dan tekan joystick, sentuh TTP223, dekatkan magnet ke sensor hall effect. Catat hasilnya
6. Biarkan joystick di posisi tengah, lalu catat nilai VRx dan VRy sebanyak 3 kali. Apakah selalu tepat 2048?
7. Analisis mengapa perlu memberi batas toleransi di sekitar tengah (dead zone), bukan hanya memeriksa apakah nilainya sama dengan 2048
8. Bandingkan cara kerja ketiga sensor. Analisis mengapa TTP223 dan hall effect langsung memberi nilai hidup atau mati (digital), sedangkan joystick memberi nilai yang berubah-ubah (analog)

**Kode Program (Joystick KY-023, TTP223, & Hall Effect):**
```cpp
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
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `analogRead(JOY_VRX)` / `analogRead(JOY_VRY)` | Membaca nilai ADC 12-bit (0–4095) dari masing-masing potensiometer sumbu X dan Y joystick — sama prinsipnya dengan pembacaan LDR di Modul 1, namun di sini nilainya diinterpretasikan sebagai **perintah kontrol**, bukan besaran lingkungan |
| `pinMode(JOY_SW, INPUT_PULLUP)` | Tombol SW pada joystick umumnya bertipe *active-low* (menghubungkan pin ke GND saat ditekan), sehingga memerlukan pull-up (internal atau eksternal) agar terbaca HIGH saat tidak ditekan |
| `digitalRead(TOUCH_PIN) == HIGH` | Modul TTP223 sudah mengeluarkan output digital siap pakai — tidak perlu `touchRead()` maupun threshold manual seperti fitur touch bawaan ESP32 |
| `digitalRead(HALL_PIN) == LOW` | Sebagian besar modul hall effect bersifat aktif LOW — perlu diverifikasi pada datasheet modul yang digunakan |

---

### PERCOBAAN 2 — Sensor Basis Lain (Ultrasonik & IR Obstacle)

**Tujuan:**
Mahasiswa mampu mengimplementasikan pembacaan sensor ultrasonik (basis akustik) dan sensor IR obstacle (basis optik).

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| HC-SR04 — Trig | GPIO 5 | Output dari ESP32 ke sensor |
| HC-SR04 — Echo | GPIO 18 | Input ke ESP32; gunakan pembagi tegangan bila level Echo 5V (contoh: 1kΩ seri dari Echo ke GPIO, 2kΩ dari GPIO ke GND) |
| Sensor IR obstacle | GPIO 19 | Output digital |

<img src="img/wiring_ultrasonik_ir.png" alt="Gambar 10: Diagram wiring sensor ultrasonik HC-SR04 dan sensor IR obstacle ke ESP32" width="60%">

*Gambar 10: Diagram wiring sensor ultrasonik HC-SR04 dan sensor IR obstacle ke ESP32*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang sensor HC-SR04, lalu tulis program pengukur jarak dengan `pulseIn()`
2. Pasang sensor IR obstacle, lalu uji apakah ada benda di depannya
3. Lihat hasil kedua sensor sekaligus di Serial Monitor, lalu coba berbagai jarak dan benda
4. Ukur 3 jarak dengan penggaris (misalnya 10, 30, dan 60 cm), bandingkan dengan angka di Serial Monitor, lalu catat selisihnya
5. Uji sensor IR pada jarak yang sama dengan beberapa permukaan (terang, gelap, halus, kasar)
6. Analisis mengapa sensor cahaya (IR) dipengaruhi warna dan tekstur permukaan, sedangkan sensor ultrasonik tidak

> **Catatan level tegangan:** Satukan GND HC-SR04 dan ESP32. Banyak modul HC-SR04 mengeluarkan Echo 5V. ESP32 yang tetap bekerja saat Echo dihubungkan langsung belum tentu rusak saat itu juga, tetapi level 5V berada di luar batas input GPIO ESP32 dan dapat merusak atau mengurangi keandalan pin. Gunakan pembagi tegangan seperti contoh pada tabel, kecuali datasheet modul yang digunakan memastikan Echo berlevel 3.3V. Batas maksimum input ESP32 klasik adalah 3.6V ([datasheet Espressif](https://documentation.espressif.com/esp32_datasheet_en.html)).

**Kode Program (Ultrasonik HC-SR04 & IR Obstacle):**
```cpp
#include <Arduino.h>

#define TRIG_PIN 5
#define ECHO_PIN 18
#define IR_PIN 19

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(IR_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
}

float readDistanceCM() {
  // Pastikan TRIG LOW
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Kirim pulsa 10 us
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Baca durasi pantulan
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // timeout 30 ms

  if (duration == 0)
    return -1.0; // tidak ada objek dalam jangkauan

  // Konversi ke cm
  return duration * 0.0343 / 2.0;
}

void loop() {
  float distance = readDistanceCM();
  bool obstacle = (digitalRead(IR_PIN) == LOW); // umumnya aktif LOW

  if (distance < 0) {
    Serial.print("Jarak: tidak ada objek");
  } else {
    Serial.printf("Jarak: %.1f cm", distance);
  }
  Serial.printf(" | IR Obstacle: %s\n", obstacle ? "TERDETEKSI" : "idle");
  delay(100);
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `pulseIn(ECHO_PIN, HIGH, 30000)` | Mengukur durasi (mikrodetik) pin ECHO berada pada kondisi HIGH, dengan batas timeout 30ms |
| `duration == 0` | Menandakan tidak ada pantulan yang diterima dalam batas timeout, sehingga dianggap tidak ada objek pada jangkauan sensor |
| `digitalRead(IR_PIN) == LOW` | Sebagian besar modul IR obstacle bersifat aktif LOW saat mendeteksi halangan |

---

### PERCOBAAN 3 — Aktuator Motor DC 

**Tujuan:**
Mahasiswa mampu mengimplementasikan kontrol kecepatan dan arah putar motor DC menggunakan sinyal PWM, dikendalikan secara interaktif melalui sumbu X joystick KY-023.

**Prinsip Kontrol:** Posisi joystick VRx (0–4095) dipetakan sebagai berikut — nilai di sekitar titik tengah (**dead zone**) berarti motor berhenti; deviasi ke satu sisi menggerakkan motor maju dengan kecepatan proporsional terhadap besar deviasi tersebut; deviasi ke sisi berlawanan menggerakkan motor mundur. Tombol **SW** berfungsi sebagai **stop darurat** — selama ditekan, motor dipaksa berhenti apa pun posisi joystick.

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| Joystick KY-023 — VRx | GPIO 34 | Kecepatan & arah (sama seperti Percobaan 1) |
| Joystick KY-023 — SW | GPIO 27 | Stop darurat, aktif LOW |
| Driver motor (ENA) | GPIO 25 | Sinyal PWM kecepatan |
| Driver motor (IN1) | GPIO 26 | Arah putar motor |
| Driver motor (IN2) | GPIO 33 | Arah putar motor |
| Motor DC — M1 (kabel Merah, +) | Driver OUT1 | Menukar M1/M2 membalik arah putar default motor |
| Motor DC — M2 (kabel Putih, −) | Driver OUT2 | — |

<img src="img/wiring_motor_dc_l298n.png" alt="Gambar 11: Contoh wiring motor DC via driver L298N dikendalikan joystick (nomor GPIO pada gambar ilustratif, ikuti tabel di atas untuk pin yang sesuai kode)" width="60%">

*Gambar 11: Contoh wiring motor DC via driver L298N dikendalikan joystick (nomor GPIO pada gambar ilustratif, ikuti tabel di atas untuk pin yang sesuai kode)*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang motor DC ke terminal OUT1 dan OUT2 pada L298N. Sambungkan terminal daya motor L298N (+12V) ke catu daya 12V, lalu satukan GND catu 12V, GND L298N, dan GND ESP32. Jangan sambungkan 12V ke pin ESP32. Lepas jumper ENA pada modul L298N supaya sinyal PWM dari GPIO 25 bisa mengatur kecepatan lewat pin ENA
2. Pasang joystick (VRx ke GPIO 34, SW ke GPIO 27), sama seperti Percobaan 1
3. Tulis program yang mengatur kecepatan (lewat ENA) dan arah putar (lewat IN1 dan IN2) sesuai posisi joystick
4. Gerakkan joystick ke kiri dan kanan, lalu lihat kecepatan dan arah putar motor berubah
5. Tekan SW sebagai tombol darurat. Motor harus langsung berhenti selama SW ditekan
6. Analisis mengapa arah (`IN1` dan `IN2`) harus diatur lebih dulu sebelum kecepatan (`ENA`). Apa yang terjadi jika urutannya dibalik?

**Kode Program (Kontrol Motor DC via Joystick):**
```cpp
#include <Arduino.h>

//==================== JOYSTICK ====================
#define JOY_VRX 34
#define JOY_SW  27

const int JOY_CENTER = 2048;
const int JOY_DEADZONE = 300; // toleransi di sekitar titik tengah

//==================== MOTOR ====================
#define ENA 25
#define IN1 26
#define IN2 33

const int pwmChannel = 0;
const int pwmFreq = 1000;
const int pwmResolution = 8;

//================================================

void motorForward(uint8_t speed) {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(pwmChannel, speed);
}

void motorBackward(uint8_t speed) {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  ledcWrite(pwmChannel, speed);
}

void motorStop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  ledcWrite(pwmChannel, 0);
}

//================================================

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(JOY_SW, INPUT_PULLUP);

  ledcSetup(pwmChannel, pwmFreq, pwmResolution); // konfigurasi channel PWM (core 2.x)
  ledcAttachPin(ENA, pwmChannel);                // hubungkan channel ke pin ENA

  Serial.println("--------------------------------");
  Serial.println("ESP32 Motor DC via Joystick");
  Serial.println("Geser VRx untuk maju/mundur, tekan SW untuk stop darurat");
  Serial.println("--------------------------------");

  motorStop();
}

//================================================

void loop() {
  bool emergencyStop = (digitalRead(JOY_SW) == LOW);

  if (emergencyStop) {
    motorStop();
    Serial.println("STOP DARURAT (SW ditekan)");
    delay(50);
    return;
  }

  int vrx = analogRead(JOY_VRX);
  int deviation = vrx - JOY_CENTER;

  if (abs(deviation) < JOY_DEADZONE) {
    motorStop();
    Serial.println("Motor: idle (joystick netral)");
  } else if (deviation > 0) {
    uint8_t speed = map(deviation, JOY_DEADZONE, JOY_CENTER, 0, 255);
    motorForward(speed);
    Serial.printf("Motor: MAJU, PWM = %d\n", speed);
  } else {
    uint8_t speed = map(-deviation, JOY_DEADZONE, JOY_CENTER, 0, 255);
    motorBackward(speed);
    Serial.printf("Motor: MUNDUR, PWM = %d\n", speed);
  }

  delay(100);
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `JOY_CENTER`, `JOY_DEADZONE` | Titik tengah nominal ADC (2048) dan rentang toleransi di sekitarnya — deviasi di bawah nilai ini dianggap joystick dalam posisi netral (motor berhenti) |
| `deviation = vrx - JOY_CENTER` | Selisih posisi VRx terhadap titik tengah — nilai positif berarti stick digeser ke satu sisi (maju), negatif ke sisi berlawanan (mundur) |
| `map(deviation, JOY_DEADZONE, JOY_CENTER, 0, 255)` | Memetakan besar deviasi (setelah dikurangi dead zone) menjadi nilai PWM 0–255, sehingga kecepatan motor proporsional terhadap seberapa jauh joystick digeser dari titik tengah |
| `digitalRead(JOY_SW) == LOW` diperiksa di awal `loop()` | Tombol SW berfungsi sebagai **stop darurat** dengan prioritas tertinggi — diperiksa sebelum logika kecepatan/arah, dan langsung `return` agar motor pasti berhenti selama tombol ditekan |

---

### PERCOBAAN 4 — Aktuator Motor Stepper 

**Tujuan:**
Mahasiswa mampu mengimplementasikan kontrol motor stepper 4-fasa melalui driver ULN2003, yaitu memutar motor sejauh sudut tertentu (90°) berdasarkan jumlah step, lalu berhenti sejenak secara berulang.

**Prinsip Kontrol:** Motor berputar sejauh **90°** (1024 step dari 4096 step per putaran penuh pada 28BYJ-48 dengan gearbox), berhenti **0,5 detik**, lalu mengulang pola yang sama terus-menerus. Jumlah step menentukan sudut putar, sedangkan jeda antar step (`STEP_DELAY_US`) menentukan kecepatan putar.

**Skema Rangkaian:**

| Komponen | Pin ESP32 / Sumber | Keterangan |
|---|---|---|
| Driver stepper — IN1 | GPIO 16 (RX2) | Fasa koil 1 |
| Driver stepper — IN2 | GPIO 17 (TX2) | Fasa koil 1 |
| Driver stepper — IN3 | GPIO 18 | Fasa koil 2 |
| Driver stepper — IN4 | GPIO 19 | Fasa koil 2 |
| Motor stepper 28BYJ-48 | Konektor driver ULN2003 | Colok langsung ke konektor pada driver |
| Driver stepper — daya | Catu daya eksternal | (+) ke VCC driver, (−) ke GND driver dan GND ESP32 |

> **Catatan:** Skema ini menggunakan driver stepper 4-fasa (mis. ULN2003 untuk motor stepper 28BYJ-48), sesuai kode program yang mengatur `stepSequence` 4-bit secara langsung — berbeda dari driver STEP/DIR (A4988/DRV8825) yang dibahas pada **C.7 Motor Stepper**. Jika menggunakan driver STEP/DIR, sesuaikan fungsi `setStep()`/`stopMotor()` menjadi pulsa pada pin STEP dan level pada pin DIR.

<img src="img/wiring_motor_stepper_percobaan4.png" alt="Gambar 12: Wiring motor stepper 28BYJ-48 via driver ULN2003 ke ESP32 (IN1–IN4 ke GPIO 16, 17, 18, 19) dengan catu daya eksternal" width="70%">

*Gambar 12: Wiring motor stepper 28BYJ-48 via driver ULN2003 ke ESP32 (IN1–IN4 ke GPIO 16, 17, 18, 19) dengan catu daya eksternal*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang motor stepper ke driver ULN2003, lalu hubungkan IN1 sampai IN4 ke ESP32 sesuai tabel. Pakai catu daya terpisah untuk driver
2. Tulis kode di bawah pada `src/main.cpp`, lalu klik **Build** dan **Upload**
3. Buka Serial Monitor. Pesan "Motor berputar 90 derajat" dan "Motor berhenti 0.5 detik" akan muncul bergantian
4. Lihat poros motor: berputar seperempat putaran (90°), diam sekitar setengah detik, lalu mengulang
5. Latihan: kecilkan `STEP_DELAY_US` bertahap (`2000`, lalu `1000`, `500`, `300`). Klik Build dan Upload tiap kali, lalu catat nilai terkecil yang masih membuat motor berputar lancar
6. Ubah `STEPS_PER_REVOLUTION` menjadi `2048`, klik Build dan Upload, lalu lihat sudut putarnya
7. Analisis mengapa motor bergetar atau melewatkan langkah jika `STEP_DELAY_US` terlalu kecil. Kaitkan dengan waktu yang dibutuhkan kumparan untuk berganti arus
8. Analisis hubungan jumlah langkah dengan sudut putar. Mengapa sudut putar di langkah 6 berubah padahal motornya sama?

**Kode Program (Kontrol Motor Stepper — Putar 90° dengan Jeda 0,5 Detik):**
```cpp
#include <Arduino.h>

//==================== STEPPER MOTOR ====================
#define IN1 16
#define IN2 17
#define IN3 18
#define IN4 19

const int motorPins[4] = {IN1, IN2, IN3, IN4};

const int stepSequence[8][4] = {
    {1, 0, 0, 0},
    {1, 1, 0, 0},
    {0, 1, 0, 0},
    {0, 1, 1, 0},
    {0, 0, 1, 0},
    {0, 0, 1, 1},
    {0, 0, 1, 0},
    {0, 0, 0, 1}
};

//==================== KONFIGURASI ====================
// Sesuaikan dengan spesifikasi motor stepper
const int STEPS_PER_REVOLUTION = 4096;  // Contoh: 28BYJ-48 dengan gearbox
const int STEPS_PER_90_DEG = STEPS_PER_REVOLUTION / 4;

const int STEP_DELAY_US = 2000;
const int STOP_DELAY_MS = 500;

//==================== MOTOR ====================
void setStep(int step) {
    for (int i = 0; i < 4; i++) {
        digitalWrite(motorPins[i], stepSequence[step][i]);
    }
}

void stopMotor() {
    for (int i = 0; i < 4; i++) {
        digitalWrite(motorPins[i], LOW);
    }
}

void rotate90Degrees() {
    for (int i = 0; i < STEPS_PER_90_DEG; i++) {
        setStep(i % 8);
        delayMicroseconds(STEP_DELAY_US);
    }

    stopMotor();
}

//==================== SETUP ====================
void setup() {
    Serial.begin(115200);

    for (int i = 0; i < 4; i++) {
        pinMode(motorPins[i], OUTPUT);
    }

    stopMotor();

    Serial.println("Stepper: 90 degree rotation");
    Serial.println("Stop duration: 500 ms");
}

//==================== LOOP ====================
void loop() {
    Serial.println("Motor berputar 90 derajat");

    rotate90Degrees();

    Serial.println("Motor berhenti 0.5 detik");
    delay(STOP_DELAY_MS);
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `stepSequence[8][4]` | Delapan pola pengaktifan 4 koil driver (IN1–IN4); setiap baris adalah satu step, dijalankan berurutan agar rotor tertarik medan magnet yang berpindah dari koil ke koil |
| `STEPS_PER_REVOLUTION` dan `STEPS_PER_90_DEG` | Jumlah step satu putaran penuh (4096 untuk contoh 28BYJ-48 dengan gearbox — sesuaikan dengan motor Anda) dan seperempatnya, yaitu jumlah step untuk memutar 90° (1024 step) |
| `STEP_DELAY_US` | Jeda antar step dalam mikrodetik — semakin kecil semakin cepat putarannya. Pada 2000 µs, 1024 step memerlukan sekitar 2 detik per putaran 90° |
| `setStep(i % 8)` | Memilih pola ke-`i mod 8` sehingga urutan 8 pola berulang terus selama `i` bertambah |
| `rotate90Degrees()` | Menjalankan `STEPS_PER_90_DEG` step berturut-turut dengan jeda `STEP_DELAY_US`, lalu memanggil `stopMotor()` |
| `stopMotor()` | Menetapkan seluruh pin IN menjadi `LOW` sehingga koil tidak dialiri arus — motor tidak menahan posisi, tetapi tidak panas dan hemat daya selama jeda |
| `delay(STOP_DELAY_MS)` di `loop()` | Menahan program 500 ms setelah motor berhenti, sebelum `loop()` mengulang putaran 90° berikutnya |


---

### PERCOBAAN 5 — Aktuator Motor Servo

**Tujuan:**
Mahasiswa mampu mengimplementasikan kontrol posisi sudut motor servo menggunakan sinyal PWM melalui library ESP32Servo, dengan menggerakkan servo bolak-balik antara dua sudut tertentu.

**Prinsip Kontrol:** Servo bergerak ke sudut **180°** (CW), ditunggu **400 ms** sebagai estimasi waktu geraknya, berhenti **0,5 detik**, lalu bergerak ke sudut **0°** (CCW) dengan pola waktu yang sama, dan seterusnya berulang. Program tidak mendapat umpan balik posisi dari servo, sehingga lama gerakan hanya diperkirakan lewat `MOVE_TIME_MS`.

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| Servo motor (sinyal) | GPIO 13 | Sinyal PWM servo (50Hz) |
| Servo motor (VCC) | Pin 5V ESP32 | Daya servo diambil dari pin 5V board (bukan 3.3V) |
| Servo motor (GND) | GND ESP32 | — |

<img src="img/wiring_servo.png" alt="Gambar 13: Wiring motor servo ke ESP32 (sinyal ke GPIO 13, daya servo dan GND ke pin 5V dan GND ESP32)" width="60%">

*Gambar 13: Wiring motor servo ke ESP32 (sinyal ke GPIO 13, daya servo dan GND ke pin 5V dan GND ESP32)*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps = madhephaestus/ESP32Servo@^3.0.0
```

**Langkah Kerja:**
1. Pasang servo: kabel sinyal ke GPIO 13, VCC ke pin 5V ESP32, GND ke GND ESP32. Jangan ambil daya servo dari pin 3.3V ESP32
2. Tulis kode di bawah pada `src/main.cpp`, lalu klik **Build** dan **Upload**
3. Buka Serial Monitor. Pesan "Servo bergerak CW ke 180 derajat" dan "Servo bergerak CCW ke 0 derajat" akan muncul bergantian
4. Lihat poros servo: bergerak ke 180°, diam sekitar setengah detik, lalu bergerak ke 0°, dan mengulang
5. Latihan: ubah `ANGLE_CW` menjadi `90` dan `ANGLE_CCW` menjadi `45`, klik Build dan Upload, lalu lihat sudut barunya
6. Latihan: kecilkan `MOVE_TIME_MS` menjadi `100`, klik Build dan Upload, lalu lihat apakah servo sempat sampai ke sudut tujuan sebelum perintah berikutnya
7. Analisis mengapa servo tidak butuh sensor putaran tambahan (encoder) seperti motor DC di Percobaan 3. Kaitkan dengan potensiometer di dalam servo yang memberi tahu posisinya
8. Analisis mengapa `MOVE_TIME_MS` hanya perkiraan, dan apa akibatnya jika nilainya terlalu kecil

**Kode Program (Kontrol Motor Servo — Gerak Bolak-balik 0° dan 180°):**
```cpp
#include <Arduino.h>
#include <ESP32Servo.h>

#define SERVO_PIN 13

Servo myServo;

const int ANGLE_CW = 180;
const int ANGLE_CCW = 0;

const int MOVE_TIME_MS = 400;  // Estimasi waktu gerak servo
const int STOP_DELAY_MS = 500; // Jeda setelah gerakan

void moveServo(int angle, const char* direction) {
    myServo.write(angle);

    Serial.printf("Servo bergerak %s ke %d derajat\n",
                  direction, angle);

    // Tunggu estimasi gerakan selesai
    delay(MOVE_TIME_MS);

    Serial.println("Gerakan selesai (estimasi)");
    Serial.println("Berhenti selama 0.5 detik");

    // Jeda dimulai setelah waktu gerak
    delay(STOP_DELAY_MS);
}

void setup() {
    Serial.begin(115200);

    myServo.setPeriodHertz(50);
    myServo.attach(SERVO_PIN, 500, 2400);

    myServo.write(ANGLE_CCW);
    delay(1000);

    Serial.println("MG90S Servo Control Started");
}

void loop() {
    moveServo(ANGLE_CW, "CW");
    moveServo(ANGLE_CCW, "CCW");
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `myServo.setPeriodHertz(50)` dan `myServo.attach(SERVO_PIN, 500, 2400)` | Mengatur sinyal PWM servo pada 50 Hz (periode 20 ms) dan menghubungkannya ke GPIO 13, dengan lebar pulsa 500–2400 µs yang dipetakan ke sudut 0°–180° |
| `myServo.write(angle)` | Memerintahkan servo menuju sudut tujuan; servo bergerak sendiri sampai posisi tercapai dan menahannya |
| `ANGLE_CW` dan `ANGLE_CCW` | Dua sudut tujuan yang dipakai bergantian (180° dan 0°) |
| `MOVE_TIME_MS` | Estimasi lama servo mencapai sudut tujuan. ESP32 tidak menerima umpan balik posisi, sehingga program hanya menunggu waktu yang dianggap cukup |
| `moveServo(angle, direction)` | Mengirim perintah sudut, mencetak pesan, menunggu `MOVE_TIME_MS`, lalu menunggu `STOP_DELAY_MS` sebagai jeda sebelum gerakan berikutnya |
| `myServo.write(ANGLE_CCW)` dan `delay(1000)` di `setup()` | Memposisikan servo ke 0° lebih dulu dan memberi waktu 1 detik agar posisi awal pasti sebelum `loop()` dimulai |

---

### PERCOBAAN 6 — Aktuator ESC & Motor Brushless (BLDC) (Dikendalikan Joystick)

**Tujuan:**
Mahasiswa mampu memahami prinsip kerja ESC sebagai pengendali motor brushless, serta mengimplementasikan proses arming dan kontrol kecepatan motor secara langsung melalui **LEDC** (tanpa library ESP32Servo), dikendalikan secara interaktif melalui sumbu X joystick KY-023.

**Prinsip Kontrol:** Setelah proses arming selesai, posisi joystick VRx dipetakan langsung menjadi throttle (1000–2000µs) — posisi paling kiri menghasilkan throttle minimum (motor idle/berhenti), semakin ke kanan semakin besar throttle. Tombol **SW** berfungsi sebagai **kill switch**: selama ditekan, throttle dipaksa ke nilai minimum (1000µs) terlepas dari posisi joystick — penting sebagai mekanisme keselamatan untuk motor bertenaga besar seperti BLDC.


**Skema Rangkaian:**

| Komponen | Pin ESP32 / Sumber | Keterangan |
|---|---|---|
| Joystick KY-023 — VRx | GPIO 34 | Besar throttle (setelah arming) |
| Joystick KY-023 — SW | GPIO 27 | Kill switch (paksa throttle minimum), aktif LOW |
| ESC — Sinyal (PWM) | GPIO 25 | Sinyal kontrol dari ESP32 ke ESC, via channel LEDC |
| ESC — GND (sinyal) | GND | Disatukan dengan GND ESP32 (**common ground** dengan baterai) |
| ESC — Power (input daya) | Baterai LiPo 2S–3S (7.4V–11.1V) | Jalur daya utama motor, **terpisah** dari power ESP32 |

<img src="img/wiring_esc_bldc.png" alt="Gambar 14: Contoh wiring ESC, motor brushless (BLDC), baterai LiPo, dan joystick ke ESP32 (nomor GPIO pada gambar ilustratif, ikuti tabel di atas untuk pin yang sesuai kode)" width="60%">

*Gambar 14: Contoh wiring ESC, motor brushless (BLDC), baterai LiPo, dan joystick ke ESP32 (nomor GPIO pada gambar ilustratif, ikuti tabel di atas untuk pin yang sesuai kode)*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

> **Catatan:** Percobaan ini **tidak memerlukan** library ESP32Servo — sinyal PWM 50Hz untuk ESC dibangkitkan langsung melalui API **LEDC** (`ledcSetup`/`ledcAttachPin`/`ledcWrite`), sebagai kontras dengan pendekatan Percobaan 5 (Servo) yang menggunakan abstraksi library. Keduanya menghasilkan sinyal yang identik (pulsa 1000–2000µs pada periode 20ms) — hanya berbeda pada tingkat abstraksi API yang dipakai.

**Langkah Kerja:**
1. Pastikan baling-baling (propeller) **sudah dilepas** dari motor brushless
2. Pasang ESC: kabel sinyal ke GPIO 25, GND ESC disatukan dengan GND ESP32, dan daya ESC dari sumber **terpisah** (bukan dari 5V ESP32)
3. Pasang joystick (VRx ke GPIO 34, SW ke GPIO 27), sama seperti Percobaan 1
4. Geser joystick sampai paling kiri, lalu klik **Build** dan **Upload**. Baterai ESC belum boleh disambungkan, ESP32 cukup memakai daya dari USB
5. Biarkan joystick tetap paling kiri dan tahan tombol SW. Saat Serial Monitor menampilkan "Sekarang nyalakan PSU ESC", segera sambungkan baterai LiPo. Kode menahan sinyal terendah selama 5 detik, jadi lakukan sebelum waktu itu habis. Tunggu bunyi *beep* dari ESC dan pesan "Arming selesai", dan tetap tahan SW sampai itu terjadi
6. Setelah arming berhasil, lepas SW. Geser joystick pelan dari kiri ke kanan dan lihat kecepatan motor naik
7. Tekan SW saat motor berputar sebagai tombol berhenti darurat. Analisis apakah motor berhenti dengan halus atau menyentak
8. Analisis mengapa proses arming penting bagi ESC, dan apa risikonya jika dilewati
9. Bandingkan cara di percobaan ini (mengatur sinyal PWM sendiri lewat `pulseToDuty()`) dengan cara memakai library ESP32Servo di Percobaan 5 (`attach()` dan `write()`). Diskusikan kelebihan dan kekurangannya

> **Mengapa urutan ini penting:** Jeda 5 detik pada kode dimulai saat ESP32 reboot, bukan saat baterai ESC dipasang. Jika baterai baru dipasang setelah jeda berakhir, loop mungkin sudah mengirim nilai throttle dari joystick; nilai paling kiri pun dapat sedikit lebih tinggi dari 1000µs karena toleransi ADC. ESC bisa menolak arming dan memberi bunyi peringatan, atau merespons throttle sesuai perilaku model ESC. Bila jeda terlewat sebelum baterai dipasang, lepaskan baterai ESC, reset ESP32, lalu ulangi urutan sambil menahan SW dan memastikan joystick di kiri. Tetap tanpa propeller selama pengujian.

**Kode Program (Arming ESC & Kontrol Kecepatan Motor Brushless via Joystick, berbasis LEDC):**
```cpp
#include <Arduino.h>

//==================== JOYSTICK ====================
#define JOY_VRX 34
#define JOY_SW  27

//==================== ESC ====================
#define ESC_PIN 25
#define ESC_CHANNEL 0

const uint32_t PWM_FREQ = 50;
const uint8_t PWM_RESOLUTION = 16;

const uint16_t THROTTLE_MIN = 1000; // us
const uint16_t THROTTLE_MAX = 2000; // us

uint32_t pulseToDuty(uint16_t pulseUs) {
  return ((uint32_t)pulseUs * 65535UL) / 20000UL;
}

void setThrottle(uint16_t pulseUs) {
  uint32_t duty = pulseToDuty(pulseUs);
  ledcWrite(ESC_CHANNEL, duty);
}

void setup() {
  Serial.begin(115200);
  pinMode(JOY_SW, INPUT_PULLUP);

  ledcSetup(ESC_CHANNEL, PWM_FREQ, PWM_RESOLUTION);
  ledcAttachPin(ESC_PIN, ESC_CHANNEL);

  Serial.println("=======================");
  Serial.println("BLDC VIA JOYSTICK");
  Serial.println("=======================");

  // Harus sudah aktif SEBELUM ESC dinyalakan
  setThrottle(THROTTLE_MIN);

  Serial.println("PWM minimum aktif.");
  Serial.println("Sekarang nyalakan PSU ESC.");

  // Beri ESC waktu untuk arming
  delay(5000);

  Serial.println("Arming selesai. Kontrol joystick aktif.");
}

void loop() {
  bool killSwitch = (digitalRead(JOY_SW) == LOW);

  uint16_t throttle;
  if (killSwitch) {
    throttle = THROTTLE_MIN;
  } else {
    int vrx = analogRead(JOY_VRX);
    throttle = map(vrx, 0, 4095, THROTTLE_MIN, THROTTLE_MAX);
  }

  setThrottle(throttle);
  Serial.printf("Throttle = %d us %s\n", throttle, killSwitch ? "(KILL SWITCH)" : "");

  delay(100);
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `pulseToDuty(pulseUs)` | Mengonversi lebar pulsa (mikrodetik) menjadi nilai duty cycle LEDC 16-bit (0–65535) relatif terhadap periode 20ms (`20000` mikrodetik) — rumus manual yang digantikan abstraksinya oleh `writeMicroseconds()` pada library ESP32Servo |
| `ledcSetup(ESC_CHANNEL, PWM_FREQ, PWM_RESOLUTION)` | Mengonfigurasi channel LEDC 0 dengan frekuensi 50Hz dan resolusi 16-bit — resolusi tinggi diperlukan agar pemetaan mikrodetik ke duty cycle cukup presisi |
| `setThrottle(THROTTLE_MIN)` diikuti `delay(5000)` | Proses **arming** — menahan sinyal throttle minimum selama 5 detik sebelum ESC menerima perintah throttle lain, sama seperti prinsip arming pada Percobaan sebelumnya |
| `map(vrx, 0, 4095, THROTTLE_MIN, THROTTLE_MAX)` | Memetakan posisi joystick langsung menjadi nilai throttle dalam mikrodetik, tanpa dead zone (seluruh rentang joystick digunakan sebagai skala throttle 0–100%) |
| `killSwitch` diperiksa sebelum `setThrottle()` | Tombol SW pada joystick berfungsi sebagai kill switch — memaksa throttle minimum kapan pun ditekan, mekanisme keselamatan penting untuk motor bertenaga besar |


---

## F. Tugas Modul


**Potensiometer Ganda Mengendalikan Servo & Stepper Terintegrasi:**

Buatlah simulasi di mana **dua potensiometer** mengendalikan servo dan motor stepper secara terintegrasi (rangkaian dan kode program bebas dirancang sendiri):
1. Potensiometer 1 menentukan **posisi sudut servo** (0°–180°, boleh kontinu atau dibatasi ke beberapa posisi diskrit sesuai pilihan Anda)
2. **Arah** motor stepper ditentukan oleh **posisi servo dari titik tengah (90°)** — Jika posisi servo berada pada sudut lebih dari 90°, maka motor stepper akan berputar searah jarum jam (CW). Jika posisi servo berada pada sudut kurang dari 90°, maka motor stepper akan berputar berlawanan arah jarum jam (CCW). Jika posisi servo sama dengan 90°, maka motor stepper berhenti total **(Terapkan mekanisme dead zone)**. 
3. Potensiometer 2 menentukan **kecepatan dasar** (base frequency) putaran stepper.

- kumpulkan tangkapan layar dari hasil simulasi beserta source code-nya. Simulasi dapat dilakukan pada website seperti Wokwi (rekomendasi) atau Cirkit.


**Pertanyaan Analisis:**
1. Analisis bagaimana rancangan Anda menggabungkan dua nilai (kecepatan dasar dari potensiometer 2, dan arah dair posisi servo) menjadi satu nilai kecepatan akhir stepper — apa fungsi *dead zone* di sekitar 90° pada rancangan ini?
2. Sinyal kontrol servo dan sinyal STEP pada driver stepper sama-sama berbasis PWM, namun diinterpretasikan berbeda oleh masing-masing aktuator — analisis apa yang direpresentasikan oleh sinyal PWM pada servo dibanding pada stepper.
3. Analisis mengapa pin EN (enable) pada driver stepper perlu dinonaktifkan (motor dibiarkan bebas berputar/*freewheel*) saat servo berada tepat di titik tengah, bukan hanya menghentikan pulsa STEP saja.

**Pengumpulan:** Sertakan project (folder PlatformIO beserta `diagram.json`, atau link project simulasi mode *share* dengan visibility public/unlisted bila dikerjakan lewat browser) beserta jawaban Pertanyaan Analisis pada laporan singkat.

---

## G. Referensi
1. Espressif Systems, *ESP32 Technical Reference Manual*
2. Espressif Systems, *ESP32 Arduino Core Documentation — Analog, Touch, LEDC*, https://docs.espressif.com/projects/arduino-esp32/
3. Datasheet Modul Joystick 2-Axis KY-023 (dual potensiometer + push button)
4. Datasheet HC-SR04 Ultrasonic Sensor
5. Datasheet Hall Effect Sensor Module (mis. A3144/KY-003)
6. Datasheet Driver Motor Stepper A4988/DRV8825 dan ULN2003
7. ESP32Servo Library Documentation, https://github.com/madhephaestus/ESP32Servo
8. PlatformIO Documentation, https://docs.platformio.org/
9. Oscar Liang, *How Does an ESC / BLDC Motor Work*, https://oscarliang.com/esc-firmware-protocol/ — referensi prinsip kerja ESC dan proses arming
