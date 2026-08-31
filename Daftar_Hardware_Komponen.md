# DAFTAR HARDWARE & KOMPONEN

Daftar konsolidasi seluruh hardware/komponen yang dibutuhkan sepanjang **Modul 1–5** Praktikum Mikrokontroler & Embedded System. Kolom **Jumlah** menunjukkan kebutuhan puncak (jumlah maksimum yang dipakai bersamaan pada satu Percobaan) — sebagian besar komponen (board, breadboard, kabel, dst.) dipakai ulang lintas modul, bukan kebutuhan kumulatif per modul.

> **Catatan:** Untuk komponen tanpa produsen/model tunggal yang baku (mis. modul generik dari berbagai reseller), kolom **Link Datasheet** ditandai "—" agar tidak mengarahkan ke tautan yang belum tentu sesuai dengan varian produk yang dibeli. Selalu periksa datasheet dari produk spesifik yang benar-benar dipakai.

---

## Board & Programmer

| Nama Komponen | Jenis (Seri/Model/Manufaktur) | Jumlah | Dipakai di Modul | Digunakan untuk Apa di Modul Itu | Level Tegangan | Link Datasheet |
|---|---|---|---|---|---|---|
| Board ESP32 DevKit | ESP32 DevKit v1 (chip ESP32-WROOM-32, Espressif) | 2 (Modul 3 butuh 2 board sekaligus; modul lain cukup 1) | 1, 2, 3, 4, 5 | Modul 1: GPIO dasar, pull-up/down, debounce, ADC sederhana (framework Arduino & ESP-IDF); Modul 2: pembacaan sensor & kontrol aktuator; Modul 3: komunikasi UART/I2C/SPI/DMA (2 board untuk Percobaan board-to-board); Modul 4: external/timer interrupt, watchdog, FreeRTOS; Modul 5: filtering sinyal & kontrol PID | Logika 3.3V; input daya 5V via USB | https://www.espressif.com/en/products/socs/esp32 |
| Board STM32 Blackpill | STM32F401CCU6 / STM32F411CEU6 (STMicroelectronics) | 1 | 1 | Percobaan 1: pengenalan board STM32 & flashing program Blink via ST-Link (framework Arduino) | Logika 3.3V; input daya 5V via USB atau 3.3V langsung | https://www.st.com/en/microcontrollers-microprocessors/stm32f401cc.html |
| ST-Link V2 | Programmer/debugger SWD (STMicroelectronics, atau kloningan kompatibel) | 1 | 1 | Percobaan 1: programmer untuk mem-flash board STM32 Blackpill (STM32 tidak punya USB-to-serial bawaan) | USB 5V; jalur SWD (SWDIO/SWCLK) 3.3V | https://www.st.com/en/development-tools/st-link-v2.html |

## Perkakas & Bahan Umum

| Nama Komponen | Jenis (Seri/Model/Manufaktur) | Jumlah | Dipakai di Modul | Digunakan untuk Apa di Modul Itu | Level Tegangan | Link Datasheet |
|---|---|---|---|---|---|---|
| Breadboard | 830 titik | 1 | 1, 2, 3, 4, 5 | Prototyping seluruh rangkaian Percobaan tanpa solder | Pasif | — |
| Kabel jumper male-male | — | Secukupnya | 1, 2, 3, 4, 5 | Menghubungkan komponen antar titik breadboard/board | Pasif | — |
| Kabel jumper female-female | — | 4 | 1 | Menghubungkan pin ST-Link ke pin SWD Blackpill (Percobaan 1) | Pasif | — |
| Kabel jumper male-female | — | Secukupnya | 3 | Menghubungkan modul dengan pin header female (mis. OLED, IMU) ke breadboard/board | Pasif | — |
| Kabel USB Micro-USB/USB-C | sesuai port board | 2 | 1, 2, 3, 4, 5 | Menyambungkan board ke PC untuk upload program & Serial Monitor/Plotter | 5V | — |
| Laptop/PC | VSCode + PlatformIO terinstal | 1 | 1, 2, 3, 4, 5 | Menulis, meng-build, dan meng-upload kode program di seluruh Percobaan | — | — |

## Komponen Pasif & Indikator

| Nama Komponen | Jenis (Seri/Model/Manufaktur) | Jumlah | Dipakai di Modul | Digunakan untuk Apa di Modul Itu | Level Tegangan | Link Datasheet |
|---|---|---|---|---|---|---|
| LED 5mm + resistor 220Ω | — | 1 | 1, 2, 4 | Modul 1: indikator uji Blink ESP32 (jika tidak ada LED onboard); Modul 2: indikator kedipan mengikuti nilai potensiometer (Tugas Modul, Wokwi); Modul 4: indikator timer interrupt (Percobaan 3) & indikator tombol darurat (Percobaan 1) | Vf ≈ 2V, didorong dari GPIO 3.3V | — |
| Pushbutton (tactile) | — | 2 | 1, 4, 5 | Modul 1: pull-up/pull-down eksternal & internal (Percobaan 3), debouncing (Percobaan 4); Modul 4: tombol darurat manual recovery (Percobaan 1), latihan tambahan komunikasi antar task via queue (Percobaan 5); Modul 5: tombol naik/turun target RPM (Percobaan 5) | Logika 3.3V (tergantung konfigurasi pull-up/pull-down) | — |
| Resistor | 10kΩ | Secukupnya | 1 | Modul 1: resistor pull-up/pull-down eksternal pada tombol (Percobaan 3); pembagi tegangan untuk sensor resistif LDR (Percobaan 5) | Pasif | — |
| Resistor pull-up | 4.7kΩ | 2 | 3 | Stabilisasi jalur SDA/SCL bus I2C bila komunikasi tidak stabil (opsional, Percobaan 2) | Pasif | — |

## Sensor

| Nama Komponen | Jenis (Seri/Model/Manufaktur) | Jumlah | Dipakai di Modul | Digunakan untuk Apa di Modul Itu | Level Tegangan | Link Datasheet |
|---|---|---|---|---|---|---|
| LDR (Light Dependent Resistor) | mis. GL5528 | 1 | 1 | Percobaan 5: contoh sensor basis resistif — pembacaan intensitas cahaya via ADC | Pasif, dibaca via pembagi tegangan 0–3.3V | — |
| Modul joystick 2-axis | KY-023 (dual potensiometer + tombol SW) | 1 | 2 | Percobaan 1: contoh sensor basis resistif sebagai input kontrol (bukan sensor lingkungan) — VRx/VRy dibaca via ADC; Percobaan 3–6: input kontrol interaktif untuk mengendalikan motor DC, stepper, servo, dan BLDC | VCC 3.3–5V; output analog 0–VCC (dibaca via ADC ESP32, gunakan VCC 3.3V) | — |
| Modul touch sensor | TTP223 (Tontek) | 1 | 2 | Percobaan 1: contoh sensor basis kapasitif — deteksi sentuhan dengan output digital siap pakai | VCC 2.0–5.5V; output digital mengikuti level VCC | — |
| Hall effect sensor module | mis. A3144 / KY-003 | 1 | 2 | Percobaan 1: contoh sensor basis induktif — deteksi keberadaan/kekuatan medan magnet | **VCC minimal ±4.5V — gunakan 5V, bukan 3.3V**; output open-collector | — |
| Magnet kecil | — | 1 | 2 | Percobaan 1: objek uji untuk memicu pembacaan hall effect sensor | — | — |
| Sensor ultrasonik | HC-SR04 | 1 | 2 | Percobaan 2: contoh sensor basis akustik — pengukuran jarak via `pulseIn()`; juga dipakai pada Tugas Modul (Wokwi) sebagai indikator jarak otomatis | VCC 5V; **output Echo 5V — perlu pembagi tegangan sebelum masuk ESP32** | — |
| Sensor IR obstacle | Modul generik (umumnya IR pair + komparator LM393) | 1 | 2 | Percobaan 2: contoh sensor basis optik — deteksi halangan jarak dekat dengan output digital | VCC 3.3–5V; output digital | — |
| Modul OLED display | SH1106, 128×64, I2C (chip kompatibel SSD1306 juga umum ditemui — periksa chip aktual pada modul) | 1 | 3 | Percobaan 2 Bagian B: menampilkan data akselerometer MPU6050 sebagai contoh interfacing multi-device pada satu bus I2C | VCC 3.3–5V (modul umumnya sudah ada regulator onboard); I2C logika 3.3V | — |
| Modul IMU | MPU6050, breakout I2C | 1 | 3 | Percobaan 2 Bagian B: sensor akselerometer yang dibaca via register I2C manual (tanpa library), berbagi bus dengan OLED | VCC 3.3–5V (modul dengan regulator onboard); I2C logika mengikuti VCC | https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/ |
| Modul IMU | MPU6500, breakout SPI | 1 | 3 | Percobaan 4: pembacaan register SPI manual; Percobaan 5: pembacaan burst via SPI + DMA (dibandingkan dengan Percobaan 4) | VCC 3.3V (periksa toleransi modul); SPI logika 3.3V | https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6500/ |

## Aktuator & Driver

| Nama Komponen | Jenis (Seri/Model/Manufaktur) | Jumlah | Dipakai di Modul | Digunakan untuk Apa di Modul Itu | Level Tegangan | Link Datasheet |
|---|---|---|---|---|---|---|
| Motor DC + driver | Driver mis. L298N / L293D | 1 | 2, 5 | Modul 2 Percobaan 3: kontrol kecepatan (PWM) & arah putar motor DC, dikendalikan secara interaktif via joystick KY-023 (Percobaan 1); Modul 5: motor sebagai *plant* pada kontrol closed-loop on-off/P (Percobaan 4) dan PID lengkap (Percobaan 5) | Logika driver 5V; suplai motor sesuai motor (praktik umum 6–12V, maksimum driver hingga 46V untuk L298N) | https://www.st.com/en/motor-drivers/l298.html |
| Motor stepper | mis. 28BYJ-48 (4-fasa) atau NEMA17 (STEP/DIR) | 1 | 2 | Percobaan 4: kontrol pergerakan motor step-per-step dengan profil akselerasi, dikendalikan secara interaktif via joystick KY-023 (Percobaan 1) | Suplai motor via driver, umumnya 5V (28BYJ-48) atau 8–35V (NEMA17, tergantung driver & motor) | — |
| Driver motor stepper | ULN2003 (4-fasa) / A4988 / DRV8825 (STEP/DIR) | 1 | 2 | Percobaan 4: menerjemahkan sinyal dari ESP32 menjadi urutan arus ke lilitan motor stepper | Logika 3.3–5V; suplai motor 5V (ULN2003) / 8–35V (A4988) / 8.2–45V (DRV8825) | https://www.allegromicro.com/en/products/motor-drivers/brush-dc-motor-drivers/a4988 |
| Servo motor | SG90 (TowerPro atau kompatibel) | 1 | 2 | Percobaan 5: kontrol posisi sudut (0°–180°) via library ESP32Servo, dipetakan langsung dari posisi joystick KY-023 (Percobaan 1); juga dipakai pada Tugas Modul (Wokwi) sebagai indikator jarak | Suplai 4.8–6V; sinyal PWM kompatibel logika 3.3V/5V | — |
| ESC (Electronic Speed Controller) | ESC brushless RC hobby, 20–30A | 1 | 2 | Percobaan 6: menerjemahkan sinyal PWM (mikrodetik, dibangkitkan langsung via LEDC) dari ESP32 menjadi daya 3-fasa untuk motor brushless, termasuk proses arming dan kontrol throttle interaktif via joystick KY-023 (Percobaan 1) | Sinyal PWM 3.3–5V; daya utama dari baterai 2S–4S (7.4–16.8V, sesuai rating ESC) | — |
| Motor brushless (BLDC) | Motor brushless RC, mis. 2200KV | 1 | 2 | Percobaan 6: aktuator yang dikendalikan ESC untuk mendemonstrasikan kontrol kecepatan motor 3-fasa | Digerakkan via ESC 3-fasa, sesuai rating baterai 2S–3S | — |
| Baterai LiPo | 2S–3S | 1 | 2 | Percobaan 6: sumber daya utama untuk ESC dan motor brushless (terpisah dari power ESP32) | 7.4–11.1V nominal | — |
| Motor DC + encoder magnetik quadrature | Modul dengan konektor JST 6-pin, mis. JGB37-520 | 1 | 4, 5 | Modul 4 Percobaan 2: decoding sinyal quadrature encoder (pulsa & arah) via external interrupt; Modul 5: konversi pulsa ke RPM, filtering (alpha/Kalman), dan *plant* pada kontrol closed-loop/PID (seluruh Percobaan) | Motor umumnya 6–12V (varian umum 12V); encoder logika 3.3–5V | — |
| Catu daya eksternal | Sesuai kebutuhan motor DC/stepper | 1 | 2, 5 | Modul 2: sumber daya motor DC/stepper (Percobaan 3–4); Modul 5: sumber daya motor DC pada seluruh Percobaan kontrol closed-loop | Variabel, mengikuti spesifikasi motor — **jangan gunakan 5V dari USB langsung** | — |

---

## Catatan Tambahan

- **Level tegangan yang ditandai peringatan** (Hall effect sensor A3144/KY-003 dan Echo HC-SR04) memerlukan perhatian khusus — menyambungkan langsung ke pin 3.3V-only ESP32 tanpa penyesuaian dapat merusak GPIO.
- **Motor DC + encoder JGB37-520** dan komponennya (motor, driver, ESC, baterai) dipakai lintas modul (Modul 2, 4, 5) — disarankan menyiapkan set yang sama sejak Modul 2 agar tidak perlu membeli ulang.
- **OLED display**: cek chip aktual pada modul fisik yang dibeli sebelum praktikum (SH1106 vs SSD1306 memerlukan library Adafruit yang berbeda — lihat `Modul_3_Komunikasi_Serial.md` bagian C.2 dan D.4).
- Datasheet yang ditandai "—" bukan berarti tidak ada datasheet sama sekali, melainkan karena komponennya generik/multi-produsen sehingga tautan resmi tunggal tidak dapat dipastikan sesuai dengan produk yang benar-benar dibeli — cari datasheet dari toko/produsen spesifik produk yang digunakan.
