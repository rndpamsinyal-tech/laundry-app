"""
app.py  -  PERAN ORANG 2 (Antarmuka & Alur Order)
Jalankan:  streamlit run app.py
"""
import streamlit as st
import pandas as pd
import database as db
import segmentasi as seg

st.set_page_config(page_title="Kasir Laundry", page_icon="🧺", layout="wide")
db.init_db()

st.title("🧺 Kasir Laundry + Segmentasi Pelanggan (K-Means RFM)")
tab1, tab2, tab3, tab4 = st.tabs(["🧾 Kasir", "📋 Daftar Order", "👥 Pelanggan", "📊 Segmentasi (K-Means)"])

# ---------------------------------------------------------------- TAB 1: KASIR
with tab1:
    pel = db.daftar_pelanggan()
    lay = db.daftar_layanan()
    if pel.empty:
        st.info("Belum ada pelanggan. Tambahkan di tab Pelanggan atau isi data contoh.")
    else:
        c1, c2, c3 = st.columns(3)
        nama_pel = c1.selectbox("Pelanggan", pel["nama"] + " - " + pel["no_hp"].fillna(""))
        nama_lay = c2.selectbox("Layanan", lay["nama"])
        baris_lay = lay[lay["nama"] == nama_lay].iloc[0]
        jumlah = c3.number_input(f"Jumlah ({baris_lay['satuan']})", min_value=0.5, value=1.0, step=0.5)

        total = int(baris_lay["harga"] * jumlah)
        st.metric("Total bayar", f"Rp {total:,}".replace(",", "."))

        if st.button("Simpan Order", type="primary"):
            id_p = int(pel.loc[(pel["nama"] + " - " + pel["no_hp"].fillna("")) == nama_pel, "id"].iloc[0])
            db.buat_order(id_p, int(baris_lay["id"]), jumlah)
            st.success("Order tersimpan. Status awal: Diterima.")

# ----------------------------------------------------------- TAB 2: DAFTAR ORDER
with tab2:
    orders = db.daftar_order()
    if orders.empty:
        st.info("Belum ada order.")
    else:
        st.subheader("Ringkasan")
        a, b, c = st.columns(3)
        a.metric("Total order", len(orders))
        b.metric("Total pendapatan", f"Rp {int(orders['total'].sum()):,}".replace(",", "."))
        c.metric("Belum diambil", int((orders["status"] != "Diambil").sum()))

        st.subheader("Ubah status order")
        aktif = orders[orders["status"] != "Diambil"]
        if not aktif.empty:
            d1, d2, d3 = st.columns([2, 1, 1])
            pilih = d1.selectbox(
                "Order", aktif["id"].astype(str) + " - " + aktif["pelanggan"] + " (" + aktif["status"] + ")")
            status_baru = d2.selectbox("Status baru", db.STATUS)
            if d3.button("Perbarui"):
                db.ubah_status(int(pilih.split(" - ")[0]), status_baru)
                st.rerun()
        st.dataframe(orders.drop(columns=["id_pelanggan"]), use_container_width=True, hide_index=True)

# ------------------------------------------------------------ TAB 3: PELANGGAN
with tab3:
    st.subheader("Tambah pelanggan")
    n1, n2, n3 = st.columns([2, 2, 1])
    nama = n1.text_input("Nama")
    hp = n2.text_input("No. HP")
    if n3.button("Tambah") and nama.strip():
        db.tambah_pelanggan(nama.strip(), hp.strip())
        st.rerun()

    st.subheader("Data contoh untuk demo")
    e1, e2 = st.columns(2)
    if e1.button("Isi data contoh (45 pelanggan)"):
        db.isi_data_contoh()
        st.rerun()
    if e2.button("Hapus semua data pelanggan & order"):
        db.hapus_semua_data()
        st.rerun()
    st.dataframe(db.daftar_pelanggan(), use_container_width=True, hide_index=True)

# --------------------------------------------------------- TAB 4: SEGMENTASI
with tab4:
    st.markdown("**Alur algoritma:** hitung RFM → normalisasi Min-Max → cari k (Elbow & Silhouette) → K-Means → interpretasi.")
    orders = db.daftar_order()
    if orders["id_pelanggan"].nunique() < 6 if not orders.empty else True:
        st.warning("Data belum cukup (minimal 6 pelanggan yang punya order). Isi data contoh di tab Pelanggan.")
    else:
        pel = db.daftar_pelanggan().set_index("id")["nama"]
        rfm = seg.hitung_rfm(orders, pel)

        st.subheader("1. Tabel RFM per pelanggan")
        st.dataframe(rfm, use_container_width=True)

        st.subheader("2. Menentukan jumlah klaster (k)")
        X = seg.normalisasi(rfm)
        hasil_k = seg.cari_k(X)
        g1, g2 = st.columns(2)
        g1.caption("Elbow (inertia): pilih titik siku")
        g1.line_chart(hasil_k.set_index("k")["inertia"])
        g2.caption("Silhouette: makin tinggi makin baik")
        g2.line_chart(hasil_k.set_index("k")["silhouette"])
        st.dataframe(hasil_k.round(3), hide_index=True)

        k = st.slider("Pilih k", 2, 6, 3)
        hasil, ringkas, inertia, sil = seg.jalankan_kmeans(rfm, k)

        st.subheader("3. Hasil K-Means")
        m1, m2 = st.columns(2)
        m1.metric("Inertia", f"{inertia:.2f}")
        m2.metric("Silhouette score", f"{sil:.3f}")
        st.caption("Rata-rata R, F, M per klaster")
        st.dataframe(ringkas, use_container_width=True)
        st.bar_chart(hasil["Segmen"].value_counts())

        st.subheader("4. Rekomendasi tindakan")
        if k == 3:
            for segmen, saran in seg.SARAN.items():
                st.write(f"**{segmen}**: {saran}")
        else:
            st.info("Rekomendasi otomatis tersedia untuk k = 3.")

        st.caption("Daftar pelanggan per segmen")
        st.dataframe(hasil.sort_values("Segmen"), use_container_width=True)
