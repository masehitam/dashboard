"""Buat data contoh SINTETIS untuk uji coba Metabase/Superset/Orange. Bukan data instansi nyata.

Jalankan: python3 data/generate.py  (hanya pustaka standar, hasil selalu sama karena seed tetap)
"""
import csv
import math
import random
from pathlib import Path

random.seed(2026)
OUT = Path(__file__).parent
WILAYAH = {"Aceh": .9, "Sumatera Utara": 1.3, "DKI Jakarta": 2.2, "Jawa Barat": 2.0, "Jawa Tengah": 1.7,
           "Jawa Timur": 1.9, "Bali": .8, "Kalimantan Timur": .7, "Sulawesi Selatan": 1.0, "Papua": .5}
KANAL = ("Online", "Loket")

# 1) Rekap bulanan per wilayah & kanal: cocok untuk dashboard dan forecasting.
with open(OUT / "layanan_bulanan.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bulan", "wilayah", "kanal", "jumlah_layanan", "waktu_tunggu_menit", "skor_kepuasan", "jumlah_keluhan"])
    for m in range(42):  # Jan 2023 – Jun 2026
        year, month = 2023 + m // 12, m % 12 + 1
        season = 1 + .12 * math.sin(2 * math.pi * (month - 3) / 12)
        for nama, skala in WILAYAH.items():
            for kanal in KANAL:
                tren = 1 + (.025 if kanal == "Online" else -.004) * m
                jumlah = max(20, round(400 * skala * season * tren * random.uniform(.9, 1.1)))
                tunggu = round(max(3, (8 if kanal == "Online" else 22) - .08 * m + random.gauss(0, 2.5)), 1)
                skor = round(min(100, max(40, 88 - .9 * tunggu + random.gauss(0, 3))), 1)
                keluhan = max(0, round(jumlah * (.01 + .002 * tunggu) * random.uniform(.6, 1.4)))
                w.writerow([f"{year}-{month:02d}-01", nama, kanal, jumlah, tunggu, skor, keluhan])

# 2) Survei per responden: cocok untuk klasifikasi (puas ya/tidak) dan clustering di Orange.
with open(OUT / "survei_responden.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id_responden", "wilayah", "kanal", "usia", "waktu_tunggu_menit", "jumlah_kunjungan", "petugas_ramah", "informasi_jelas", "puas"])
    for i in range(1, 2001):
        wilayah, kanal = random.choice(list(WILAYAH)), random.choice(KANAL)
        usia = random.randint(18, 70)
        tunggu = round(max(1, random.gauss(9 if kanal == "Online" else 21, 6)), 1)
        kunjungan = random.randint(1, 8)
        ramah, jelas = random.randint(1, 5), random.randint(1, 5)
        z = -1.2 - .09 * tunggu + .55 * ramah + .45 * jelas + .01 * (usia - 40) + random.gauss(0, .8)
        w.writerow([f"R{i:04d}", wilayah, kanal, usia, tunggu, kunjungan, ramah, jelas, "Ya" if z > 0 else "Tidak"])
print("Selesai: layanan_bulanan.csv dan survei_responden.csv")
