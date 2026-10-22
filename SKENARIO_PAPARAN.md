# Skenario Paparan (3 Orang, Tanpa PPT, Langsung Kode)

**Aplikasi:** Kasir Laundry + Segmentasi Pelanggan (K-Means berbasis RFM)
**Durasi:** sekitar 12-15 menit paparan + 5 menit tanya jawab
**Layar:** buka 2 jendela berdampingan: editor kode (VS Code) dan browser dengan aplikasi Streamlit.

## Persiapan (lakukan SEBELUM presentasi, malam ini atau besok siang)
1. `pip install -r requirements.txt`
2. `streamlit run app.py`
3. Buka tab **Pelanggan**, klik **Isi data contoh** supaya data siap.
4. Jalankan sekali tab Segmentasi, pastikan tidak error.
5. Siapkan 3 file terbuka di editor: `database.py`, `app.py`, `segmentasi.py`.
6. Bawa cadangan: rekam layar demo (video 2 menit) kalau-kalau laptop bermasalah.

## Pembagian Peran

| Orang | Fokus | File | Durasi |
|---|---|---|---|
| **Orang 1** | Pembuka, masalah, database dan alur kasir | `database.py` | 4 menit |
| **Orang 2** | Antarmuka dan alur order (kasir, status, laporan) | `app.py` | 4 menit |
| **Orang 3** | Algoritma K-Means RFM dan hasil | `segmentasi.py` | 6 menit |

Semua ikut menjawab pertanyaan sesuai bagiannya.

---

## ORANG 1: Pembuka + Database (4 menit)

**Buka (30 detik)**
> "Selamat malam. Kami akan mempresentasikan aplikasi **Kasir Laundry dengan Segmentasi Pelanggan memakai K-Means**. Masalahnya: pemilik laundry biasanya mencatat transaksi, tetapi tidak tahu pelanggan mana yang setia dan mana yang sudah lama tidak datang. Aplikasi kami menyelesaikan dua hal: mencatat order, lalu mengelompokkan pelanggan secara otomatis."

**Tunjukkan `database.py` (3 menit)**
1. Scroll ke `init_db()`:
   > "Kami memakai SQLite dengan 3 tabel: `pelanggan`, `layanan`, dan `orders`. Layanan awal sudah diisi: cuci kering, cuci setrika, setrika saja, express, dan selimut."
2. Scroll ke `buat_order()`:
   > "Total dihitung otomatis: harga layanan dikali jumlah kg. Contoh: Cuci Setrika Rp7.000 × 3 kg = Rp21.000."
3. Scroll ke `ubah_status()` dan `STATUS`:
   > "Setiap order punya status: Diterima, Diproses, Selesai, Diambil."
4. Scroll ke `isi_data_contoh()`:
   > "Karena tidak ada dataset laundry publik, kami membuat **data sintetis** 45 pelanggan dengan tiga pola perilaku: sering dan baru datang, sedang, dan jarang serta lama tidak datang. Hasilnya 440 order. Kami sebutkan ini sebagai keterbatasan di akhir."

**Serah terima:**
> "Selanjutnya Orang 2 akan menunjukkan bagaimana database ini dipakai di antarmuka."

---

## ORANG 2: Antarmuka + Alur Order (4 menit)

**Tunjukkan `app.py` lalu demo di browser (4 menit)**

1. Kode: baris `st.tabs(...)`:
   > "Aplikasi dibuat dengan Streamlit, terdiri dari 4 tab: Kasir, Daftar Order, Pelanggan, dan Segmentasi."
2. **Demo tab Kasir** (di browser):
   - Pilih pelanggan, pilih layanan "Cuci Setrika", isi 3 kg.
   - Tunjukkan total berubah otomatis, klik **Simpan Order**.
   > "Total dihitung langsung sebelum disimpan, jadi kasir tidak perlu kalkulator."
3. **Demo tab Daftar Order:**
   - Tunjukkan ringkasan: total order, total pendapatan, jumlah yang belum diambil.
   - Ubah status order yang baru dibuat dari Diterima menjadi Selesai.
   > "Pemilik bisa memantau cucian yang belum diambil dan pendapatan."
4. **Demo tab Pelanggan:**
   - Tambah satu pelanggan baru.
   > "Pelanggan baru langsung muncul di pilihan kasir."

**Serah terima:**
> "Data transaksi yang terkumpul inilah bahan untuk fitur cerdas kami. Orang 3 akan menjelaskan algoritmanya."

---

## ORANG 3: Algoritma K-Means RFM (6 menit)

**Tunjukkan `segmentasi.py` lalu tab Segmentasi (6 menit)**

**1. Konsep RFM (1 menit)** (kode `hitung_rfm`)
> "RFM mengubah riwayat transaksi menjadi 3 angka per pelanggan: **Recency** (berapa hari sejak order terakhir), **Frequency** (berapa kali order), **Monetary** (total uang yang dibelanjakan)."
- Di browser, tunjukkan tabel RFM.

**2. Normalisasi (30 detik)** (kode `normalisasi`)
> "Monetary bernilai ratusan ribu, sedangkan Frequency hanya puluhan. Kalau tidak disamakan skalanya, Monetary mendominasi jarak. Kami memakai **Min-Max**: x' = (x − min) / (max − min), sehingga semua bernilai 0 sampai 1."

**3. Menentukan jumlah klaster (1,5 menit)** (kode `cari_k`)
> "K-Means butuh jumlah klaster k di awal. Kami menguji k = 2 sampai 6 dengan dua cara: **Elbow** (inertia, mencari titik siku) dan **Silhouette** (makin dekat 1 makin baik)."
- Di browser, tunjukkan grafik. Hasil kami: **silhouette tertinggi di k = 3 (0,69)**, dan elbow melandai setelah k = 3.
> "Karena itu kami memilih k = 3."

**4. Cara kerja K-Means (1,5 menit)** (kode `jalankan_kmeans`)
> "Langkahnya: (1) pilih k titik pusat awal, (2) tiap pelanggan masuk ke pusat terdekat memakai jarak Euclidean, (3) pusat dihitung ulang sebagai rata-rata anggota, (4) ulangi sampai pusat tidak berubah."
- Rumus jarak: d = √((R₁−R₂)² + (F₁−F₂)² + (M₁−M₂)²)

**5. Hasil dan interpretasi (1,5 menit)** (browser)
- Tunjukkan tabel rata-rata per klaster. Hasil pada data contoh kami:

| Segmen | Rata-rata Recency | Frequency | Monetary | Jumlah |
|---|---|---|---|---|
| Setia | ±7 hari | ±20 kali | ±Rp700 ribu | 15 |
| Reguler | ±25 hari | ±8 kali | ±Rp180 ribu | 15 |
| Pasif | ±126 hari | ±2 kali | ±Rp36 ribu | 15 |

> "Setia diberi diskon atau poin member, Reguler ditawari paket langganan, dan Pasif dikirimi promo 'kami rindu Anda'."

*(Angka bisa sedikit berbeda di layar Anda. Sebutkan angka yang tampil di aplikasi.)*

**Penutup (semua, 30 detik), Orang 1 atau 3:**
> "Kesimpulan: aplikasi mencatat order laundry dan memanfaatkan datanya untuk segmentasi pelanggan otomatis. **Keterbatasan:** data masih sintetis, dan K-Means sensitif terhadap titik awal dan outlier. **Pengembangan:** memakai data laundry nyata dan membandingkan dengan K-Medoids atau Agglomerative Clustering. Terima kasih."

---

## Antisipasi Pertanyaan Dosen

| Pertanyaan | Jawaban singkat | Penjawab |
|---|---|---|
| Mengapa K-Means? | Sederhana, cepat, cocok untuk data numerik RFM, hasilnya mudah diinterpretasi. | Orang 3 |
| Mengapa data dinormalisasi? | Skala R, F, M berbeda jauh; tanpa normalisasi Monetary mendominasi jarak. | Orang 3 |
| Bagaimana menentukan k? | Elbow dan Silhouette; k=3 silhouette tertinggi (0,69). | Orang 3 |
| Apa kelemahan K-Means? | Sensitif titik awal (kami pakai `n_init=10`), sensitif outlier, harus tentukan k di awal. | Orang 3 |
| Apa arti silhouette 0,69? | Klaster cukup terpisah dan padat; mendekati 1 berarti baik. Catatan: data sintetis sengaja berpola jelas. | Orang 3 |
| Mengapa data sintetis? | Tidak ada dataset laundry publik dan waktu terbatas; polanya dirancang realistis. Pengembangan: data laundry nyata. | Orang 1 |
| Mengapa SQLite? | Ringan, tanpa instalasi server, cukup untuk prototipe. | Orang 1 |
| Mengapa Streamlit? | Membuat antarmuka web dengan Python saja, cepat untuk prototipe. | Orang 2 |
| Bagaimana total dihitung? | Harga layanan × jumlah (kg atau item), di `buat_order()`. | Orang 1 / 2 |
| Apa manfaat bagi pemilik laundry? | Tahu pelanggan setia untuk diberi reward, dan pelanggan pasif untuk diajak kembali. | Semua |
| Apa yang membedakan dari kasir biasa? | Ada fitur cerdas: segmentasi otomatis dari data transaksi. | Semua |

## Tips Hari-H
- Latihan penuh minimal **2 kali** dengan stopwatch.
- Jangan membaca kode baris per baris; **tunjukkan fungsi kuncinya saja** dan jelaskan maksudnya.
- Kalau error di tengah demo, tetap tenang: ulangi klik **Isi data contoh** atau pindah ke video cadangan.
- Hafalkan angka kunci: **45 pelanggan, 440 order, k = 3, silhouette 0,69**.
