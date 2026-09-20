# Tugas Pendahuluan — Modul 4: Interrupt, Timer, Watchdog & Multitasking


1. Jelaskan perbedaan mendasar antara **polling** dan **interrupt** dalam menangani suatu kejadian (mis. perubahan sinyal dari tombol) pada mikrokontroler.
2. Mengapa kode di dalam ISR (Interrupt Service Routine) harus dibuat sesingkat dan sesederhana mungkin? Apa risikonya jika ISR berjalan terlalu lama?
3. Jelaskan perbedaan antara **timer interrupt** dan penggunaan fungsi `delay()` dalam menjalankan suatu tugas secara periodik.
4. Bagaimana **watchdog timer** bekerja untuk mendeteksi dan memulihkan sistem dari kondisi *hang* (macet)?
5. Jelaskan konsep **task** dan **queue** pada FreeRTOS, serta mengapa keduanya berguna untuk multitasking pada mikrokontroler dual-core seperti ESP32.
6. Buatlah analogi sederhana dalam kehidupan sehari-hari terkait mekanisme **WDT, ISR, dan FreeRTOS**
