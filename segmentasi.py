"""
segmentasi.py  -  PERAN ORANG 3 (Algoritma K-Means + RFM)
Langkah: hitung RFM -> normalisasi -> cari k (Elbow & Silhouette) -> K-Means -> beri nama klaster.
"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score


def hitung_rfm(df_order, nama_pelanggan, hari_ini=None):
    """
    R = hari sejak order terakhir, F = jumlah order, M = total uang.
    df_order butuh kolom: id_pelanggan, tanggal, total
    """
    df = df_order.copy()
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    hari_ini = pd.Timestamp(hari_ini) if hari_ini is not None else pd.Timestamp.now().normalize()
    rfm = df.groupby("id_pelanggan").agg(
        Recency=("tanggal", lambda s: (hari_ini - s.max()).days),
        Frequency=("id", "count"),
        Monetary=("total", "sum"),
    )
    rfm.insert(0, "Pelanggan", rfm.index.map(nama_pelanggan))
    return rfm


def normalisasi(rfm):
    """Min-Max: x' = (x - min) / (max - min), supaya R, F, M setara skalanya."""
    scaler = MinMaxScaler()
    return scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])


def cari_k(X, k_max=6):
    """Hitung inertia (Elbow) dan silhouette untuk k = 2..k_max."""
    hasil = []
    for k in range(2, min(k_max, len(X) - 1) + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
        hasil.append({"k": k, "inertia": km.inertia_,
                      "silhouette": silhouette_score(X, km.labels_)})
    return pd.DataFrame(hasil)


def jalankan_kmeans(rfm, k):
    """Jalankan K-Means, lalu beri nama klaster berdasarkan skor rata-rata R/F/M."""
    X = normalisasi(rfm)
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    hasil = rfm.copy()
    hasil["Klaster"] = km.labels_

    # Skor klaster: Recency kecil itu baik, Frequency & Monetary besar itu baik
    ringkas = hasil.groupby("Klaster")[["Recency", "Frequency", "Monetary"]].mean()
    n = (ringkas - ringkas.min()) / (ringkas.max() - ringkas.min() + 1e-9)
    skor = (1 - n["Recency"]) + n["Frequency"] + n["Monetary"]
    urut = skor.sort_values(ascending=False).index.tolist()

    if k == 3:
        nama = {urut[0]: "Setia", urut[1]: "Reguler", urut[2]: "Pasif"}
    else:
        nama = {kl: f"Klaster {i + 1} (peringkat {i + 1})" for i, kl in enumerate(urut)}
    hasil["Segmen"] = hasil["Klaster"].map(nama)
    ringkas["Jumlah Pelanggan"] = hasil.groupby("Klaster").size()
    ringkas.index = [nama[i] for i in ringkas.index]
    return hasil, ringkas.round(1), km.inertia_, silhouette_score(X, km.labels_)


SARAN = {
    "Setia": "Beri poin/diskon member agar tetap loyal.",
    "Reguler": "Tawarkan paket langganan bulanan.",
    "Pasif": "Kirim promo 'kami rindu Anda' lewat WhatsApp.",
}
