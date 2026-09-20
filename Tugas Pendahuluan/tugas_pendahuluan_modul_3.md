# Tugas Pendahuluan — Modul 3: Komunikasi Serial

Kerjakan soal-soal berikut **sebelum** sesi praktikum berlangsung, sebagai persiapan agar Anda memiliki gambaran konsep dasar sebelum mempraktekkan Modul 3.

1. Jelaskan perbedaan mendasar antara protokol **UART**, **I2C**, dan **SPI**, khususnya dari segi jumlah jalur komunikasi yang digunakan dan kebutuhan sinyal clock bersama.
2. Bagaimana I2C dapat melayani lebih dari satu perangkat pada bus fisik yang sama, sedangkan SPI justru memerlukan jalur Chip Select (CS) terpisah untuk setiap perangkat?
3. Jelaskan mengapa kedua sisi komunikasi UART harus menyepakati **baud rate** yang sama terlebih dahulu sebelum dapat saling bertukar data dengan benar.
4. Apa keuntungan penggunaan DMA (Direct Memory Access) dibandingkan pembacaan data secara *blocking*, khususnya dari sisi pemanfaatan waktu CPU?
5. Selain UART, I2C, dan SPI, terdapat protokol komunikasi lain seperti **CAN bus**, **Modbus**, dan **1-Wire**. jelaskan secara singkat prinsip kerjanya serta pada jenis aplikasi apa protokol tersebut biasa digunakan.
