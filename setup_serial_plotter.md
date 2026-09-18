# Tutorial Serial Plotter pada VSCode + PlatformIO

## A. Tujuan

Tutorial ini membahas instalasi, konfigurasi, dan penggunaan Serial Plotter pada Visual Studio Code (VSCode) untuk melakukan visualisasi data telemetri dari mikrokontroler secara real-time.

Setelah mengikuti tutorial ini, praktikan mampu:

1. Menginstal extension Serial Plotter pada VSCode.
2. Membuka dan mengonfigurasi Serial Plotter.
3. Menghubungkan Serial Plotter dengan serial interface ESP32.
4. Menentukan serial port dan baud rate yang sesuai.
5. Mengirim data telemetri dari ESP32 menggunakan format yang dapat diproses oleh Serial Plotter.
6. Menampilkan satu maupun beberapa variabel secara simultan.
7. Menggunakan Serial Plotter untuk melakukan observasi terhadap karakteristik sinyal, noise, respons transien, dan perubahan nilai parameter sistem.

---

# B. Persyaratan

Tutorial ini menggunakan konfigurasi berikut:

| Komponen | Konfigurasi |
|---|---|
| IDE | Visual Studio Code |
| Extension | Serial Plotter |
| Build System | PlatformIO |
| Mikrokontroler | ESP32 |
| Framework | Arduino |
| Interface | USB Serial |
| Baud Rate | 115200 bps |

Praktikan diasumsikan telah menyelesaikan instalasi VSCode dan PlatformIO serta telah memiliki project ESP32 berbasis Arduino.

Tutorial ini tidak membahas pembuatan project PlatformIO dari awal. Prosedur pembuatan project dan konfigurasi board dibahas pada modul pengantar mikrokontroler.

---

# C. Instalasi Serial Plotter

## C.1 Membuka Extension Manager

Buka Visual Studio Code.

Extension dapat diakses melalui **Extensions** pada Activity Bar di sisi kiri VSCode.

Alternatifnya, gunakan kombinasi tombol:

    Ctrl + Shift + X

Panel Extensions akan menampilkan daftar extension yang telah terpasang dan fasilitas pencarian extension dari Visual Studio Code Marketplace.

---

## C.2 Mencari Serial Plotter

Pada kolom pencarian Extensions, masukkan:

    Serial Plotter

Cari extension dengan nama:

    Serial Plotter

oleh:

    badlogic

Pilih extension tersebut dan klik:

    Install

Tunggu hingga proses instalasi selesai.

---

## C.3 Verifikasi Instalasi

Setelah instalasi selesai, buka **Command Palette** menggunakan:

    Ctrl + Shift + P

Kemudian masukkan:

    Serial Plotter: Open pane

Jika command tersebut tersedia dan panel Serial Plotter dapat dibuka, extension telah berhasil terpasang.

---

# D. Konsep Koneksi Serial

Serial Plotter memperoleh data dari serial interface yang digunakan oleh mikrokontroler.

Pada sistem ESP32, aliran data dapat digambarkan sebagai berikut:

    ESP32
       |
       | USB Serial
       v
    Serial Interface
       |
       | Data Stream
       v
    VSCode
       |
       v
    Serial Plotter
       |
       v
    Real-Time Visualization

ESP32 berfungsi sebagai sumber data. Firmware mengirimkan data melalui interface serial, sedangkan Serial Plotter menerima, melakukan parsing, dan memvisualisasikan data tersebut sebagai grafik.

Serial Plotter tidak menghasilkan data sensor secara langsung. Data yang divisualisasikan berasal dari nilai yang dikirimkan oleh firmware melalui komunikasi serial.

---

# E. Membuka Serial Plotter

## E.1 Membuka Panel

Buka Command Palette:

    Ctrl + Shift + P

Kemudian pilih:

    Serial Plotter: Open pane

Panel Serial Plotter akan ditampilkan pada area kerja VSCode.

---

## E.2 Menghubungkan ESP32

Hubungkan board ESP32 ke komputer menggunakan kabel USB.

Pastikan:

1. Board mendapatkan catu daya.
2. Kabel USB mendukung komunikasi data.
3. Serial interface ESP32 telah dikenali oleh sistem operasi.
4. Tidak terdapat aplikasi lain yang sedang menggunakan serial port yang sama.

---

# F. Konfigurasi Serial Port

## F.1 Identifikasi Serial Port

Serial Plotter harus menggunakan serial port yang terhubung dengan ESP32.

Pada sistem Linux, serial device umumnya memiliki format:

    /dev/ttyUSB0

atau:

    /dev/ttyACM0

Pada Windows, serial device umumnya memiliki format:

    COM3

    COM4

    COM5

Nama dan nomor serial port bergantung pada sistem operasi, USB-to-Serial interface, serta konfigurasi perangkat.

Praktikan tidak boleh mengasumsikan nomor port. Serial port harus ditentukan berdasarkan perangkat ESP32 yang sedang terhubung.

---

## F.2 Identifikasi melalui PlatformIO

Serial device yang tersedia dapat diperiksa melalui PlatformIO.

Buka terminal pada VSCode kemudian jalankan:

    pio device list

Perintah tersebut akan menampilkan serial device yang terdeteksi oleh komputer.

Contoh:

    /dev/ttyUSB0
    CP210x USB to UART Bridge

Jika ESP32 menggunakan USB-to-Serial converter seperti CP210x atau CH340, nama interface tersebut dapat muncul pada informasi perangkat.

---

## F.3 Memilih Port pada Serial Plotter

Pada panel Serial Plotter, pilih serial port yang sesuai dengan ESP32.

Contoh:

    /dev/ttyUSB0

Setelah port dipilih, pastikan port tersebut merupakan port yang sama dengan yang digunakan oleh board saat melakukan komunikasi serial.

Jika ESP32 tidak muncul pada daftar port:

1. Periksa koneksi USB.
2. Pastikan kabel USB merupakan kabel data.
3. Periksa apakah board terdeteksi oleh sistem operasi.
4. Gunakan `pio device list` untuk memeriksa serial device.
5. Lakukan refresh daftar port pada Serial Plotter.

---

# G. Konfigurasi Baud Rate

Baud rate menentukan kecepatan komunikasi serial antara ESP32 dan komputer.

Nilai baud rate pada Serial Plotter harus sama dengan nilai yang digunakan oleh firmware ESP32.

Contoh pada firmware:

    Serial.begin(115200);

Maka Serial Plotter harus dikonfigurasi menggunakan:

    115200

Konfigurasi komunikasi dapat direpresentasikan sebagai:

    ESP32
      |
      | 115200 bps
      |
      v
    Serial Plotter

Jika baud rate pada kedua sisi tidak sama, data yang diterima dapat menjadi tidak valid atau tidak dapat diproses sebagaimana mestinya.

---

# H. Format Data Serial Plotter

Serial Plotter memerlukan format data tertentu agar data numerik dapat dikenali sebagai variabel yang akan divisualisasikan.

Format dasar satu variabel:

    >NamaVariabel:nilai

Contoh:

    >RPM:120.5

Pada format tersebut:

    RPM

merupakan identifier variabel, sedangkan:

    120.5

merupakan nilai numerik yang dikirimkan.

---

## H.1 Pengiriman Beberapa Variabel

Beberapa variabel dapat dikirimkan dalam satu sample.

Format:

    >NamaVariabel1:nilai1,NamaVariabel2:nilai2

Contoh:

    >RPM:120.5,Target:150.0

Data tersebut merepresentasikan dua variabel:

    RPM
    Target

Serial Plotter kemudian dapat menampilkan kedua variabel tersebut sebagai data series yang berbeda pada grafik.

---

# I. Implementasi pada ESP32

Data telemetri dikirimkan menggunakan fungsi `Serial.print()` dan `Serial.println()`.

Contoh program:

    #include <Arduino.h>

    void setup()
    {
        Serial.begin(115200);
    }

    void loop()
    {
        float rpm = 120.5;
        float target = 150.0;

        Serial.print(">");

        Serial.print("RPM:");
        Serial.print(rpm);

        Serial.print(",Target:");
        Serial.print(target);

        Serial.println();

        delay(100);
    }

Program tersebut menghasilkan data serial:

    >RPM:120.5,Target:150.0

Setiap baris data merupakan satu sample yang dikirimkan dari ESP32 ke komputer.

---

# J. Menjalankan Data Acquisition

Setelah firmware berhasil di-upload ke ESP32, buka kembali Serial Plotter.

Konfigurasikan:

    Serial Port : Port ESP32
    Baud Rate   : 115200

Kemudian pilih:

    Start

Serial Plotter akan mulai melakukan data acquisition dari serial interface.

Apabila data diterima dengan format yang valid, variabel yang terdeteksi akan ditampilkan pada area plotting.

---

# K. Visualisasi Satu Variabel

Untuk menguji fungsi dasar Serial Plotter, gunakan program berikut:

    #include <Arduino.h>

    float value = 0.0;

    void setup()
    {
        Serial.begin(115200);
    }

    void loop()
    {
        Serial.print(">Sensor:");
        Serial.println(value);

        value += 1.0;

        delay(100);
    }

Data yang dikirimkan:

    >Sensor:0
    >Sensor:1
    >Sensor:2
    >Sensor:3
    ...

Serial Plotter akan mendeteksi satu variabel:

    Sensor

dan memvisualisasikan perubahan nilai tersebut terhadap waktu.

---

# L. Visualisasi Beberapa Variabel

Serial Plotter dapat digunakan untuk melakukan observasi beberapa parameter secara simultan.

Contoh:

    #include <Arduino.h>

    float sensorValue = 0.0;

    void setup()
    {
        Serial.begin(115200);
    }

    void loop()
    {
        float filteredValue = sensorValue * 0.8;

        Serial.print(">");

        Serial.print("Sensor:");
        Serial.print(sensorValue);

        Serial.print(",Filter:");
        Serial.print(filteredValue);

        Serial.println();

        sensorValue += 1.0;

        delay(100);
    }

Data yang dihasilkan:

    >Sensor:0,Filter:0
    >Sensor:1,Filter:0.8
    >Sensor:2,Filter:1.6
    >Sensor:3,Filter:2.4

Serial Plotter akan mendeteksi:

    Sensor
    Filter

Kedua variabel tersebut dapat diamati secara bersamaan sehingga hubungan antara sinyal masukan dan sinyal hasil pemrosesan dapat dibandingkan secara visual.

---

# M. Implementasi untuk Data Filtering

Serial Plotter dapat digunakan untuk membandingkan sinyal mentah dengan sinyal hasil filtering.

Contoh implementasi:

    Serial.print(">");

    Serial.print("RPM_Mentah:");
    Serial.print(rawRPM, 2);

    Serial.print(",");

    Serial.print("RPM_Alpha:");
    Serial.print(filteredRPM, 2);

    Serial.println();

Data yang dikirimkan akan memiliki format:

    >RPM_Mentah:125.42,RPM_Alpha:119.73

Dengan demikian terdapat dua data series:

    RPM_Mentah
    RPM_Alpha

Secara konseptual, aliran data dapat direpresentasikan sebagai:

    Encoder
       |
       v
    Pulse Counting
       |
       v
    RPM Calculation
       |
       +--------------------+
       |                    |
       v                    v
    RPM_Mentah           Filtering
                            |
                            v
                       RPM_Alpha
                            |
                            +------+
                                   |
                                   v
                             Serial Output
                                   |
                                   v
                            Serial Plotter

Melalui grafik tersebut, praktikan dapat melakukan observasi terhadap:

- Fluktuasi sinyal.
- Noise pengukuran.
- Respons filtering.
- Perubahan nilai terhadap waktu.
- Perbedaan antara sinyal mentah dan sinyal terfilter.
- Delay atau perubahan respons akibat proses filtering.

Pendekatan ini digunakan pada percobaan filtering untuk membandingkan data RPM sebelum dan setelah proses filtering.

---

# N. Visualisasi Parameter Sistem Kontrol

Serial Plotter juga dapat digunakan untuk melakukan observasi beberapa parameter pada sistem kontrol secara bersamaan.

Contoh:

    Serial.print(">");

    Serial.print("Target:");
    Serial.print(targetRPM);

    Serial.print(",");

    Serial.print("RPM:");
    Serial.print(currentRPM);

    Serial.print(",");

    Serial.print("PWM:");
    Serial.print(pwmValue);

    Serial.println();

Data yang dikirimkan:

    >Target:150,RPM:142,PWM:187

Serial Plotter kemudian dapat menampilkan:

    Target
    RPM
    PWM

Dengan konfigurasi tersebut, praktikan dapat melakukan observasi terhadap hubungan antara:

    Target
       |
       v
    Error
       |
       v
    Controller
       |
       v
    PWM
       |
       v
    Motor
       |
       v
    RPM

Data telemetri dari masing-masing bagian sistem dapat digunakan untuk membantu analisis perilaku sistem kontrol.

---

# O. Parameter yang Dapat Diamati

Serial Plotter dapat digunakan untuk memvisualisasikan berbagai parameter numerik dari sistem embedded.

Contoh parameter:

| Parameter | Fungsi |
|---|---|
| Sensor | Nilai hasil pembacaan sensor |
| RPM_Mentah | RPM sebelum filtering |
| RPM_Alpha | RPM setelah alpha filter |
| RPM_Kalman | RPM setelah Kalman filter |
| Target | Nilai referensi sistem |
| Error | Selisih antara target dan output |
| PWM | Duty cycle atau nilai kendali |
| Voltage | Tegangan hasil pengukuran |
| Current | Arus hasil pengukuran |

Pemilihan parameter bergantung pada sistem yang sedang diuji.

---

# P. Pengaturan Tampilan Grafik

Setelah data diterima, Serial Plotter menyediakan beberapa fasilitas untuk membantu observasi data.

## P.1 Variables

Panel Variables menampilkan variabel yang berhasil dikenali dari data serial.

Variabel dapat digunakan untuk mengetahui parameter yang sedang diplot dan nilai yang sedang diterima.

---

## P.2 Show / Hide Variables

Variabel tertentu dapat ditampilkan atau disembunyikan dari grafik.

Fitur ini berguna ketika program mengirimkan banyak parameter tetapi praktikan hanya ingin menganalisis beberapa parameter tertentu.

---

## P.3 Auto-Scroll

Fungsi Auto-Scroll digunakan agar area grafik secara otomatis mengikuti sample terbaru.

Fitur ini berguna ketika sistem menghasilkan data secara kontinu.

Jika diperlukan analisis terhadap sample sebelumnya, Auto-Scroll dapat dinonaktifkan.

---

## P.4 Zoom

Fitur Zoom digunakan untuk mengatur jumlah data yang ditampilkan pada area grafik.

Zoom dapat digunakan untuk:

- Melihat perubahan sinyal secara keseluruhan.
- Mengamati detail perubahan sinyal.
- Mengidentifikasi fluktuasi atau noise.
- Mengamati respons transien.

---

# Q. Prosedur Penggunaan pada Praktikum

Gunakan prosedur berikut ketika melakukan pengambilan data:

### 1. Hubungkan ESP32

Hubungkan ESP32 ke komputer menggunakan USB.

### 2. Pastikan firmware telah di-upload

Upload program melalui PlatformIO.

### 3. Buka Serial Plotter

Gunakan:

    Ctrl + Shift + P

kemudian:

    Serial Plotter: Open pane

### 4. Pilih serial port

Pilih serial port ESP32.

### 5. Atur baud rate

Gunakan nilai yang sama dengan firmware.

Contoh:

    115200

### 6. Jalankan acquisition

Pilih:

    Start

### 7. Jalankan eksperimen

Operasikan sensor, motor, actuator, atau sistem yang sedang diuji.

### 8. Amati grafik

Perhatikan perubahan setiap data series terhadap waktu.

### 9. Catat atau dokumentasikan hasil

Gunakan screenshot grafik atau data hasil pengamatan sesuai kebutuhan laporan praktikum.

### 10. Hentikan acquisition

Setelah eksperimen selesai, pilih:

    Stop

sebelum menggunakan serial port untuk keperluan lain.

---

# R. Penghentian Serial Plotter

Setelah proses pengambilan data selesai:

1. Pilih:

       Stop

2. Pastikan koneksi serial telah dihentikan.

3. Setelah serial port dilepas, lakukan upload firmware berikutnya jika diperlukan.

Serial port merupakan resource komunikasi yang dapat mengalami konflik apabila digunakan oleh beberapa aplikasi secara bersamaan.

Contoh konflik:

    Serial Plotter
          |
          +---- menggunakan /dev/ttyUSB0
          |
          X
          |
    PlatformIO Upload

Untuk menghindari konflik, hentikan Serial Plotter sebelum melakukan upload firmware apabila serial port yang sama akan digunakan kembali oleh PlatformIO.

---

# S. Troubleshooting

## S.1 Serial Port Tidak Terdeteksi

Jika ESP32 tidak muncul pada daftar serial port, lakukan pemeriksaan berikut:

    USB Cable
        ↓
    ESP32 Power
        ↓
    USB-to-Serial Detection
        ↓
    Operating System
        ↓
    PlatformIO Device List
        ↓
    Serial Plotter

Gunakan:

    pio device list

untuk memeriksa serial device yang terdeteksi.

Periksa juga apakah kabel USB yang digunakan mendukung komunikasi data.

---

## S.2 Serial Plotter Tidak Menampilkan Data

Periksa parameter berikut:

1. Serial port.
2. Baud rate.
3. Status firmware ESP32.
4. Format data serial.
5. Status koneksi Serial Plotter.

Pastikan firmware menggunakan:

    Serial.begin(115200);

dan Serial Plotter menggunakan:

    115200

---

## S.3 Data Serial Diterima tetapi Grafik Tidak Muncul

Periksa format data.

Format yang digunakan untuk plotting:

    >Sensor:100

Untuk beberapa variabel:

    >Sensor:100,Filter:95

Pastikan identifier variabel dan nilai numerik ditulis dengan benar.

Hindari mengirim data yang tidak diperlukan pada baris plotting apabila data tersebut dapat mengganggu proses parsing.

---

## S.4 Grafik Hanya Menampilkan Sebagian Variabel

Periksa apakah setiap variabel memiliki format:

    NamaVariabel:nilai

Contoh:

    >RPM:120,Target:150,PWM:180

Bukan:

    >RPM=120,Target=150,PWM=180

Gunakan format yang sesuai dengan parser Serial Plotter yang digunakan.

---

## S.5 Upload Firmware Gagal

Jika upload firmware gagal setelah Serial Plotter digunakan:

    Stop Serial Plotter
          ↓
    Pastikan serial port dilepas
          ↓
    Upload firmware
          ↓
    Jalankan Serial Plotter kembali

Jika masalah masih terjadi, periksa serial port yang dipilih oleh PlatformIO.

---

# T. Validasi Sistem

Sebelum digunakan untuk praktikum, lakukan validasi sederhana.

### Tahap 1 — Validasi komunikasi

Pastikan ESP32 dapat mengirim data:

    >Test:100

### Tahap 2 — Validasi satu channel

Pastikan Serial Plotter menampilkan:

    Test

### Tahap 3 — Validasi multi-channel

Kirim:

    >Sensor:100,Filter:90

Pastikan dua series muncul:

    Sensor
    Filter

### Tahap 4 — Validasi data dinamis

Gunakan data yang berubah terhadap waktu.

Contoh:

    >Sensor:100,Filter:95
    >Sensor:105,Filter:98
    >Sensor:110,Filter:102

Pastikan grafik bergerak mengikuti perubahan nilai.

### Tahap 5 — Validasi aplikasi

Gunakan Serial Plotter pada data aktual dari sensor atau sistem yang sedang diuji.

---

# U. Contoh Format Telemetri

Berikut beberapa contoh format yang dapat digunakan.

## U.1 Sensor Tunggal

    >Temperature:28.5

## U.2 Dua Sensor

    >Temperature:28.5,Humidity:72.4

## U.3 Encoder

    >Pulse:1250,RPM:120.5

## U.4 Filtering

    >Raw:125.4,Filtered:119.7

## U.5 Sistem Kontrol

    >Target:150,RPM:142,Error:8,PWM:187

Pemilihan nama variabel sebaiknya konsisten dan deskriptif agar grafik mudah diidentifikasi.

---

# V. Best Practice Pengiriman Data

Untuk memperoleh data telemetri yang lebih mudah dianalisis, gunakan beberapa prinsip berikut:

### 1. Gunakan nama variabel yang deskriptif

Gunakan:

    RPM_Mentah
    RPM_Alpha
    RPM_Kalman

daripada:

    A
    B
    C

### 2. Gunakan satu sample per baris

Contoh:

    >RPM:120,Target:150
    >RPM:121,Target:150
    >RPM:123,Target:150

### 3. Gunakan baud rate yang konsisten

Pastikan firmware dan Serial Plotter menggunakan parameter komunikasi yang sama.

### 4. Hindari output debug yang tidak diperlukan

Jika Serial Plotter digunakan untuk plotting, output debug sebaiknya tidak dicampurkan secara sembarangan dengan format data plotting.

Contoh yang kurang baik:

    >RPM:120
    DEBUG Motor OK
    >RPM:121

Gunakan channel atau format output yang konsisten agar proses parsing tidak terganggu.

### 5. Batasi frekuensi pengiriman data

Frekuensi pengiriman data harus disesuaikan dengan kebutuhan eksperimen.

Tidak semua sistem membutuhkan pengiriman data pada frekuensi yang sangat tinggi.

---

# W. Alur Keseluruhan

Workflow penggunaan Serial Plotter pada praktikum dapat dirangkum sebagai berikut:

    Firmware ESP32
          |
          v
    Sensor / System Data
          |
          v
    Data Processing
          |
          v
    Serial.print()
          |
          v
    USB Serial Interface
          |
          v
    VSCode Serial Plotter
          |
          v
    Data Parsing
          |
          v
    Data Series
          |
          v
    Real-Time Graph
          |
          v
    Signal Analysis

Dengan workflow tersebut, Serial Plotter digunakan sebagai interface observasi antara firmware embedded system dan praktikan.

---

# X. Ringkasan

Serial Plotter merupakan tool visualisasi yang dapat digunakan untuk mengubah data telemetri numerik dari ESP32 menjadi grafik secara real-time.

Parameter utama yang harus dikonfigurasi adalah:

    Serial Port
    Baud Rate
    Data Format

Firmware ESP32 harus mengirimkan data menggunakan format yang sesuai dengan parser Serial Plotter.

Contoh satu variabel:

    >RPM:120

Contoh beberapa variabel:

    >RPM:120,Target:150

Untuk aplikasi filtering:

    >RPM_Mentah:125.4,RPM_Alpha:119.7

Dengan memvisualisasikan beberapa data series secara simultan, praktikan dapat melakukan observasi terhadap karakteristik sinyal dan hubungan antarparameter sistem secara langsung.

Serial Plotter dapat digunakan pada berbagai aplikasi praktikum, termasuk pembacaan sensor, encoder, filtering, motor control, PWM, dan PID.