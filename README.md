# Kasir Laundry + Segmentasi Pelanggan (K-Means RFM)

Aplikasi kasir laundry sederhana dengan fitur segmentasi pelanggan menggunakan K-Means berbasis RFM (Recency, Frequency, Monetary).

## Struktur
- `database.py` : SQLite, pelanggan, layanan, order, data contoh
- `app.py` : antarmuka Streamlit (Kasir, Daftar Order, Pelanggan, Segmentasi)
- `segmentasi.py` : RFM, normalisasi Min-Max, Elbow/Silhouette, K-Means

## Menjalankan (macOS / Linux)
```bash
git clone <URL-REPO>
cd laundry-app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Buka http://localhost:8501, masuk ke tab **Pelanggan**, klik **Isi data contoh**, lalu buka tab **Segmentasi**.

## Menjalankan (Windows)
```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Catatan
Data contoh bersifat sintetis (45 pelanggan, sekitar 440 order). Database `laundry.db` dibuat otomatis saat aplikasi dijalankan pertama kali.
