#!/bin/sh
# Dijalankan sekali saat volume database masih kosong (docker-entrypoint-initdb.d).
set -eu
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d postgres <<SQL
CREATE DATABASE metabase;
CREATE DATABASE data_uji;
CREATE ROLE pembaca LOGIN PASSWORD '$PEMBACA_PASSWORD';
SQL
psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d data_uji <<'SQL'
CREATE TABLE layanan_bulanan (
  bulan date, wilayah text, kanal text, jumlah_layanan int,
  waktu_tunggu_menit numeric(5,1), skor_kepuasan numeric(4,1), jumlah_keluhan int);
CREATE TABLE survei_responden (
  id_responden text PRIMARY KEY, wilayah text, kanal text, usia int, waktu_tunggu_menit numeric(5,1),
  jumlah_kunjungan int, petugas_ramah int, informasi_jelas int, puas text);
\copy layanan_bulanan FROM '/data/layanan_bulanan.csv' CSV HEADER
\copy survei_responden FROM '/data/survei_responden.csv' CSV HEADER
COMMENT ON TABLE layanan_bulanan IS 'Data SINTETIS untuk uji coba, bukan data nyata';
COMMENT ON TABLE survei_responden IS 'Data SINTETIS untuk uji coba, bukan data nyata';
-- Metabase cukup membaca data uji: akun pembaca hanya punya hak SELECT.
GRANT CONNECT ON DATABASE data_uji TO pembaca;
GRANT USAGE ON SCHEMA public TO pembaca;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pembaca;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO pembaca;
SQL
