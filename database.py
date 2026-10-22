"""
database.py  -  PERAN ORANG 1 (Database & Kasir)
Semua urusan SQLite: tabel, tambah pelanggan, buat order, ubah status, data contoh.
"""
import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd

DB = "laundry.db"
STATUS = ["Diterima", "Diproses", "Selesai", "Diambil"]


def conn():
    return sqlite3.connect(DB)


def init_db():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS pelanggan(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            no_hp TEXT
        );
        CREATE TABLE IF NOT EXISTS layanan(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            harga INTEGER NOT NULL,
            satuan TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pelanggan INTEGER NOT NULL,
            id_layanan INTEGER NOT NULL,
            jumlah REAL NOT NULL,
            total INTEGER NOT NULL,
            tanggal TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Diterima'
        );
        """)
        if c.execute("SELECT COUNT(*) FROM layanan").fetchone()[0] == 0:
            c.executemany(
                "INSERT INTO layanan(nama, harga, satuan) VALUES (?,?,?)",
                [("Cuci Kering", 5000, "kg"),
                 ("Cuci Setrika", 7000, "kg"),
                 ("Setrika Saja", 4000, "kg"),
                 ("Express (6 jam)", 12000, "kg"),
                 ("Selimut", 25000, "item")],
            )


def tambah_pelanggan(nama, no_hp):
    with conn() as c:
        c.execute("INSERT INTO pelanggan(nama, no_hp) VALUES (?,?)", (nama, no_hp))


def daftar_pelanggan():
    with conn() as c:
        return pd.read_sql("SELECT * FROM pelanggan ORDER BY nama", c)


def daftar_layanan():
    with conn() as c:
        return pd.read_sql("SELECT * FROM layanan", c)


def buat_order(id_pelanggan, id_layanan, jumlah, tanggal=None, status="Diterima"):
    """Hitung total = harga x jumlah, lalu simpan order."""
    tanggal = tanggal or datetime.now().strftime("%Y-%m-%d")
    with conn() as c:
        harga = c.execute("SELECT harga FROM layanan WHERE id=?", (id_layanan,)).fetchone()[0]
        total = int(harga * jumlah)
        c.execute(
            "INSERT INTO orders(id_pelanggan,id_layanan,jumlah,total,tanggal,status) VALUES (?,?,?,?,?,?)",
            (id_pelanggan, id_layanan, jumlah, total, tanggal, status),
        )
    return total


def daftar_order():
    with conn() as c:
        return pd.read_sql("""
            SELECT o.id, p.nama AS pelanggan, l.nama AS layanan, o.jumlah, l.satuan,
                   o.total, o.tanggal, o.status, o.id_pelanggan
            FROM orders o
            JOIN pelanggan p ON p.id = o.id_pelanggan
            JOIN layanan l ON l.id = o.id_layanan
            ORDER BY o.id DESC
        """, c)


def ubah_status(id_order, status_baru):
    with conn() as c:
        c.execute("UPDATE orders SET status=? WHERE id=?", (status_baru, id_order))


def isi_data_contoh():
    """Buat 45 pelanggan sintetis dengan 3 pola perilaku (setia, reguler, pasif)."""
    random.seed(42)
    hari_ini = datetime.now()
    nama_depan = ["Budi", "Siti", "Andi", "Rina", "Dewi", "Agus", "Fajar", "Maya", "Rudi",
                  "Lina", "Hadi", "Sari", "Joko", "Tina", "Eko"]
    nama_belakang = ["Santoso", "Wijaya", "Putri", "Pratama", "Lestari", "Nugroho", "Hidayat"]
    # (jumlah pelanggan, rentang frekuensi order, rentang hari terakhir order, rentang kg)
    pola = [(15, (14, 24), (0, 10), (3, 7)),     # setia
            (15, (5, 9), (10, 40), (2, 5)),      # reguler
            (15, (1, 3), (70, 170), (1, 4))]     # pasif
    ids_layanan = daftar_layanan()["id"].tolist()
    with conn() as c:
        for n, (f_lo, f_hi), (r_lo, r_hi), (k_lo, k_hi) in pola:
            for _ in range(n):
                nama = f"{random.choice(nama_depan)} {random.choice(nama_belakang)}"
                hp = "08" + "".join(random.choices("0123456789", k=10))
                cur = c.execute("INSERT INTO pelanggan(nama,no_hp) VALUES (?,?)", (nama, hp))
                id_p = cur.lastrowid
                freq = random.randint(f_lo, f_hi)
                terakhir = random.randint(r_lo, r_hi)
                for i in range(freq):
                    hari_lalu = terakhir + i * random.randint(3, 9)
                    tgl = (hari_ini - timedelta(days=hari_lalu)).strftime("%Y-%m-%d")
                    id_l = random.choice(ids_layanan[:4])
                    kg = random.randint(k_lo, k_hi)
                    harga = c.execute("SELECT harga FROM layanan WHERE id=?", (id_l,)).fetchone()[0]
                    c.execute(
                        "INSERT INTO orders(id_pelanggan,id_layanan,jumlah,total,tanggal,status) VALUES (?,?,?,?,?,?)",
                        (id_p, id_l, kg, harga * kg, tgl, "Diambil"),
                    )


def hapus_semua_data():
    with conn() as c:
        c.executescript("DELETE FROM orders; DELETE FROM pelanggan;")
