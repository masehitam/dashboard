# Dashboard · Kementerian PANRB

Aplikasi untuk mengubah data milik pengguna menjadi **dashboard** yang bisa dipakai di sini maupun ditanam di aplikasi lain. Pembuatannya dibantu **AI MenPAN**, jadi pengguna tidak perlu menulis SQL.

| Bagian | Isi |
|---|---|
| Landing page | `landing/` (HTML/CSS/JS statis, disajikan nginx di `/`) |
| Aplikasi dashboard | [Metabase](https://www.metabase.com) v0.64 di `/app/` |
| Database | PostgreSQL 17: penyimpanan Metabase + database contoh `data_uji` (data **sintetis**) |

```text
compose.yaml      web (nginx) + metabase + pilot-db, semuanya restart otomatis
landing/          index.html, styles.css, flow.js
nginx/            konfigurasi: / landing, /app/ Metabase
db/init.sh        membuat database metabase & data_uji + akun hanya-baca "pembaca"
data/             data contoh CSV + generate.py (data rekaan, bukan data nyata)
.env.example      contoh variabel; salin ke .env
```

## Menjalankan

Prasyarat: Docker dengan Compose v2.

```bash
cp .env.example .env
# isi POSTGRES_PASSWORD dan PEMBACA_PASSWORD dengan nilai acak, misal: openssl rand -hex 16
docker compose up -d
```

Buka http://localhost:3100. Metabase butuh ±1–2 menit saat pertama kali.

Untuk server (bisa diakses dari jaringan), tambahkan di `.env`:

```bash
WEB_BIND=0.0.0.0
WEB_PORT=80
MB_SITE_URL=http://ALAMAT-SERVER/app
```

Semua container memakai `restart: unless-stopped`, jadi otomatis jalan lagi setelah server restart (selama Docker aktif saat boot).

| Perintah | Fungsi |
|---|---|
| `docker compose ps` | status |
| `docker compose logs -f metabase` | log Metabase |
| `docker compose down` | berhenti, data tetap |
| `docker compose pull && docker compose up -d` | perbarui image |

## Pertama kali di Metabase

1. Buka `/app/`, buat akun admin.
2. Tambah data: **Pengaturan admin → Database → Tambahkan database → PostgreSQL**. Untuk data contoh: host `pilot-db`, port `5432`, database `data_uji`, user `pembaca`, password = `PEMBACA_PASSWORD`. Untuk database instansi, gunakan akun **hanya-baca** khusus. Database di mesin yang sama dicapai lewat `host.docker.internal` (Docker Desktop) atau IP server.
3. **AI MenPAN (Metabot)**: **Pengaturan admin → AI**, pilih provider yang kompatibel OpenAI, base URL `https://ai.menpan.go.id/v1`, model sesuai yang diberikan pengelola (mis. `qwen3.6`), dan API key Anda. `MB_LLM_ALLOWED_NETWORKS=allow-private` sudah diset karena server AI ada di jaringan internal.
4. Buat pertanyaan (**+ Baru → Pertanyaan**) atau tanya Metabot, simpan, lalu susun di **+ Baru → Dashboard**.
5. Tanam ke aplikasi lain lewat **Bagikan → Sematkan** (lihat **Pengaturan admin → Embedding**; sebagian fitur embedding hanya ada di versi berbayar).

## Kendala umum

| Gejala | Solusi |
|---|---|
| `/app/` belum terbuka | Metabase masih memulai; cek `docker compose logs -f metabase`. |
| Chat AI "terjadi kesalahan" | Cek log Metabase. Biasanya provider atau nama model salah (pilih provider kompatibel OpenAI, bukan Mistral). |
| Port 3100 dipakai | Ganti `WEB_PORT` di `.env`. |

Kata sandi ada di `.env`. File itu dan `AKUN.md` tidak di-commit.

---
© 2026 Kementerian Pendayagunaan Aparatur Negara dan Reformasi Birokrasi · Made with ♥ by Biro Datin
