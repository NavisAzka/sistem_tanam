# Tugas Pendahuluan — Modul 1: Pengantar Mikrokontroler

1. Jelaskan perbedaan mendasar antara framework **Arduino** dan **ESP-IDF** dalam memprogram mikrokontroler, termasuk kelebihan dan kekurangan masing-masing.
2. Mengapa board STM32 Blackpill memerlukan programmer eksternal (ST-Link) untuk di-flash, sedangkan ESP32 dapat diprogram langsung melalui kabel USB? Kaitkan jawaban Anda dengan keberadaan chip USB-to-Serial.
3. Jelaskan perbedaan kondisi logika (HIGH/LOW) pada konfigurasi **pull-up** dan **pull-down** resistor, baik saat tombol tidak ditekan maupun saat ditekan.
4. Mengapa pin GPIO 34–39 pada ESP32 tidak dapat menggunakan resistor pull-up/pull-down internal? Apa konsekuensinya terhadap perancangan rangkaian yang menggunakan pin tersebut?
5. Jelaskan fenomena **bouncing** pada tombol mekanik — mengapa hal ini bisa terjadi — dan sebutkan minimal dua pendekatan untuk mengatasinya.
6. Bagaimana ADC (Analog-to-Digital Converter) mengubah sinyal analog menjadi nilai digital? Jelaskan pula pengaruh resolusi bit ADC terhadap presisi hasil pembacaan.
