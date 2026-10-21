# MODUL 5
# PEMROSESAN DATA SENSOR & DASAR SISTEM KONTROL (FILTERING & PID)

**Mata Kuliah:** Praktikum Mikrokontroler & Embedded System
**Alokasi Waktu:** 5 x Percobaan (@ 100–150 menit)
**Platform:** ESP32 (Framework Arduino)
**IDE:** VSCode + PlatformIO

> **Catatan:** Modul ini merupakan modul kapstone yang menggabungkan **Modul 2** (motor DC + PWM), **Modul 3** (MPU6500), dan **Modul 4 Percobaan 2** (quadrature encoder via external interrupt). Pastikan rangkaian motor+encoder+driver dan modul MPU6500 dari modul-modul tersebut sudah berfungsi sebelum memulai modul ini. Seluruh contoh kode menggunakan platform PlatformIO resmi `espressif32` (Arduino-ESP32 **core versi 2.0.x**), konsisten dengan Modul 2–4, termasuk API LEDC berbasis channel (`ledcSetup`/`ledcAttachPin`/`ledcWrite`) untuk kontrol PWM motor DC.
>
> Grafik sinyal contoh (quadrature encoder, filter alpha, filter Kalman, on-off vs P, respons PID) pada modul ini adalah **data simulasi/dummy**, bukan hasil pengukuran alat sungguhan — dibuat dengan skrip Python **[scripts/generate_modul5_signals.py](scripts/generate_modul5_signals.py)** (`matplotlib` + `numpy`) untuk memberi gambaran bentuk sinyal yang diharapkan di Serial Plotter. Bentuk sinyal asli hasil praktikum bisa berbeda.

---

## Daftar Isi
- [MODUL 5](#modul-5)
- [PEMROSESAN DATA SENSOR \& DASAR SISTEM KONTROL (FILTERING \& PID)](#pemrosesan-data-sensor--dasar-sistem-kontrol-filtering--pid)
  - [Daftar Isi](#daftar-isi)
  - [A. Capaian Pembelajaran](#a-capaian-pembelajaran)
  - [B. Alat dan Bahan](#b-alat-dan-bahan)
  - [C. Dasar Teori](#c-dasar-teori)
    - [C.1 Dari Pulsa Encoder ke RPM](#c1-dari-pulsa-encoder-ke-rpm)
    - [C.2 Filtering Sederhana — Low-Pass Filter Alpha](#c2-filtering-sederhana--low-pass-filter-alpha)
    - [C.3 Filtering Lanjut — Kalman Filter](#c3-filtering-lanjut--kalman-filter)
    - [C.4 Sistem Kontrol Closed-Loop](#c4-sistem-kontrol-closed-loop)
    - [C.5 Kontrol PID](#c5-kontrol-pid)
  - [D. Persiapan Sebelum Praktikum](#d-persiapan-sebelum-praktikum)
  - [E. Kegiatan Praktikum](#e-kegiatan-praktikum)
    - [PERCOBAAN 1 — Filtering Alpha pada MPU6500 (Akselerometer)](#percobaan-1--filtering-alpha-pada-mpu6500-akselerometer)
    - [PERCOBAAN 2 — Dari Pulsa ke RPM dengan Filtering Alpha](#percobaan-2--dari-pulsa-ke-rpm-dengan-filtering-alpha)
    - [PERCOBAAN 3 — Filtering dengan Kalman Filter](#percobaan-3--filtering-dengan-kalman-filter)
    - [PERCOBAAN 4 — Kontrol Closed-Loop: On-Off vs Proportional (P)](#percobaan-4--kontrol-closed-loop-on-off-vs-proportional-p)
    - [PERCOBAAN 5 — Kontrol PID Lengkap \& Tuning](#percobaan-5--kontrol-pid-lengkap--tuning)
  - [F. Tugas Modul](#f-tugas-modul)
  - [G. Referensi](#g-referensi)

---

## A. Capaian Pembelajaran

Setelah menyelesaikan Modul 5, praktikan mampu:
1. Mengonversi data pulsa mentah dari encoder menjadi kecepatan putar (RPM)
2. Menerapkan filtering sederhana (low-pass filter berbasis alpha) untuk mengurangi noise, baik pada sinyal sensor sederhana (akselerometer MPU6500) maupun sinyal RPM encoder
3. Menerapkan Kalman filter sebagai metode filtering alternatif, serta membandingkannya dengan filter alpha
4. Menjelaskan konsep sistem kontrol closed-loop, serta mengimplementasikan kontrol on-off dan Proportional (P)
5. Mengimplementasikan kontrol PID lengkap untuk mengatur kecepatan motor DC berdasarkan target RPM, serta melakukan tuning parameter

---

## B. Alat dan Bahan

| No | Nama Komponen | Spesifikasi | Jumlah |
|---|---|---|---|
| 1 | Board ESP32 DevKit | ESP32 DevKit v1 | 1 |
| 2 | Modul IMU MPU6500 | mode I2C (sama seperti Modul 3 Percobaan 2) | 1 |
| 3 | Motor DC + encoder magnetik quadrature | **JGA25-370 (1000RPM)**, konektor JST 6-pin (sama seperti Modul 4) | 1 |
| 4 | Driver motor | L298N (sama seperti Modul 2) | 1 |
| 5 | Catu daya eksternal | sesuai kebutuhan motor (jangan gunakan 5V dari USB langsung) | 1 |
| 6 | Pushbutton (tactile) | 2 buah — tombol naik/turun target RPM | 2 |
| 7 | Breadboard | 830 titik | 1 |
| 8 | Kabel jumper male-male | — | secukupnya |
| 9 | Laptop/PC | VSCode + PlatformIO terinstal, Serial Plotter | 1 |

---

## C. Dasar Teori

> **Ringkasan Istilah Penting pada Modul Ini:**
> | Istilah | Pengertian Singkat |
> |---|---|
> | **RPM** | *Revolutions Per Minute* — jumlah putaran penuh poros dalam satu menit |
> | **CPR** | *Counts Per Revolution* — jumlah pulsa encoder untuk satu kali putaran penuh |
> | **Noise** | Fluktuasi acak yang tidak diinginkan pada pembacaan sensor meskipun kondisi fisik sebenarnya stabil |
> | **Filter** | Algoritma pemrosesan sinyal untuk meredam *noise* sehingga nilai pembacaan menjadi lebih halus |
> | **Setpoint** | Nilai target yang ingin dicapai sistem kontrol (mis. target kecepatan 100 RPM) |
> | **Error** | Selisih antara nilai target (*setpoint*) dan nilai aktual yang terukur saat ini |
> | **Steady-state error** | Selisih yang tetap tersisa terhadap *setpoint* meskipun respons sistem sudah mencapai kondisi tunak (stabil) |
> | **PID** | Metode kontrol umpan balik yang menggabungkan aksi *Proportional*, *Integral*, dan *Derivative* menjadi satu sinyal koreksi |
> | **Tuning** | Proses penyesuaian parameter kontrol ($K_p$, $K_i$, $K_d$) untuk mendapatkan karakteristik respons sistem yang optimal |
> | **Overshoot** | Lonjakan respons yang melampaui nilai *setpoint* sesaat sebelum akhirnya melandai menuju kondisi stabil |

### C.1 Dari Pulsa Encoder ke RPM
Setiap kali poros encoder berputar, sejumlah pulsa listrik dihasilkan — semakin cepat putarannya, semakin banyak pulsa yang terhitung dalam satu satuan waktu. Dari jumlah pulsa inilah kecepatan putar (**RPM** — *Revolutions Per Minute*) dapat dihitung.

Untuk motor ber-*gearbox* (seperti JGA25-370 yang digunakan pada modul ini), jumlah pulsa untuk satu putaran penuh pada **poros output** (poros akhir setelah *gearbox*, tempat beban/roda dipasang) merupakan hasil kali antara resolusi encoder mentah (**CPR** — *Counts Per Revolution*) dan rasio reduksi *gearbox*:

```
CPR_TOTAL = CPR_encoder × Rasio_Gearbox
```

Nilai RPM kemudian dihitung dari pertambahan jumlah pulsa ($\Delta\text{Count}$) selama selang waktu pencuplikan ($\Delta t$ dalam detik):

```
RPM = (deltaCount / deltaTime) × (60 / CPR_TOTAL)
```

Spesifikasi CPR dan rasio *gearbox* pada lembar data umum sering kali memiliki toleransi — cara paling presisi adalah melakukan **kalibrasi langsung** (memutar poros output sejumlah putaran penuh yang diketahui, lalu mencatat total pulsa yang terhitung). Pada modul ini, konstanta `PULSES_PER_REV` cukup menggunakan **nilai estimasi dari spesifikasi motor** (untuk JGA25-370 1000RPM: $\approx 102$ pulsa/putaran, lihat Percobaan 2) yang sudah memadai untuk eksperimen sistem kontrol.

<img src="img/anim_quadrature_direction.gif" alt="Gambar 1: Animasi sinyal quadrature encoder Channel A dan Channel B, menunjukkan bagaimana urutan fasa antar kedua channel menentukan arah putaran (maju vs mundur)" width="70%">

*Gambar 1: Animasi sinyal quadrature encoder Channel A dan Channel B — perhatikan urutan fasa antar kedua channel berbalik saat arah putaran berbalik (Channel A mendahului B saat maju/CW, Channel B mendahului A saat mundur/CCW)*

### C.2 Filtering Sederhana — Low-Pass Filter Alpha
Nilai RPM mentah (`rawRPM`) yang dihitung langsung dari pencacahan pulsa diskret umumnya mengandung **noise** — nilainya berfluktuasi tajam antar periode pencuplikan, terutama pada kecepatan rendah. Metode paling sederhana untuk menghaluskan sinyal tersebut adalah **Low-Pass Filter berbasis Alpha** (*Exponential Moving Average*), dengan persamaan rekursif:

```
filtered_baru = α × filtered_lama + (1 - α) × raw_baru
```

Koefisien `α` (*alpha*) bernilai antara `0` hingga `1` dan menentukan bobot nilai terfilter sebelumnya terhadap pembacaan baru. Semakin besar nilai `α` (mendekati `1`), sinyal keluaran semakin halus, namun memiliki tundaan fasa (*lag*) yang lebih besar sehingga lebih lambat merespons perubahan kecepatan yang sesungguhnya. Filter ini sangat ringan secara komputasi dan hanya memerlukan satu parameter (`α`), namun bobotnya bersifat tetap sehingga tidak dapat beradaptasi secara dinamis saat karakteristik *noise* berubah.

<img src="img/grafik_filter_alpha.png" alt="Gambar 2: Grafik perbandingan sinyal RPM mentah (noisy) vs hasil filter alpha pada beberapa nilai α berbeda, menunjukkan trade-off kehalusan vs lag" width="60%">

*Gambar 2: Grafik perbandingan sinyal RPM mentah (noisy) vs hasil filter alpha pada beberapa nilai α berbeda, menunjukkan trade-off kehalusan vs lag*

### C.3 Filtering Lanjut — Kalman Filter
**Kalman Filter** mengestimasi keadaan (*state*) suatu sistem dengan menggabungkan dua sumber informasi secara optimal: **prediksi berbasis estimasi sebelumnya** dan **pengukuran baru dari sensor**, dengan memberikan bobot lebih besar pada sumber yang memiliki ketidakpastian lebih kecil.

Berbeda dari filter alpha yang menggunakan faktor pembobotan tetap (`α`), Kalman filter menghitung ulang bobot optimalnya — disebut **Kalman Gain (`K`)** — pada setiap siklus pencuplikan berdasarkan dua parameter kovariansi *noise*:
- **Q (*Process Noise Covariance*):** merepresentasikan seberapa cepat nilai fisik sebenarnya diperkirakan berubah — nilai `Q` yang lebih besar membuat filter lebih responsif mengikuti perubahan cepat.
- **R (*Measurement Noise Covariance*):** merepresentasikan tingkat *noise* atau ketidakpastian sensor — nilai `R` yang lebih besar membuat filter lebih meredam fluktuasi pengukuran sensor.

Untuk sistem 1 dimensi (1D), algoritma Kalman filter bekerja melalui dua tahap pada setiap siklus — **Predict** (memperbarui estimasi ketidakpastian seiring waktu) dan **Update** (mengoreksi estimasi menggunakan data pengukuran terbaru):
```
// Predict
P = P + Q

// Update
K = P / (P + R)
X = X + K × (measurement - X)
P = (1 - K) × P
```
Di sini `X` adalah nilai estimasi terbaik saat ini, dan `P` adalah kovariansi error estimasi (semakin kecil `P`, semakin tinggi tingkat kepercayaan terhadap estimasi `X`). Karena `K` diperbarui setiap siklus, Kalman filter mampu menyeimbangkan peredaman *noise* dan kecepatan respons secara adaptif.

<img src="img/diagram_kalman_filter.png" alt="Gambar 3: Diagram blok siklus predict-update Kalman filter, beserta grafik perbandingan hasil Kalman filter vs filter alpha pada sinyal RPM yang sama" width="85%">

*Gambar 3: Diagram blok siklus predict-update Kalman filter, beserta grafik perbandingan hasil Kalman filter vs filter alpha pada sinyal RPM yang sama*

### C.4 Sistem Kontrol Closed-Loop
Sistem kontrol **loop tertutup (*closed-loop*)** bekerja dengan membaca kondisi aktual sistem secara kontinu melalui sensor (**feedback**), membandingkannya dengan nilai target yang diinginkan (**setpoint**), lalu menghitung nilai koreksi untuk aktuator berdasarkan selisih keduanya (**error**):

```
error = setpoint - nilai_terukur
```

Dua metode kontrol *closed-loop* paling dasar adalah:
- **Kontrol On-Off (Bang-Bang Control):** Aktuator diaktifkan penuh (PWM = 255) ketika nilai aktual berada di bawah *setpoint* (`error > 0`), dan dimatikan sepenuhnya (PWM = 0) ketika nilai aktual mencapai atau melampaui *setpoint*. Meskipun sangat sederhana, metode ini menyebabkan kecepatan motor berosilasi terus-menerus di sekitar *setpoint*.
- **Kontrol Proportional (P):** Besarnya sinyal kendali sebanding lurus dengan nilai *error* saat itu (`output = Kp × error`) — semakin jauh kecepatan motor dari target, semakin besar daya PWM yang diberikan. Kontrol P menghasilkan respons yang jauh lebih stabil dibanding *on-off*, namun umumnya menyisakan selisih tetap saat tunak (**steady-state error**) karena ketika *error* mengecil, nilai `Kp × error` tidak lagi cukup besar untuk mengimbangi beban/gesekan motor.

<img src="img/diagram_closed_loop.png" alt="Gambar 4: Diagram blok sistem kontrol closed-loop (setpoint → kontroler → aktuator → plant → sensor → feedback ke pembanding), beserta grafik respons on-off (osilasi) vs P (steady-state error)" width="85%">

*Gambar 4: Diagram blok sistem kontrol closed-loop (setpoint → kontroler → aktuator → plant → sensor → feedback ke pembanding), beserta grafik respons on-off (osilasi) vs P (steady-state error)*

### C.5 Kontrol PID
Kontroler **PID (*Proportional–Integral–Derivative*)** menyempurnakan kontrol Proportional dengan menambahkan dua suku koreksi tambahan:
- **Integral (I):** Mengakumulasikan *error* terhadap waktu (`integralError += error × dt`). Selama masih terdapat selisih terhadap *setpoint*, suku Integral akan terus membesar hingga mampu mengeliminasi **steady-state error** yang tidak dapat diatasi oleh kontrol P saja.
- **Derivative (D):** Menghitung laju perubahan *error* (`derivativeError = (error - previousError) / dt`). Suku ini memberikan efek pengereman (*damping*) ketika nilai aktual mendekati *setpoint* dengan cepat, sehingga meredam **overshoot** dan mempercepat waktu tunak (*settling time*).

Ketiga komponen tersebut dijumlahkan menjadi satu sinyal kendali diskret pada setiap interval pencuplikan $\Delta t$:

```
output = (Kp × error) + (Ki × integralError) + (Kd × derivativeError)
```

Tiga aspek praktis yang perlu diperhatikan saat mengimplementasikan PID pada mikrokontroler:
- **Anti-windup (Integral Clamping):** Akumulasi `integralError` dapat tumbuh terlalu besar (*integral windup*) apabila aktuator mengalami saturasi atau terhambat dalam waktu lama. Oleh karena itu, nilai `integralError` wajib dibatasi (*clamped*) pada rentang tertentu.
- **Kompensasi Deadzone Motor (PWM Minimum):** Motor DC memerlukan ambang tegangan minimum tertentu (`PWM_MIN_RUN`) untuk mengatasi gesekan statis awal. Jika keluaran PID bernilai positif kecil tetapi di bawah ambang tersebut, nilainya perlu diangkat ke `PWM_MIN_RUN` agar poros motor dapat mulai berputar.
- **Tuning Parameter:** Penentuan kombinasi $K_p$, $K_i$, dan $K_d$ dilakukan secara bertahap dengan mengamati kurva respons terhadap perubahan *setpoint* (atau menggunakan metode formal seperti *Ziegler-Nichols* di luar cakupan modul ini).

<img src="img/diagram_blok_pid.png" alt="Gambar 5: Diagram blok kontroler PID (jalur Proportional, Integral, Derivative dijumlahkan menjadi output), beserta grafik respons sistem sebelum dan sesudah tuning" width="85%">

*Gambar 5: Diagram blok kontroler PID (jalur Proportional, Integral, Derivative dijumlahkan menjadi output), beserta grafik respons sistem sebelum dan sesudah tuning*

---

## D. Persiapan Sebelum Praktikum

1. Pastikan PlatformIO sudah terinstal (lihat **[setup_vscode_platformio.md](setup_vscode_platformio.md)**)
2. Instal ekstensi **Serial Plotter** pada VSCode — dibutuhkan untuk memvisualisasikan data pada seluruh Percobaan modul ini, karena VSCode (berbeda dari Arduino IDE) tidak memiliki Serial Plotter bawaan:
   - Buka **Extensions** pada VSCode (`Ctrl+Shift+X`), cari **"Serial Plotter"** (oleh badlogic), klik **Install**
   - Repository resmi: https://github.com/badlogic/serial-plotter
   - Setelah terinstal, buka melalui **Command Palette** (`Ctrl+Shift+P`) → ketik **"Serial Plotter: Open pane"**
   - Pada panel yang terbuka: pilih **port** serial ESP32 dan **baud rate** (115200, sesuai `Serial.begin()` pada kode), lalu klik **Start**
   - Ekstensi ini membaca format baris `>nama_variabel:nilai,nama_variabel2:nilai2` — persis format yang digunakan pada seluruh contoh kode `Serial.print()` di modul ini
   - **Penting:** port serial hanya dapat diakses satu proses dalam satu waktu — klik **Stop** pada Serial Plotter sebelum melakukan Upload program baru, agar proses upload tidak gagal karena port sedang terpakai
3. Pastikan rangkaian motor DC + driver (Modul 2), encoder quadrature (Modul 4 Percobaan 2), dan modul MPU6500 mode I2C (Modul 3) masing-masing sudah berfungsi normal — motor dan encoder berasal dari modul fisik yang sama
4. Buat project baru untuk Modul 5:
   - Name: `modul5-filtering-pid`
   - Board: **"Espressif ESP32 Dev Module"**
   - Framework: **Arduino**
5. Pastikan `platformio.ini` berisi:
   ```ini
   [env:esp32dev]
   platform = espressif32
   board = esp32dev
   framework = arduino
   ```
6. Tidak ada library eksternal tambahan yang dibutuhkan — seluruh fitur (interrupt, LEDC PWM) sudah tersedia dalam Arduino-ESP32 core, tidak perlu menambahkan baris `lib_deps` apa pun pada `platformio.ini`
7. **Alur kerja tiap Percobaan:** seluruh Percobaan pada modul ini (1–5) menggunakan **satu project PlatformIO yang sama** dari langkah 4–5 di atas. Setiap kode program pada modul ini bersifat **lengkap dan berdiri sendiri (self-contained)** — untuk berpindah ke Percobaan berikutnya, cukup **hapus seluruh isi** `src/main.cpp` dan **ganti dengan kode program Percobaan yang bersangkutan**, lalu **Build & Upload** ulang. Tidak perlu menggabungkan potongan kode dari beberapa Percobaan secara manual.

---

## E. Kegiatan Praktikum

### PERCOBAAN 1 — Filtering Alpha pada MPU6500 (Akselerometer)

**Tujuan:**
Mahasiswa mampu mengidentifikasi noise pada sinyal sensor mentah dan menerapkan low-pass filter alpha untuk menghaluskannya, sebagai pengantar konsep filtering sebelum diterapkan pada sinyal RPM yang lebih kompleks di Percobaan 2.

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| MPU6500 — SDA (pin SDI) | GPIO 21 | Mode I2C |
| MPU6500 — SCL (pin SCLK) | GPIO 22 | Mode I2C |
| MPU6500 — AD0 (pin SDO) | GND | Mengunci alamat I2C pada `0x68` |
| MPU6500 — CS/NCS | 3.3V (ditarik tetap) | Wajib, agar modul beroperasi dalam mode I2C |
| MPU6500 — VCC / GND | 3.3V / GND | — |

<img src="img/wiring_mpu6500_p1.png" alt="Gambar 6: Wiring MPU6500 mode I2C ke ESP32" width="60%">

*Gambar 6: Wiring MPU6500 mode I2C ke ESP32*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang MPU6500 sesuai skema (mode I2C, pin CS ditarik ke 3.3V)
2. Tulis dan upload kode lengkap di bawah, lalu buka **Serial Plotter** untuk mengamati kurva `Accel_Mentah` dan `Accel_Alpha` secara bersamaan
3. Ketuk meja pelan atau goyangkan sensor. Amati perbedaan antara garis `Accel_Mentah` yang naik-turun tajam (mengandung *noise*) dan garis `Accel_Alpha` yang sudah dihaluskan oleh filter
4. Ubah nilai `FILTER_ALPHA` menjadi `0.3`, lalu `0.7`, lalu `0.9`. Klik Build dan Upload ulang untuk tiap nilai (jangan lupa klik **Stop** pada Serial Plotter sebelum Upload). Analisis untung ruginya: makin besar α makin halus sinyalnya, tetapi makin lambat mengikuti perubahan (*lag*)

**Kode Program (MPU6500 + Low-Pass Filter Alpha):**
```cpp
#include <Arduino.h>
#include <Wire.h>

#define MPU6500_ADDR 0x68
#define PWR_MGMT_1   0x6B
#define ACCEL_XOUT_H 0x3B

#define FILTER_ALPHA 0.7 // sesuaikan: makin besar = makin halus, makin lambat merespons

float rawAccel = 0.0;
float filteredAccel = 0.0;

void writeRegister(uint8_t reg, uint8_t value)
{
    Wire.beginTransmission(MPU6500_ADDR);
    Wire.write(reg);
    Wire.write(value);
    Wire.endTransmission();
}

int16_t read16(uint8_t reg)
{
    Wire.beginTransmission(MPU6500_ADDR);
    Wire.write(reg);
    Wire.endTransmission(false); // repeated start, bus tetap dikuasai

    Wire.requestFrom(MPU6500_ADDR, 2);

    uint8_t high = Wire.read();
    uint8_t low  = Wire.read();

    return (high << 8) | low;
}

void setup()
{
    Serial.begin(115200);
    Wire.begin(21, 22); // SDA, SCL

    writeRegister(PWR_MGMT_1, 0x00); // bangunkan dari sleep mode
    delay(100);
}

void loop()
{
    int16_t az = read16(ACCEL_XOUT_H + 4); // sumbu Z

    // Sensitivitas default +-2g -> 16384 LSB/g
    rawAccel = az / 16384.0;

    // Low-pass filter alpha
    filteredAccel = FILTER_ALPHA * filteredAccel + (1.0 - FILTER_ALPHA) * rawAccel;

    Serial.print(">");
    Serial.print("Accel_Mentah:");
    Serial.print(rawAccel, 3);
    Serial.print(",Accel_Alpha:");
    Serial.print(filteredAccel, 3);
    Serial.println();

    delay(50);
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `writeRegister()` / `read16()` | Fungsi baca/tulis register MPU6500 via I2C |
| `az / 16384.0` | Konversi nilai mentah 16-bit ke satuan g, sesuai sensitivitas default ±2g |
| `filteredAccel = FILTER_ALPHA * filteredAccel + (1.0 - FILTER_ALPHA) * rawAccel` | Implementasi rumus low-pass filter alpha pada Dasar Teori C.2 — persis sama dengan yang dipakai untuk RPM di Percobaan 2 |
| `delay(50)` | Sampling lebih cepat dibanding percobaan RPM (100ms) karena sinyal akselerometer berubah lebih cepat |

---

### PERCOBAAN 2 — Dari Pulsa ke RPM dengan Filtering Alpha

**Tujuan:**
Mahasiswa mampu mengonversi data pulsa mentah dari encoder (Modul 4 Percobaan 2) menjadi nilai RPM menggunakan konstanta estimasi dari spesifikasi motor, serta menerapkan low-pass filter alpha untuk menghaluskan sinyal RPM.

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| Encoder — Channel A (C1, kabel Kuning) | GPIO 32 | `INPUT_PULLUP`, dipasang ke interrupt (trigger `RISING`) — sama seperti Modul 4 Percobaan 2 |
| Encoder — Channel B (C2, kabel Hijau) | GPIO 33 | `INPUT_PULLUP`, dibaca di dalam ISR untuk menentukan arah |
| Encoder — VCC (kabel Biru) | 3.3V–5V | — |
| Encoder — GND (kabel Hitam) | GND | — |

> Kabel daya motor (M1 Merah / M2 Putih) **tidak digunakan** pada percobaan ini — motor diputar dengan tangan.

<img src="img/wiring_encoder_esp32.png" alt="Gambar 7: Wiring diagram encoder quadrature (Channel A, Channel B, VCC, GND) ke ESP32, sama seperti Modul 4 Percobaan 2" width="60%">

*Gambar 7: Wiring diagram encoder quadrature (Channel A, Channel B, VCC, GND) ke ESP32, sama seperti Modul 4 Percobaan 2*

<img src="img/plot_filter_alpha_contoh.png" alt="Gambar 8: Contoh tampilan Serial Plotter yang diharapkan — garis RPM_Mentah bergerigi tajam berdampingan dengan garis RPM_Alpha yang jauh lebih halus" width="60%">

*Gambar 8: Contoh tampilan Serial Plotter yang diharapkan — garis RPM_Mentah bergerigi tajam berdampingan dengan garis RPM_Alpha yang jauh lebih halus*

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang encoder sesuai skema di atas (kabel daya motor M1/M2 belum disambungkan)
2. Tulis dan upload kode lengkap di bawah (yang menggabungkan pembacaan encoder dari Modul 4 Percobaan 2, konversi RPM dengan `PULSES_PER_REV = 102.0`, serta filter alpha)
3. Buka **Serial Plotter**, lalu putar poros motor dengan tangan. Nilai `RPM_Mentah` dan `RPM_Alpha` harus ikut berubah (lihat Gambar 8)
4. Perhatikan bahwa garis `RPM_Mentah` terlihat lebih bergerigi (*noisy*) dibanding sinyal akselerometer di Percobaan 1 karena pencacahan pulsa bersifat diskret per interval 100 ms
5. Ubah nilai `FILTER_ALPHA` menjadi `0.3`, lalu `0.7`, lalu `0.9`. Klik Build dan Upload ulang untuk tiap nilai. Analisis kapan nilai α besar atau kecil lebih menguntungkan pada pembacaan kecepatan motor

**Kode Program (Encoder + RPM + Low-Pass Filter Alpha — Program Lengkap):**
```cpp
#include <Arduino.h>
#include <math.h>

#define ENCODER_A_PIN 32
#define ENCODER_B_PIN 33

// Estimasi dari spesifikasi motor JGA25-370 1000RPM (11 PPR x rasio gearbox ~9.28)
// Bukan hasil kalibrasi manual, sehingga bisa meleset dari motor sungguhan Anda
const float PULSES_PER_REV = 102.0;

#define FILTER_ALPHA 0.7 // sesuaikan: makin besar = makin halus, makin lambat merespons

volatile int32_t encoderCount = 0;
portMUX_TYPE encoderMux = portMUX_INITIALIZER_UNLOCKED;

int32_t previousCount = 0;
unsigned long previousMillis = 0;
const unsigned long SAMPLE_INTERVAL_MS = 100;

float rawRPM = 0.0;
float filteredRPM = 0.0;

void IRAM_ATTR encoderA_ISR()
{
    bool channelB = digitalRead(ENCODER_B_PIN);

    portENTER_CRITICAL_ISR(&encoderMux);
    if (channelB == HIGH)
    {
        encoderCount++;
    }
    else
    {
        encoderCount--;
    }
    portEXIT_CRITICAL_ISR(&encoderMux);
}

void setup()
{
    Serial.begin(115200);

    pinMode(ENCODER_A_PIN, INPUT_PULLUP);
    pinMode(ENCODER_B_PIN, INPUT_PULLUP);

    attachInterrupt(digitalPinToInterrupt(ENCODER_A_PIN), encoderA_ISR, RISING);
}

void loop()
{
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= SAMPLE_INTERVAL_MS)
    {
        float deltaTime = (currentMillis - previousMillis) / 1000.0;
        previousMillis = currentMillis;

        int32_t currentCount;
        portENTER_CRITICAL(&encoderMux);
        currentCount = encoderCount;
        portEXIT_CRITICAL(&encoderMux);

        int32_t deltaCount;
        if (abs(currentCount - previousCount) > 600) // filter noise
        {
            deltaCount = 0;
        }
        else
        {
            deltaCount = currentCount - previousCount;
        }
        previousCount = currentCount;

        // Konversi pulsa -> RPM
        rawRPM = (deltaCount / deltaTime) * (60.0 / PULSES_PER_REV);

        // Filtering alpha
        filteredRPM = FILTER_ALPHA * filteredRPM + (1.0 - FILTER_ALPHA) * rawRPM;

        // Format khusus agar terbaca oleh ESP32 Serial Plotter (Serial Monitor -> Plotter)
        Serial.print(">");
        Serial.print("RPM_Mentah:");
        Serial.print(rawRPM, 2);
        Serial.print(",");
        Serial.print("RPM_Alpha:");
        Serial.print(filteredRPM, 2);
        Serial.println();
    }
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `if (abs(currentCount - previousCount) > 600)` | Filter penolak *noise* pulsa — jika selisih pulsa dalam 100 ms melonjak di atas 600 akibat *noise* sensor, `deltaCount` dianggap `0` sebelum dihitung menjadi RPM |
| `PULSES_PER_REV` | Estimasi dari spesifikasi motor (11 pulsa/putaran motor × rasio gearbox ~9.28) — bukan hasil kalibrasi manual, jadi bisa berbeda dari motor sungguhan Anda |
| `deltaTime = (currentMillis - previousMillis) / 1000.0` | Interval waktu sampling dikonversi ke detik, agar hasil RPM sesuai satuan (menit) |
| `rawRPM = (deltaCount / deltaTime) * (60.0 / PULSES_PER_REV)` | Implementasi langsung rumus RPM pada Dasar Teori C.1 |
| `filteredRPM = FILTER_ALPHA * filteredRPM + (1.0 - FILTER_ALPHA) * rawRPM` | Implementasi rumus low-pass filter alpha yang sama seperti Percobaan 1, kali ini pada sinyal RPM |

---

### PERCOBAAN 3 — Filtering dengan Kalman Filter

**Tujuan:**
Mahasiswa mampu menerapkan Kalman filter 1D sebagai metode filtering alternatif untuk sinyal RPM, serta membandingkan hasilnya dengan low-pass filter alpha pada Percobaan 2.

> **Catatan:** Sama seperti Percobaan 2, fokusnya adalah **membandingkan bentuk tiga garis** pada grafik, bukan mengubah kecepatan motor.

<img src="img/plot_filter_kalman_contoh.png" alt="Gambar 9: Contoh tampilan Serial Plotter dengan tiga garis (RPM_Mentah, RPM_Alpha, RPM_Kalman) pada kondisi RPM yang sama, untuk perbandingan visual" width="60%">

*Gambar 9: Contoh tampilan Serial Plotter dengan tiga garis (RPM_Mentah, RPM_Alpha, RPM_Kalman) pada kondisi RPM yang sama, untuk perbandingan visual*

**Skema Rangkaian:**

| Komponen | Pin ESP32 | Keterangan |
|---|---|---|
| Encoder — Channel A (C1, kabel Kuning) | GPIO 32 | `INPUT_PULLUP`, dipasang ke interrupt (trigger `RISING`) |
| Encoder — Channel B (C2, kabel Hijau) | GPIO 33 | `INPUT_PULLUP`, dibaca di dalam ISR |
| Encoder — VCC (kabel Biru) | 3.3V–5V | Suplai daya sensor encoder |
| Encoder — GND (kabel Hitam) | GND | — |

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Upload kode di bawah. Kode ini sudah berisi RPM dan filter alpha sebagai pembanding, ditambah filter Kalman yang baru
2. Perhatikan bagian kelas `KalmanFilter` pada kode
3. Tampilkan `RPM_Mentah`, `RPM_Alpha`, dan `RPM_Kalman` bersamaan di Serial Plotter (lihat Gambar 9)
4. Coba nilai awal Q dan R (0.001 dan 0.1), lalu ubah menjadi Q=0.1 dan R=5. Lihat perubahan bentuk garis `RPM_Kalman`
5. Bandingkan grafiknya: `RPM_Kalman` seharusnya lebih halus tetapi lebih cepat mengikuti perubahan dibanding `RPM_Alpha`. Tulis pengamatan Anda

**Kode Program (Encoder + RPM + Filter Alpha + Kalman Filter — Program Lengkap):**
```cpp
#include <Arduino.h>
#include <math.h>

#define ENCODER_A_PIN 32
#define ENCODER_B_PIN 33

// Estimasi dari spesifikasi motor JGA25-370 1000RPM — bukan hasil kalibrasi manual
const float PULSES_PER_REV = 102.0;

#define FILTER_ALPHA 0.7 // filter alpha, sebagai pembanding

volatile int32_t encoderCount = 0;
portMUX_TYPE encoderMux = portMUX_INITIALIZER_UNLOCKED;

int32_t previousCount = 0;
unsigned long previousMillis = 0;
const unsigned long SAMPLE_INTERVAL_MS = 100;

float rawRPM = 0.0;
float filteredRPM = 0.0; // hasil filter alpha

class KalmanFilter
{
private:
    float Q = 0.001; // process noise - seberapa besar nilai sebenarnya diperkirakan berubah
    float R = 0.1;   // measurement noise - seberapa "berisik" hasil pengukuran sensor
    float X = 0;     // estimasi nilai saat ini
    float P = 1;     // estimasi ketidakpastian (error covariance)
    float K = 0;     // Kalman gain

public:
    float update(float measurement)
    {
        // Predict
        P += Q;

        // Update
        K = P / (P + R);
        X = X + K * (measurement - X);
        P = (1 - K) * P;

        return X;
    }
};

KalmanFilter rpmKalman;
float kalmanRPM = 0.0; // hasil Kalman filter

void IRAM_ATTR encoderA_ISR()
{
    bool channelB = digitalRead(ENCODER_B_PIN);

    portENTER_CRITICAL_ISR(&encoderMux);
    if (channelB == HIGH)
    {
        encoderCount++;
    }
    else
    {
        encoderCount--;
    }
    portEXIT_CRITICAL_ISR(&encoderMux);
}

void setup()
{
    Serial.begin(115200);

    pinMode(ENCODER_A_PIN, INPUT_PULLUP);
    pinMode(ENCODER_B_PIN, INPUT_PULLUP);

    attachInterrupt(digitalPinToInterrupt(ENCODER_A_PIN), encoderA_ISR, RISING);
}

void loop()
{
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= SAMPLE_INTERVAL_MS)
    {
        float deltaTime = (currentMillis - previousMillis) / 1000.0;
        previousMillis = currentMillis;

        int32_t currentCount;
        portENTER_CRITICAL(&encoderMux);
        currentCount = encoderCount;
        portEXIT_CRITICAL(&encoderMux);

        int32_t deltaCount;
        if (abs(currentCount - previousCount) > 600) // filter noise
        {
            deltaCount = 0;
        }
        else
        {
            deltaCount = currentCount - previousCount;
        }
        previousCount = currentCount;

        // Konversi pulsa -> RPM
        rawRPM = (deltaCount / deltaTime) * (60.0 / PULSES_PER_REV);

        // Filtering alpha (pembanding)
        filteredRPM = FILTER_ALPHA * filteredRPM + (1.0 - FILTER_ALPHA) * rawRPM;

        // Filtering Kalman
        kalmanRPM = rpmKalman.update(rawRPM);

        Serial.print(">");
        Serial.print("RPM_Mentah:");
        Serial.print(rawRPM, 2);
        Serial.print(",RPM_Alpha:");
        Serial.print(filteredRPM, 2);
        Serial.print(",RPM_Kalman:");
        Serial.print(kalmanRPM, 2);
        Serial.println();
    }
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `P += Q` (tahap Predict) | Menaikkan ketidakpastian estimasi seiring waktu, sebelum ada pengukuran baru yang menguranginya kembali |
| `K = P / (P + R)` | Kalman gain — rasio ketidakpastian model terhadap total ketidakpastian (model + pengukuran); menentukan seberapa besar pengukuran baru "dipercaya" |
| `X = X + K * (measurement - X)` (tahap Update) | Estimasi diperbarui sebagian menuju nilai pengukuran baru, sebesar proporsi `K` |
| `P = (1 - K) * P` | Ketidakpastian berkurang setelah menggabungkan informasi dari pengukuran baru |
| Nilai `Q` dan `R` sebagai parameter tuning | Berbeda dari filter alpha yang hanya punya 1 parameter, Kalman filter punya 2 parameter yang saling memengaruhi — lebih fleksibel namun juga lebih kompleks untuk di-tuning |

**Latihan Tambahan:**
Bandingkan jumlah parameter yang perlu di-tuning (filter alpha: 1 parameter vs Kalman filter: 2 parameter) serta kompleksitas komputasi keduanya. Diskusikan: dalam kondisi seperti apa kompleksitas tambahan Kalman filter sepadan dengan manfaatnya dibanding filter alpha yang jauh lebih sederhana?

---

### PERCOBAAN 4 — Kontrol Closed-Loop: On-Off vs Proportional (P)

**Tujuan:**
Mahasiswa mampu mengimplementasikan dan membandingkan kontrol on-off dengan kontrol Proportional (P) untuk mengatur kecepatan motor DC menuju target RPM.

> **Catatan:** Percobaan ini adalah yang pertama di modul ini di mana motor dikendalikan oleh program (closed-loop) — bukan diputar tangan lagi seperti percobaan-percobaan sebelumnya.

<img src="img/wiring_motor_encoder_gabungan.png" alt="Gambar 10: Wiring diagram gabungan encoder + driver motor (L298N) + ESP32 dalam satu rangkaian, digunakan mulai Percobaan 4 hingga akhir modul" width="65%">

*Gambar 10: Wiring diagram gabungan encoder + driver motor (L298N) + ESP32 dalam satu rangkaian, digunakan mulai Percobaan 4 hingga akhir modul*

<img src="img/plot_onoff_vs_p_contoh.png" alt="Gambar 11: Contoh grafik Serial Plotter perbandingan mode on-off (berosilasi di sekitar target) vs mode Proportional (stabil namun menyisakan selisih dari target)" width="60%">

*Gambar 11: Contoh grafik Serial Plotter perbandingan mode on-off (berosilasi di sekitar target) vs mode Proportional (stabil namun menyisakan selisih dari target)*

**Skema Rangkaian:**

| Komponen | Pin ESP32 / Tujuan | Keterangan |
|---|---|---|
| Encoder — Channel A (C1, kabel Kuning) | GPIO 32 | `INPUT_PULLUP`, dipasang ke interrupt (trigger `RISING`) |
| Encoder — Channel B (C2, kabel Hijau) | GPIO 33 | `INPUT_PULLUP`, dibaca di dalam ISR |
| Encoder — VCC (kabel Biru) | 3.3V–5V | Suplai daya sensor encoder |
| Encoder — GND (kabel Hitam) | GND ESP32 | — |
| Driver motor L298N — ENA | GPIO 25 | Sinyal PWM kecepatan (lepas jumper ENA pada L298N) |
| Driver motor L298N — IN1 | GPIO 26 | Arah putar motor |
| Driver motor L298N — IN2 | GPIO 27 | Arah putar motor |
| Driver motor L298N — +12V | (+) Catu daya eksternal 12V | **Jangan** ambil daya motor dari 5V USB langsung |
| Driver motor L298N — GND | (−) Catu daya 12V **dan** GND ESP32 | Wajib disatukan (*common ground*) |
| Motor DC — M1 (kabel Merah, +) | Driver OUT1 | Menukar M1/M2 membalik arah putar default motor |
| Motor DC — M2 (kabel Putih, −) | Driver OUT2 | — |

> Pin ENA/IN1/IN2 mengikuti Modul 2 Percobaan 3, kecuali IN2 dipindah ke GPIO 27 karena GPIO 33 kini dipakai encoder. Lihat Gambar 10 untuk wiring gabungan encoder + driver motor dalam satu rangkaian. Gunakan filter alpha sebagai sumber RPM terfilter.

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang motor DC, driver, dan encoder sesuai Gambar 10. Pakai catu daya terpisah untuk motor (bukan 5V dari USB)
2. Tetapkan target RPM = 100 di kode
3. Coba mode **on-off** dulu. Di Serial Plotter, RPM akan naik turun terus di sekitar target dan motor bergetar. Ini **normal** untuk mode on-off (bandingkan dengan Gambar 11)
4. Ganti ke mode **Proportional** (`Kp = 3.0`). RPM menjadi lebih stabil, tetapi berhenti sedikit di bawah target (disebut *steady-state error*). Ini juga normal untuk kontrol P
5. Ambil screenshot Serial Plotter untuk kedua mode, lalu hitung kasar selisih target dengan RPM rata-rata saat mode P sudah stabil
6. Jika motor tidak bergerak sama sekali, periksa kabel driver (Gambar 10) dan urutan `IN1` dan `IN2` sebelum `ledcWrite()` dipanggil

**Kode Program (Encoder + Filter + Kontrol On-Off/Proportional — Program Lengkap):**
```cpp
#include <Arduino.h>
#include <math.h>

// ==================== ENCODER ====================
#define ENCODER_A_PIN 32
#define ENCODER_B_PIN 33

// Estimasi dari spesifikasi motor JGA25-370 1000RPM — bukan hasil kalibrasi manual
const float PULSES_PER_REV = 102.0;

volatile int32_t encoderCount = 0;
portMUX_TYPE encoderMux = portMUX_INITIALIZER_UNLOCKED;

int32_t previousCount = 0;
unsigned long previousMillis = 0;
const unsigned long SAMPLE_INTERVAL_MS = 100;

float rawRPM = 0.0;
float filteredRPM = 0.0;
#define FILTER_ALPHA 0.7 // filter alpha

// ==================== DRIVER MOTOR (Modul 2) ====================
#define ENA 25
#define IN1 26
#define IN2 27

const int pwmChannel = 0;
const int pwmFreq = 1000;
const int pwmResolution = 8; // 0-255

// ==================== KONTROL ====================
const float targetRPM = 100.0;
const float Kp = 3.0; // untuk mode Proportional, sesuaikan hasil pengamatan

bool useProportional = true; // ganti false untuk menguji mode on-off

void IRAM_ATTR encoderA_ISR()
{
    bool channelB = digitalRead(ENCODER_B_PIN);

    portENTER_CRITICAL_ISR(&encoderMux);
    if (channelB == HIGH)
    {
        encoderCount++;
    }
    else
    {
        encoderCount--;
    }
    portEXIT_CRITICAL_ISR(&encoderMux);
}

void applyControl(float rpmInput)
{
    float error = targetRPM - rpmInput;
    int pwmOutput = 0;

    if (useProportional)
    {
        // Kontrol Proportional
        pwmOutput = (int)(Kp * error);
    }
    else
    {
        // Kontrol On-Off
        pwmOutput = (error > 0) ? 255 : 0;
    }

    pwmOutput = constrain(pwmOutput, 0, 255);
    ledcWrite(pwmChannel, pwmOutput);

    Serial.print(">");
    Serial.print("Target:");
    Serial.print(targetRPM, 2);
    Serial.print(",RPM:");
    Serial.print(rpmInput, 2);
    Serial.print(",PWM:");
    Serial.print(pwmOutput);
    Serial.println();
}

void setup()
{
    Serial.begin(115200);

    pinMode(ENCODER_A_PIN, INPUT_PULLUP);
    pinMode(ENCODER_B_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(ENCODER_A_PIN), encoderA_ISR, RISING);

    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    ledcSetup(pwmChannel, pwmFreq, pwmResolution);
    ledcAttachPin(ENA, pwmChannel);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
}

void loop()
{
    unsigned long currentMillis = millis();

    if (currentMillis - previousMillis >= SAMPLE_INTERVAL_MS)
    {
        float deltaTime = (currentMillis - previousMillis) / 1000.0;
        previousMillis = currentMillis;

        int32_t currentCount;
        portENTER_CRITICAL(&encoderMux);
        currentCount = encoderCount;
        portEXIT_CRITICAL(&encoderMux);

        int32_t deltaCount;
        if (abs(currentCount - previousCount) > 600) // filter noise
        {
            deltaCount = 0;
        }
        else
        {
            deltaCount = currentCount - previousCount;
        }
        previousCount = currentCount;

        // Konversi pulsa -> RPM
        rawRPM = (deltaCount / deltaTime) * (60.0 / PULSES_PER_REV);

        // Filtering alpha
        filteredRPM = FILTER_ALPHA * filteredRPM + (1.0 - FILTER_ALPHA) * rawRPM;

        // Kontrol on-off / proportional
        applyControl(filteredRPM);
    }
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `useProportional` | Flag sederhana untuk beralih antara mode on-off dan Proportional tanpa mengubah struktur program |
| `pwmOutput = (error > 0) ? 255 : 0` | Kontrol on-off — hanya dua kemungkinan output, penuh atau mati sama sekali |
| `pwmOutput = (int)(Kp * error)` | Kontrol Proportional — output berskala langsung dengan besar error |
| `constrain(pwmOutput, 0, 255)` | Membatasi output PWM agar tetap berada pada rentang valid 8-bit, mencegah nilai negatif atau melebihi batas maksimum |

---

### PERCOBAAN 5 — Kontrol PID Lengkap & Tuning

**Tujuan:**
Mahasiswa mampu mengimplementasikan kontrol PID lengkap untuk mengatur kecepatan motor DC menuju target RPM yang dapat diubah secara interaktif, serta melakukan tuning parameter Kp, Ki, dan Kd.

> **Catatan:** Percobaan ini adalah puncak/akhir dari seluruh modul — menggabungkan encoder, filtering, dan kontrol dari percobaan-percobaan sebelumnya menjadi satu sistem PID lengkap.

<img src="img/wiring_pid_lengkap.png" alt="Gambar 12: Wiring diagram sistem lengkap Percobaan 5 — encoder + driver motor + 2 tombol target RPM, seluruhnya terhubung ke satu ESP32" width="60%">

*Gambar 12: Wiring diagram sistem lengkap Percobaan 5 — encoder + driver motor + 2 tombol target RPM, seluruhnya terhubung ke satu ESP32*

<img src="img/plot_pid_sebelum_sesudah_tuning.png" alt="Gambar 13: Contoh grafik Serial Plotter respons sistem sebelum tuning (lambat/berosilasi/overshoot besar) dibandingkan setelah tuning (cepat stabil, overshoot terkendali)" width="60%">

*Gambar 13: Contoh grafik Serial Plotter respons sistem sebelum tuning (lambat/berosilasi/overshoot besar) dibandingkan setelah tuning (cepat stabil, overshoot terkendali)*

**Skema Rangkaian:**

| Komponen | Pin ESP32 / Tujuan | Keterangan |
|---|---|---|
| Encoder — Channel A (C1, kabel Kuning) | GPIO 32 | `INPUT_PULLUP`, dipasang ke interrupt (trigger `RISING`) |
| Encoder — Channel B (C2, kabel Hijau) | GPIO 33 | `INPUT_PULLUP`, dibaca di dalam ISR |
| Encoder — VCC (kabel Biru) | 3.3V–5V | Suplai daya sensor encoder |
| Encoder — GND (kabel Hitam) | GND ESP32 | — |
| Driver motor L298N — ENA | GPIO 25 | Sinyal PWM kecepatan (lepas jumper ENA pada L298N) |
| Driver motor L298N — IN1 | GPIO 26 | Arah putar motor |
| Driver motor L298N — IN2 | GPIO 27 | Arah putar motor |
| Driver motor L298N — +12V | (+) Catu daya eksternal 12V | **Jangan** ambil daya motor dari 5V USB langsung |
| Driver motor L298N — GND | (−) Catu daya 12V **dan** GND ESP32 | Wajib disatukan (*common ground*) |
| Motor DC — M1 (kabel Merah, +) | Driver OUT1 | Menukar M1/M2 membalik arah putar default motor |
| Motor DC — M2 (kabel Putih, −) | Driver OUT2 | — |
| Tombol Naik Target RPM | GPIO 14 | Satu kaki ke GPIO 14, kaki lain ke GND (`INPUT_PULLUP`) |
| Tombol Turun Target RPM | GPIO 16 (RX2) | Satu kaki ke GPIO 16, kaki lain ke GND (`INPUT_PULLUP`) |

Lihat Gambar 12 untuk wiring gabungan seluruh komponen di atas dalam satu rangkaian.

**`platformio.ini`:**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
```

**Langkah Kerja:**
1. Pasang encoder, driver motor, dan dua tombol target RPM sesuai Gambar 12
2. Upload kode di bawah
3. Tekan tombol naik sampai target sekitar 100 RPM. Motor akan mengejar target sendiri
4. Lihat Serial Plotter. Responsnya biasanya belum bagus. Ambil screenshot sebagai **"sebelum tuning"**
5. Lakukan **tuning** (mencari nilai terbaik), ubah satu parameter dalam satu waktu:
   - Naikkan **Kp** sampai responsnya cepat tetapi belum bergoyang berlebihan
   - Tambah **Ki** sampai RPM tepat di target (selisih yang tersisa hilang)
   - Tambah **Kd** jika RPM masih melewati target
   - Ambil screenshot hasil akhir sebagai **"setelah tuning"** (bandingkan dengan Gambar 13)
6. Bandingkan bentuk respons yang Anda dapat selama tuning dengan jenis-jenis hasil umum di Gambar 14. Analisis kira-kira kombinasi Kp, Ki, dan Kd apa yang menyebabkan tiap jenis respons

<img src="img/jenis_respons_pid.png" alt="Gambar 14: Jenis-jenis hasil respons kontrol PID: overdamped, underdamped, kritis/well-tuned, tidak stabil, steady-state error, dan integral windup" width="90%">

*Gambar 14: Jenis-jenis hasil respons kontrol PID: overdamped, underdamped, kritis/well-tuned, tidak stabil, steady-state error, dan integral windup*

**Kode Program (Kontrol PID Lengkap — Encoder, Filter, PID, Tombol Target):**
```cpp
#include <Arduino.h>
#include <math.h>

// ==================== ENCODER ====================
constexpr uint8_t ENCODER_A_PIN = 32;
constexpr uint8_t ENCODER_B_PIN = 33;

// Estimasi dari spesifikasi motor JGA25-370 1000RPM — bukan hasil kalibrasi manual
constexpr float PULSES_PER_OUTPUT_REV = 102.0f;

volatile int32_t encoderCount = 0;
portMUX_TYPE encoderMux = portMUX_INITIALIZER_UNLOCKED;

int32_t previousCount = 0;
uint32_t previousSampleTime = 0;
constexpr uint32_t SAMPLE_INTERVAL_MS = 100;

// ==================== DRIVER MOTOR (L298N) ====================
constexpr uint8_t ENA_PIN = 25;
constexpr uint8_t IN1_PIN = 26;
constexpr uint8_t IN2_PIN = 27;

constexpr int PWM_CHANNEL = 0;
constexpr uint32_t PWM_FREQUENCY = 1000;
constexpr uint8_t PWM_RESOLUTION = 8;

constexpr int PWM_MIN = 0;
constexpr int PWM_MIN_RUN = 55; // PWM minimum agar motor benar-benar berputar
constexpr int PWM_MAX = 255;

// ==================== TOMBOL TARGET RPM ====================
constexpr uint8_t BUTTON_UP_PIN = 14;
constexpr uint8_t BUTTON_DOWN_PIN = 16;
constexpr float TARGET_STEP_RPM = 10.0f;
constexpr float TARGET_MIN_RPM = 0.0f;
constexpr float TARGET_MAX_RPM = 200.0f;
constexpr uint32_t DEBOUNCE_MS = 40;

float targetRPM = 0.0f;

struct Button
{
    uint8_t pin;
    bool lastRawState;
    bool stableState;
    uint32_t lastChangeTime;
};

Button buttonUp = {BUTTON_UP_PIN, HIGH, HIGH, 0};
Button buttonDown = {BUTTON_DOWN_PIN, HIGH, HIGH, 0};

// ==================== FILTER (ALPHA) ====================
constexpr float FILTER_ALPHA = 0.70f;

float rawRPM = 0.0f;
float filteredRPM = 0.0f;

// ==================== PID ====================
// Nilai awal untuk memulai tuning — BUKAN nilai final
float Kp = 2.0f;
float Ki = 0.8f;
float Kd = 0.05f;

constexpr float INTEGRAL_MIN = -150.0f;
constexpr float INTEGRAL_MAX = 150.0f;

float integralError = 0.0f;
float previousError = 0.0f;
int currentPWM = 0;

// ==================== INTERRUPT ENCODER ====================
void IRAM_ATTR encoderA_ISR()
{
    bool channelB = digitalRead(ENCODER_B_PIN);

    portENTER_CRITICAL_ISR(&encoderMux);
    if (channelB == HIGH)
        encoderCount++;
    else
        encoderCount--;
    portEXIT_CRITICAL_ISR(&encoderMux);
}

// ==================== PEMBACAAN TOMBOL (DEBOUNCE) ====================
bool buttonPressed(Button &button)
{
    bool rawState = digitalRead(button.pin);

    if (rawState != button.lastRawState)
    {
        button.lastRawState = rawState;
        button.lastChangeTime = millis();
    }

    if (millis() - button.lastChangeTime >= DEBOUNCE_MS && rawState != button.stableState)
    {
        button.stableState = rawState;
        if (button.stableState == LOW)
        {
            return true;
        }
    }
    return false;
}

// ==================== KONTROL MOTOR ====================
void applyMotorPWM(int pwm)
{
    pwm = constrain(pwm, PWM_MIN, PWM_MAX);
    currentPWM = pwm;

    if (pwm == 0)
    {
        digitalWrite(IN1_PIN, LOW);
        digitalWrite(IN2_PIN, LOW);
        ledcWrite(PWM_CHANNEL, 0);
        return;
    }

    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
    ledcWrite(PWM_CHANNEL, pwm);
}

void stopMotor()
{
    applyMotorPWM(0);
    integralError = 0.0f;
    previousError = 0.0f;
}

// ==================== PERHITUNGAN PID ====================
void updatePID(float deltaTime)
{
    if (targetRPM <= 0.0f)
    {
        stopMotor();
        return;
    }

    float error = targetRPM - filteredRPM;
    integralError += error * deltaTime;
    integralError = constrain(integralError, INTEGRAL_MIN, INTEGRAL_MAX);

    float derivativeError = (error - previousError) / deltaTime;

    float pidOutput = (Kp * error) + (Ki * integralError) + (Kd * derivativeError);

    // Jika output PID kecil tapi target belum nol, beri PWM minimum agar motor mulai bergerak
    if (pidOutput > 0.0f && pidOutput < PWM_MIN_RUN)
    {
        pidOutput = PWM_MIN_RUN;
    }

    pidOutput = constrain(pidOutput, (float)PWM_MIN, (float)PWM_MAX);
    applyMotorPWM((int)pidOutput);

    previousError = error;
}

// ==================== SETUP ====================
void setup()
{
    Serial.begin(115200);

    pinMode(ENCODER_A_PIN, INPUT_PULLUP);
    pinMode(ENCODER_B_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(ENCODER_A_PIN), encoderA_ISR, RISING);

    pinMode(BUTTON_UP_PIN, INPUT_PULLUP);
    pinMode(BUTTON_DOWN_PIN, INPUT_PULLUP);

    pinMode(IN1_PIN, OUTPUT);
    pinMode(IN2_PIN, OUTPUT);
    ledcSetup(PWM_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION); // konfigurasi channel PWM (core 2.x)
    ledcAttachPin(ENA_PIN, PWM_CHANNEL);                   // hubungkan channel ke pin ENA

    stopMotor();
    previousSampleTime = millis();
}

// ==================== LOOP ====================
void loop()
{
    if (buttonPressed(buttonUp))
    {
        targetRPM = constrain(targetRPM + TARGET_STEP_RPM, TARGET_MIN_RPM, TARGET_MAX_RPM);
    }

    if (buttonPressed(buttonDown))
    {
        targetRPM = constrain(targetRPM - TARGET_STEP_RPM, TARGET_MIN_RPM, TARGET_MAX_RPM);
        if (targetRPM <= 0.0f)
        {
            stopMotor();
        }
    }

    uint32_t currentTime = millis();
    if (currentTime - previousSampleTime >= SAMPLE_INTERVAL_MS)
    {
        float deltaTime = (currentTime - previousSampleTime) / 1000.0f;

        int32_t currentCount;
        portENTER_CRITICAL(&encoderMux);
        currentCount = encoderCount;
        portEXIT_CRITICAL(&encoderMux);

        int32_t deltaCount;
        if (abs(currentCount - previousCount) > 600) // filter noise
        {
            deltaCount = 0;
        }
        else
        {
            deltaCount = currentCount - previousCount;
        }
        previousCount = currentCount;

        // Konversi pulsa -> RPM
        rawRPM = fabsf((deltaCount * 60.0f) / (PULSES_PER_OUTPUT_REV * deltaTime));

        // Filtering alpha (dapat diganti Kalman filter — lihat Latihan Tambahan)
        filteredRPM = FILTER_ALPHA * filteredRPM + (1.0f - FILTER_ALPHA) * rawRPM;

        // Kontrol PID
        updatePID(deltaTime);

        // Output untuk Serial Plotter
        Serial.print(">Target:");
        Serial.print(targetRPM, 2);
        Serial.print(",RPM:");
        Serial.print(filteredRPM, 2);
        Serial.print(",PWM:");
        Serial.print(currentPWM);
        Serial.println();

        previousSampleTime = currentTime;
    }
}
```

**Penjelasan Kode:**
| Bagian | Penjelasan |
|---|---|
| `updatePID()` | Implementasi langsung persamaan PID diskret pada Dasar Teori C.5, termasuk integral clamping dan PWM minimum |
| `integralError = constrain(integralError, INTEGRAL_MIN, INTEGRAL_MAX)` | Mencegah *integral windup* — akumulasi error yang membesar tanpa batas saat sistem tidak dapat mengejar target dalam waktu lama |
| `PWM_MIN_RUN` | Mengatasi *deadzone* motor — output PID kecil namun bukan nol dinaikkan ke ambang minimum agar motor benar-benar mulai berputar |
| `buttonPressed()` dengan `struct Button` | Debouncing berbasis state machine (sama seperti Modul 1) untuk kedua tombol target RPM, mencegah satu kali tekan terhitung berkali-kali |
| Alur `loop()` | Menggabungkan seluruh tahapan modul ini dalam satu siklus sampling: decoding encoder → konversi RPM → filtering → kontrol PID → tampilkan hasil |

---

## F. Tugas Modul

*(Sementara dikosongkan — akan diisi ulang menyesuaikan struktur baru modul ini.)*

---

## G. Referensi
1. sss2022, *Closed-Loop Speed Control of a DC Motor With Encoder Using a Discrete PI Controller on Arduino*, Instructables — rujukan formula RPM, filter, dan struktur kontrol PI, https://www.instructables.com/Closed-Loop-Speed-Control-of-a-DC-Motor-With-Encod/
2. Greg Welch & Gary Bishop, *An Introduction to the Kalman Filter*, University of North Carolina at Chapel Hill — referensi dasar teori Kalman filter
3. Espressif Systems, *ESP32 Arduino Core Documentation — LEDC*, https://docs.espressif.com/projects/arduino-esp32/
4. Katsuhiko Ogata, *Modern Control Engineering*, Pearson — referensi dasar teori kontrol PID
5. PlatformIO Documentation, https://docs.platformio.org/
6. badlogic, *Serial Plotter — VSCode Extension*, digunakan untuk visualisasi data Serial Plotter pada seluruh Percobaan modul ini, https://github.com/badlogic/serial-plotter
