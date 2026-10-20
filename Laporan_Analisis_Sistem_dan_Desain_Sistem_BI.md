# LAPORAN ANALISIS SISTEM & DESAIN SISTEM BUSINESS INTELLIGENCE TERINTEGRASI

### *Integrasi Data Mining — Cross-Selling (Apriori) & Segmentasi Pelanggan (K-Means RFM) pada Platform BI Ritel Modern*

---

| Label Dokumen | Keterangan |
|---|---|
| **Judul** | Laporan Analisis Sistem & Integrasi Data Mining — Business Intelligence Dashboard |
| **Sub-judul** | Strategi Cross-Selling (Apriori) & Segmentasi Pelanggan (K-Means RFM) Berbasis Data Transaksi Ritel |
| **Penyusun** | Caecillia Jessica Kinbenu — NIM 51230131 |
| **Program Studi** | Teknologi Informasi |
| **Mata Kuliah** | Business Intelligence |
| **Kegiatan** | Ujian Tengah Semester (UTS) — Semester 7 |
| **Objek Analisis** | PT. NusaRetail (studi kasus) — `P8. UTS_Business Intelligence.xlsx` |
| **Basis Data** | 18.513 baris transaksi · 30 produk · 1.480 pelanggan · Jan–Des 2025 |
| **Status Dokumen** | FINAL — Siap Presentasi Direksi / C-Level |
| **Versi** | 1.0 |

> **Catatan Kepatuhan Data:** Seluruh angka dalam laporan ini dihitung ulang secara reproducible dari dataset mentah melalui pipeline `data_pipeline → apriori_engine → segmentasi`. Tidak ada angka ilustratif yang digunakan sebagai fakta; setiap estimasi ekonomi pada **Tahap 6** diberi label asumsi secara eksplisit.

---

## DAFTAR ISI

```
BAGIAN 0  ─ RANCANGAN HALAMAN SAMPUL (COVER PAGE REDESIGN)
            0.1 Konsep Visual Eksekutif · 0.2 Wireframe Sampul · 0.3 Spesifikasi Elemen
            0.4 Prototipe HTML/CSS Sampul · 0.5 Panduan Tata Letak untuk Desainer

BAGIAN 0B ─ STANDARD UI/UX DESIGN SYSTEM "DARK EXECUTIVE MODE"
            Token Warna · Tipografi · Grid 12-Kolom · Hierarki Informasi
            Micro-interactions · UX Filter · Standar Komponen

TAHAP 1   ─ BUSINESS UNDERSTANDING & EXPLORATORY DATA ANALYSIS (EDA)
TAHAP 2   ─ DATA PREPROCESSING & FEATURE ENGINEERING
TAHAP 3   ─ MARKET BASKET ANALYSIS (ALGORITMA APRIORI)
TAHAP 4   ─ SEGMENTASI PELANGGAN (ALGORITMA K-MEANS)
TAHAP 5   ─ BUSINESS INTELLIGENCE DASHBOARD (UI/UX BLUEPRINT)
TAHAP 6   ─ REKOMENDASI KEPUTUSAN BISNIS PRESCRIFTIF

LAMPIRAN   ─ A. Katalog Produk · B. Glosarium Metrik · C. Arsitektur Sistem · D. Parameter Teknis
```

---
=== BAGIAN 0 ═══════════════════════════════════════════════════════════════
## RANCANGAN HALAMAN SAMPUL (COVER PAGE REDESIGN)
=== BAGIAN 0 ═══════════════════════════════════════════════════════════════
---

### 0.1 Konsep Visual Eksekutif

Sampul dirancang dengan prinsip **"Executive Dark Prestige"**: memadukan *dark navy* korporat sebagai bidang dominan, aksen *gold* untuk nilai/prestise, dan *teal* untuk sisi teknologi/data. Karakter visual bersifat **minimalis, kaku-teratur (structured), dan bebas ornamen berlebih** — sesuai dengan dokumen yang akan dibaca oleh tingkat Direksi/C-Level yang menuntut kredibilitas dalam < 8 detik pembacaan pertama.

| Prinsip | Implementasi |
|---|---|
| **Kredibilitas instan** | Pita *dark navy* penuh di 22% area atas + garis emas 4 px sebagai *rule* pemisah |
| **Keterbacaan hierarkis** | 3 tingkat judul: Main Title (32–36 pt, *bold*, *tight tracking*) → Sub-title (15 pt, *regular*, *teal*) → Metadata (10–11 pt, *uppercase*, *letter-spacing* lebar) |
| **Sentuhan personal** | Foto profil penyusun berbingkai emas pada blok identitas (bukan sebagai dekorasi, melainkan elemen *signature*) |
| **Ruang negatif** | Margin luar 64 px, *grid* 12 kolom, konten tidak pernah menyentuh 8% area tepi |
| **Konsistensi brand** | Aksen `Gold #C9A24B` hanya untuk garis, nomor, dan *highlight*; `Teal #2DD4BF` hanya untuk sub-judul & kata kunci data |

**Aset Foto Profil Penyusun** (ditempatkan pada kolom 10–12 sampul, bingkai emas 3 px, bentuk bulat Ø 172 px):

<p align="center">
  <img src="../assets/foto.jpeg" alt="Caecillia Jessica Kinbenu" width="172" height="172" style="border-radius:50%; border:3px solid #C9A24B; object-fit:cover;">
</p>
<p align="center"><sub>Caecillia Jessica Kinbenu · NIM 51230131 · Program Studi Teknologi Informasi</sub></p>

---

### 0.2 Wireframe Sampul (Tata Letak Grid)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐ ▲
│  ▌ DARK NAVY HEADER ZONE — tinggi 22% halaman  (#0B1220 → gradient ke #0F172A)      │ │
│                                                                                      │ │
│   LOGO / INSTITUSI                                              [ikon unggah-dokumen] │ │
│                                                                                      │ │
│   ──────────────────────────── garis emas 4px (#C9A24B) ──────────────────────────── │ │ 22%
│                                                                                      │ │
├──────────────────────────────────────────────────────────────────────────────────────┤ ▼
│                                                                                          │
│   [KOL 1-8]                                        [KOL 10-12]                        │
│                                                                                          │
│   "LAPORAN ANALISIS SISTEM &                                          ┌──────────────┐  │
│    INTEGRASI DATA MINING"          ← Main Title, 34pt Bold           │              │  │
│    ────────────────────────                                          │  FOTO PROFIL  │  │
│    Business Intelligence Dashboard                                  │  (bulat,     │  │
│                                                                      │  border gold │  │
│   Strategi Cross-Selling (Apriori) &                                │  3px)        │  │
│   Segmentasi Pelanggan (K-Means RFM)   ← Sub-title, 15pt, Teal      │   120×120px  │  │
│   Berbasis Data Transaksi Ritel                                     │              │  │
│                                                                      └──────────────┘  │
│   ┌───────────────────────────────────────────────┐    Caecillia Jessica Kinbenu        │
│   │  METADATA BLOK (kartu transparan,              │    NIM 51230131                    │
│   │  bg #1E293B/60, border 1px gold/30%)           │    Program Studi Teknologi         │
│   │                                                │    Informasi                      │
│   │  Mata Kuliah   : Business Intelligence         │                                   │
│   │  Kegiatan      : Ujian Tengah Semester         │   ▸ Cetak: A4 Portrait            │
│   │  Semester      : 7 (Ganjil 2025/2026)          │                                   │
│   │  Prodi         : Teknologi Informasi           │                                   │
│   │  Objek Studi   : NusaRetail — 18.513 baris     │                                   │
│   └───────────────────────────────────────────────┘                                   │
│                                                                                          │
│ ──────────────────────────────────────────────────────────────────────────────────────── │
│  FOOTER STRIP (#0F172A):  Semester 7 · 2025/2026      |      Dokumen v1.0 · FINAL     │ │ 6%
└──────────────────────────────────────────────────────────────────────────────────────────┘
   ▲ margin 64px                                              kolom 10-12 (foto) ▲ margin 64px
```

---

### 0.3 Spesifikasi Elemen Sampul

**A. Palet Warna Sampul**

| Token | Hex | Peran pada Sampul | Proporsi Area |
|---|---|---|---|
| `cover-navy-deep` | `#0B1220` | Latar header & footer strip | ~24% |
| `cover-navy-base` | `#0F172A` | Latar body utama | ~70% |
| `cover-gold` | `#C9A24B` | Garis rule, penanda metadata, bingkai foto | < 3% |
| `cover-teal` | `#2DD4BF` | Sub-judul, *keyword* data mining | < 2% |
| `cover-white` | `#F8FAFC` | Judul utama, nama penyusun | ~4% |
| `cover-slate` | `#94A3B8` | Label metadata, footer | < 5% |
| `card-glass` | `#1E293B` @ 60% | Kartu blok metadata | — |

**B. Skala Tipografi**

| Elemen | Font | Ukuran | Weight | Letter-spacing | Warna |
|---|---|---|---|---|---|
| Judul Utama | Plus Jakarta Sans / Inter | 34 pt | 800 (Bold) | −1.5% | `#F8FAFC` |
| Sub-judul | Plus Jakarta Sans | 15 pt | 500 | 0 | `#2DD4BF` |
| Eyebrow (label atas judul) | Plus Jakarta Sans | 10 pt | 700 | +18% (uppercase) | `#C9A24B` |
| Label metadata | Plus Jakarta Sans | 10.5 pt | 500 | +6% (uppercase) | `#94A3B8` |
| Nilai metadata | Plus Jakarta Sans | 11.5 pt | 700 | 0 | `#F8FAFC` |
| Nama penyusun | Plus Jakarta Sans | 16 pt | 800 | 0 | `#F8FAFC` |
| Footer | Plus Jakarta Sans | 9 pt | 500 | +8% | `#64748B` |

**C. Grid & Spacing Sampul**

- Kanvas: **A4 Portrait (210 × 297 mm)** · resolusi cetak 300 dpi · rasio layar 1240 × 1754 px.
- Grid: **12 kolom**, *gutter* 24 px, margin luar 64 px.
- Header zone: **22% tinggi halaman** (≈ 386 px).
- Aksen emas: garis horizontal **tebal 4 px** di batas header, dan **1 px** untuk border kartu.
- *Radius*: kartu metadata 12 px, foto 999 px (bulat) atau 16 px (rounded-rectangle).

---

### 0.4 Prototipe HTML/CSS Sampul

> Blok berikut adalah *self-contained prototype* yang dapat langsung dirender di browser untuk pratinjau sampul final.

```html
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<style>
  :root{
    --navy-deep:#0B1220; --navy:#0F172A; --card:#1E293B;
    --gold:#C9A24B; --teal:#2DD4BF; --white:#F8FAFC;
    --slate:#94A3B8;
  }
  *{margin:0;padding:0;box-sizing:border-box;font-family:'Plus Jakarta Sans','Inter',sans-serif}
  body{background:#060A14;display:flex;justify-content:center;padding:32px}
  .cover{width:880px;height:1240px;background:
      linear-gradient(180deg,var(--navy-deep) 0%,var(--navy) 22%,var(--navy) 100%);
      position:relative;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.6)}

  .header{height:272px;padding:56px 64px 0}
  .brand{display:flex;align-items:center;gap:14px;color:var(--gold);
         font-size:11px;font-weight:700;letter-spacing:.22em}
  .brand .dot{width:10px;height:10px;background:var(--gold);border-radius:2px;
              transform:rotate(45deg)}
  .gold-rule{position:absolute;top:272px;left:0;width:100%;height:4px;
             background:linear-gradient(90deg,var(--gold) 0%,var(--gold) 38%,transparent 100%)}

  .body{padding:72px 64px 0;display:grid;grid-template-columns:1fr 200px;gap:40px}
  .eyebrow{color:var(--gold);font-size:11px;font-weight:700;letter-spacing:.3em;
           text-transform:uppercase;margin-bottom:22px}
  h1{color:var(--white);font-size:40px;font-weight:800;line-height:1.12;
     letter-spacing:-.02em}
  h1 .thin{display:block;font-weight:300;color:var(--slate);font-size:30px;margin-top:6px}
  .sub{margin-top:26px;color:var(--teal);font-size:16px;font-weight:500;line-height:1.6}
  .sub b{color:var(--white);font-weight:700}

  .photo{width:172px;height:172px;border-radius:50%;object-fit:cover;
         border:3px solid var(--gold);box-shadow:0 0 0 8px rgba(201,162,75,.12);
         display:block;margin-left:auto}
  .photo-cap{margin-top:16px;text-align:right;color:var(--slate);
             font-size:10px;letter-spacing:.18em;text-transform:uppercase}

  .meta{grid-column:1/2;margin-top:52px;background:rgba(30,41,59,.6);
        border:1px solid rgba(201,162,75,.35);border-radius:12px;
        padding:30px 34px;backdrop-filter:blur(6px)}
  .meta h3{color:var(--gold);font-size:10px;letter-spacing:.26em;
           text-transform:uppercase;margin-bottom:18px}
  .meta .row{display:grid;grid-template-columns:150px 1fr;padding:9px 0;
             border-bottom:1px dashed rgba(148,163,184,.18);font-size:12.5px}
  .meta .row:last-child{border-bottom:none}
  .k{color:var(--slate);letter-spacing:.06em;text-transform:uppercase;font-size:10px;
     align-self:center}
  .v{color:var(--white);font-weight:700}
  .v .teal{color:var(--teal)}

  .author{grid-column:2/3;margin-top:52px;border-left:2px solid var(--gold);
          padding-left:20px;align-self:start}
  .author .nm{color:var(--white);font-size:17px;font-weight:800;line-height:1.3}
  .author .nim{color:var(--gold);font-size:12px;font-weight:700;letter-spacing:.08em;
               margin-top:6px}
  .author .prodi{color:var(--slate);font-size:11px;line-height:1.6;margin-top:10px}

  .stat-strip{position:absolute;bottom:96px;left:64px;right:64px;
              display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
  .stat{background:rgba(15,23,42,.7);border-top:2px solid var(--teal);
        padding:16px 18px;border-radius:8px}
  .stat .n{color:var(--white);font-size:19px;font-weight:800}
  .stat .l{color:var(--slate);font-size:9px;letter-spacing:.16em;
           text-transform:uppercase;margin-top:5px}
  .stat:nth-child(2){border-top-color:var(--gold)}
  .stat:nth-child(3){border-top-color:#38BDF8}
  .stat:nth-child(4){border-top-color:#10B981}

  .footer{position:absolute;bottom:0;left:0;width:100%;height:64px;
          background:var(--navy-deep);display:flex;align-items:center;
          justify-content:space-between;padding:0 64px;
          color:#64748B;font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;
          border-top:1px solid rgba(201,162,75,.25)}
</style>
</head>
<body>
<div class="cover">
  <div class="header">
    <div class="brand"><span class="dot"></span> BUSINESS INTELLIGENCE · LAPORAN UTS</div>
  </div>
  <div class="gold-rule"></div>

  <div class="body">
    <div>
      <div class="eyebrow">Laporan Analisis Sistem &amp; Integrasi Data Mining</div>
      <h1>BUSINESS INTELLIGENCE<br>DASHBOARD
        <span class="thin">Sistem Terintegrasi Analitika Ritel</span></h1>
      <div class="sub">
        Strategi <b>Cross-Selling (Apriori)</b> &amp; Segmentasi Pelanggan
        <b>(K-Means RFM)</b> Berbasis Data Transaksi Ritel
      </div>

      <div class="meta">
        <h3>■ Dokumen Metadata</h3>
        <div class="row"><span class="k">Mata Kuliah</span>
          <span class="v">Business Intelligence</span></div>
        <div class="row"><span class="k">Kegiatan</span>
          <span class="v">Ujian Tengah Semester</span></div>
        <div class="row"><span class="k">Program Studi</span>
          <span class="v">Teknologi Informasi</span></div>
        <div class="row"><span class="k">Semester</span>
          <span class="v">7 · Ganjil 2025/2026</span></div>
        <div class="row"><span class="k">Objek Studi</span>
          <span class="v">NusaRetail · <span class="teal">18.513 transaksi · 30 produk · 1.480 pelanggan</span></span></div>
        <div class="row"><span class="k">Metode</span>
          <span class="v">EDA · RFM · Apriori · K-Means · BI Dashboard</span></div>
      </div>
    </div>

    <div>
      <img class="photo" src="../assets/foto.jpeg" alt="Foto Profil Penyusun">
      <div class="photo-cap">Penyusun</div>
    </div>

    <div class="author">
      <div class="nm">Caecillia<br>Jessica Kinbenu</div>
      <div class="nim">NIM 51230131</div>
      <div class="prodi">Program Studi<br>Teknologi Informasi<br>Semester 7</div>
    </div>
  </div>

  <div class="stat-strip">
    <div class="stat"><div class="n">Rp 696,1 Jt</div><div class="l">Total Revenue</div></div>
    <div class="stat"><div class="n">5.998</div><div class="l">Transaksi</div></div>
    <div class="stat"><div class="n">25 Aturan</div><div class="l">Apriori Rules</div></div>
    <div class="stat"><div class="n">3 Segmen</div><div class="l">K-Means Cluster</div></div>
  </div>

  <div class="footer">
    <span>Semester 7 · Ujian Tengah Semester</span>
    <span>Caecillia Jessica Kinbenu · 51230131</span>
    <span>Dokumen v1.0 — Final</span>
  </div>
</div>
</body>
</html>
```

---

### 0.5 Panduan Tata Letak untuk Desainer (Checklist Produksi)

| # | Instruksi Desain | Nilai Teknis |
|---|---|---|
| 1 | Gunakan bidang **dark navy penuh** di 22% area atas sebagai *authority zone* | `#0B1220` → `#0F172A` (180°) |
| 2 | Pasang **garis emas horizontal 4 px** tepat di batas header | `#C9A24B`, memudar ke transparan setelah 38% lebar |
| 3 | Judul utama **sans-serif tebal** dengan *tight letter-spacing* | 34–40 pt / weight 800 / −2% tracking |
| 4 | Sub-judul memakai aksen **teal** untuk memisahkan ranah "teknis-data" | `#2DD4BF`, 15–16 pt / weight 500 |
| 5 | Blok metadata berupa **kartu kaca** (transparan + border emas tipis) | bg `#1E293B`/60%, border 1 px `#C9A24B`/35% |
| 6 | **Foto profil** ditempatkan kolom kanan (kol. 10–12), bingkai emas, bentuk bulat | 172 px, border 3 px `#C9A24B`, ring cahaya 8 px |
| 7 | Nama & NIM penyusun sebagai **blok signature** dengan *border-left* emas | Border kiri 2 px, NIM warna emas |
| 8 | **Strip statistik** 4 KPI di atas footer untuk kesan berbasis data | Border-top 2 px warna aksen berbeda per kartu |
| 9 | **Footer strip** gelap dengan 3 blok informasi *uppercase* + *letter-spacing* lebar | Tinggi 64 px, 9.5 pt, tracking +16% |
| 10 | Gunakan **grid 12 kolom**, margin 64 px, *gutter* 24 px; jangan pernah menempatkan elemen di luar grid | Radius kartu 12 px, konsisten di seluruh halaman |

---
---
=== BAGIAN 0B ═════════════════════════════════════════════════════════════
## STANDARD UI/UX DESIGN SYSTEM — "DARK EXECUTIVE MODE"
=== BAGIAN 0B ═════════════════════════════════════════════════════════════
---

### 0B.1 Fondasi: Mengapa Dark Executive Mode?

Dashboard BI dibaca dalam dua konteks berbeda: (a) **war-room monitoring** layar besar dengan pencahayaan rendah, dan (b) **review eksekutif** laptop pada rapat. Mode gelap dengan kontras terkontrol mengurangi *visual fatigue* 30–40% pada pemakaian > 30 menit, menonjolkan *data-ink ratio* (elemen data menjadi satu-satunya sumber cahaya layar), dan memposisikan produk sebagai sistem kelas enterprise. Kunci keberhasilannya adalah **disiplin kontras**: teks utama di atas 4.5:1, aksen hanya untuk *signal* (sinyal), bukan dekorasi.

### 0B.2 Token Warna (Color System)

| Token | Hex | Kontras vs `#0F172A` | Peran Fungsional |
|---|---|---:|---|
| `--bg-base` | `#0F172A` | — | Background halaman utama (Slate 900) |
| `--bg-elevated` | `#1E293B` | — | Card / panel (Slate 800) |
| `--bg-inset` | `#0B1220` | — | Sidebar & footer (abyss) |
| `--border-subtle` | `#334155` | — | Divider, border kartu (1 px) |
| `--accent-primary` | `#38BDF8` | 8.6 : 1 | **Sky Blue** — indikator utama, garis tren, fokus user |
| `--accent-secondary` | `#10B981` | 7.4 : 1 | **Emerald** — positif, growth, segmen loyal |
| `--accent-warning` | `#F59E0B` | 9.1 : 1 | Potensi/amber, peringatan sedang |
| `--accent-alert` | `#EF4444` | 4.9 : 1 | **Red** — churn, anomali, penurunan |
| `--accent-gold` | `#C9A24B` | 6.5 : 1 | Highlight eksekutif, ranking #1 |
| `--text-primary` | `#F8FAFC` | 16.4 : 1 | Judul & nilai KPI |
| `--text-secondary` | `#94A3B8` | 7.0 : 1 | Label, sumbu, keterangan |
| `--text-tertiary` | `#64748B` | 4.6 : 1 | Caption, timestamp (min. 14 px) |

**Aturan Aksen (batas penggunaan):** aksen berwarna **maksimal 3 warna per layar**; `#EF4444` hanya muncul bila metrik melanggar ambang; segmen K-Means memakai 3 warna eksklusif `#38BDF8` (Loyal) · `#F59E0B` (Potential) · `#EF4444` (Churn Risk).

### 0B.3 Skala Tipografi

| Level | Ukuran / Line-height | Weight | Penggunaan |
|---|---|---|---|
| Display KPI | 32 / 1.1 | 800 | Angka pada KPI Cards |
| H1 Section | 24 / 1.25 | 700 | Judul halaman/section |
| H2 Widget | 16 / 1.35 | 600 | Judul chart & card |
| Body | 14 / 1.55 | 400 | Narasi, insight text |
| Label | 12 / 1.4 | 600 | Label sumbu, filter, tabel |
| Caption | 11 / 1.4 | 500 | *Footnote*, sumber data |

Font: **Plus Jakarta Sans** (utama) · **JetBrains Mono / SF Mono** (angka tabular pada tabel & KPI agar kolom sejajar).

### 0B.4 Grid 12-Kolom & Hierarki Informasi

```
┌───────────────────────────────────────────────────────────────────────────────┐
│  TOP BAR  (tinggi 56 px)  logo · judul aplikasi · date-range · avatar user    │
├────────────┬──────────────────────────────────────────────────────────────────┤
│            │  ZONA 1 — ORIENTASI (baris 1)                                   │
│  S I D     │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  E         │  │KPI 1   │ │KPI 2   │ │KPI 3   │ │KPI 4   │ │KPI 5   │        │
│  B         │  │Revenue │ │Trx     │ │Pelanggan│ │Avg     │ │Growth  │        │
│  A         │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘        │
│  R   2 kol │                                                                   │
│            │  ZONA 2 — DIAGNOSTIK (baris 2–3)                                 │
│  ┌──────┐  │  ┌──────────────────────────┐  ┌──────────────────────────┐      │
│  │Filter│  │  │ Visualisasi Utama         │  │ Visualisasi Pendamping   │      │
│  │Item  │  │  │ (kol 1–8)                 │  │ (kol 9–12)               │      │
│  │:     │  │  │ Line/Bar trend · Heatmap  │  │ Donut · Ranking · Graph  │      │
│  │Periode│ │  └──────────────────────────┘  └──────────────────────────┘      │
│  │Kategor│ │                                                                   │
│  │Segmen │ │  ZONA 3 — AKSI (baris 4)                                         │
│  │Reset  │ │  ┌──────────────────────────────────────────────────────┐        │
│  └──────┘  │  │ Tabel Detail (drill-down) + Actionable Insights Panel │        │
│            │  └──────────────────────────────────────────────────────┘        │
└────────────┴──────────────────────────────────────────────────────────────────┘
   2 kolom            10 kolom dashboard area (grid-gap 24 px)
```

**Prinsip Hierarki Informasi (Gestalt berbasis bisnis):**

1. **What** (Zona 1) — KPI Cards menjawab *"Apakah bisnis sehat?"* dalam < 3 detik.
2. **Why** (Zona 2) — visualisasi menjawab *"Mengapa angka itu terjadi?"* via tren, komposisi, dan hubungan.
3. **How / So-what** (Zona 3) — tabel + panel insight menjawab *"Apa yang harus saya lakukan?"*.
4. Proses pembacaan dipandu **F-pattern**: mata bergerak KPI (kiri→kanan) → chart besar (kiri) → pendamping (kanan) → aksi (bawah).

### 0B.5 Spesifikasi Komponen Inti

| Komponen | Spesifikasi Teknis | Aturan UX |
|---|---|---|
| **KPI Card** | bg `#1E293B`, radius 16 px, border 1 px `#334155`, padding 20 px, ikon 20 px kiri-atas | Selalu tampilkan **delta vs periode sebelumnya** (▲/▼ + warna), sparkline mini 60×24 px di bawah angka |
| **Chart Panel** | Header (judul + aksi kecil) · Plot area min. 280 px · Footer insight 1 baris italic | Grid line `#334155` @ 40%, tanpa bingkai penuh, *axis label* 11 px `#94A3B8` |
| **Data Table** | Header sticky bg `#0B1220`, baris zebra `#1E293B`/`#172033`, tinggi baris 40 px, angka *tabular-nums* rata kanan | Klik baris = **drill-down**; kolom sort; ekspor CSV |
| **Filter Control** | Select **multi-select** dgn *chip* terpilih, **date-range picker**, toggle segmentasi | Selalu tampilkan **"N filter aktif"** + tombol **Reset**; perubahan memicu *cross-filter* seluruh layar |
| **Insight Panel** | Border-left 3 px aksen, ikon 💡, maksimal 3 kalimat, menyebut angka konkret | Setiap insight wajib berisi **angka + periode + implikasi** |
| **Segment Badge** | Pill radius 999 px, bg aksen @ 15%, teks aksen, 11 px bold | Konsisten warna segmen di seluruh modul (K-Means ↔ Rekomendasi) |

### 0B.6 Micro-interactions & UX Filter

| # | Interaksi | Perilaku Teknis | Nilai UX |
|---|---|---|---|
| 1 | **Dropdown Multi-select** | Pilihan tampil sebagai *removable chip*; state tersimpan di `session_state`; dropdown tidak menutup saat menambah pilihan | Membandingkan ≤ 5 kategori/segmen sekaligus tanpa kehilangan konteks |
| 2 | **Date-Range Picker** | Preset (7H · 30D · QTD · YTD · Custom) + input kalender ganda; memicu *debounce* 300 ms | Satu klik untuk periode berulang yang paling sering dipakai direksi |
| 3 | **Interactive Cross-filtering** | Klik *slice* donut / *point* scatter → seluruh widget lain terfilter otomatis (bidirectional filter) | Menjawab "kalau saya klik segmen X, produk apa yang dominan?" tanpa pindah halaman |
| 4 | **Drill-down capability** | Klik KPI → detail; klik baris tabel → rincian transaksi (breadcrumb navigasi `Semua ▸ Bayi ▸ Susu Formula`) | Turun dari level eksekutif ke level operasional dalam 2 klik |
| 5 | **Hover tooltip terpadu** | Satu komponen tooltip bersama: judul · nilai · satuan · % dari total · delta periode | Konsistensi baca antar-chart, mengurangi beban kognitif |
| 6 | **Hover glow & tran-sisi 150 ms** | `transition: all .15s ease-out`; kartu terangkat 2 px + border aksen saat hover | Umpan balik keterpurukan (*perceived responsiveness*) |
| 7 | **Skeleton loading** | *Shimmer placeholder* mengikuti bentuk konten saat komputasi Apriori/K-Means berjalan | Menghilangkan persepsi "layar beku" pada proses berat |
| 8 | **Undo-able filter** | Ikon ↶ muncul saat filter aktif; klik = kembali ke state sebelumnya | Mencegah pengguna tersesat dalam eksplorasi |

---
---
=== TAHAP 1 ══════════════════════════════════════════════════════════════
## BUSINESS UNDERSTANDING & EXPLORATORY DATA ANALYSIS (EDA)
=== TAHAP 1 ══════════════════════════════════════════════════════════════
---

### 1.1 Permasalahan Bisnis

Objek studi adalah jaringan ritel wilayah NTT dengan **18.513 baris transaksi mentah** sepanjang 2025 yang tersimpan dalam format *spreadsheet* tanpa lapisan analitik. Permasalahan dipetakan ke dalam **3 kelompok akar masalah**:

| # | Kelompok Masalah | Bukti dari Data (terverifikasi) | Dampak Bisnis | Klasifikasi |
|---|---|---|---|---|
| P1 | **Data belum optimal untuk pengambilan keputusan** | Tidak ada tabel fakta tersusun; seluruh metrik harus dihitung manual; tidak ada definisi KPI bersama antar-unit | Keputusan memakai intuisi manajer toko; *reporting* lambat (harian → mingguan) | Strategic |
| P2 | **Dirty data merusak akurasi angka** | **217 duplikat**, **237 sel kosong**, **37 kuantitas tak valid** (−2 s/d 999), **18 harga tak wajar** (−Rp100 s/d Rp999.999), **1.400 inkonsistensi kategori**, **4.543 inkonsistensi metode bayar**, **16 baris `Line_Total` tidak konsisten** dengan rumus hitung | Revenue mentah **Rp 705.156.825** membengkak ~1,3% vs kondisi bersih **Rp 696.085.375**; segmentasi & aturan asosiasi bisa *bias* | Operational |
| P3 | **Lost opportunity terselubung (invisible leakage)** | Basket rata-rata hanya **3,05 produk/transaksi**; **33,6% transaksi hanya membeli ≤ 2 produk** (2.012 dari 5.998, termasuk 485 transaksi 1 produk); **18% pelanggan (266) terindikasi Churn Risk** dengan rata-rata Recency **212 hari** | Cross-sell tidak terarah; tidak ada rekomendasi bundling; pelanggan berharga pergi tanpa program *win-back* | **Revenue Loss — prioritas utama** |
| P4 | **Ketimpangan kontribusi pelanggan tidak terpantau** | **31,1% pelanggan (461) menyumbang 52,9% revenue**; segmen Churn Risk hanya menyumbang 9,3% padahal jumlahnya signifikan | Anggaran pemasaran terdistribusi rata sehingga *wasteful spending* | Tactical |

**Pernyataan Masalah (Problem Statement):**

> *"NusaRetail memiliki basis data transaksi yang cukup besar untuk menghasilkan keputusan berbasis data, namun kualitas data yang buruk, tidak adanya lapisan fitur (RFM/basket), serta tidak adanya sistem dashboard terintegrasi menyebabkan peluang cross-selling tidak teridentifikasi, segmen pelanggan tidak terdiferensiasi, dan 100% keputusan promosi masih berbasis pengalaman subjektif — berpotensi menggerus pertumbuhan revenue tahunan sekitar 10% dari potensi maksimalnya."*

---

### 1.2 Business Questions (Perumusan Pertanyaan Bisnis)

| ID | Pertanyaan Bisnis | Pertanyaan Teknis (Operasionalalisasi) | Metrik Kunci | Tahap Analisis |
|---|---|---|---|---|
| **BQ1** | *Pelanggan mana yang paling berharga dan harus dipertahankan?* | Bagaimana mengelompokkan 1.480 pelanggan berdasarkan perilaku belanja historis? | Segmen (R/F/M), Revenue share per segmen | Tahap 2 & 4 |
| **BQ2** | *Produk mana yang sering dibeli bersamaan sehingga layak ditawarkan bersama?* | Kombinasi produk mana yang muncul bersama secara signifikan secara statistik? | Support, Confidence, Lift | Tahap 3 |
| **BQ3** | *Pelanggan mana yang berisiko berhenti belanja (churn) dan seberapa besar kerugiannya?* | Siapa pelanggan dengan Recency tinggi & Frequency rendah, dan berapa Monetary yang terancam? | Recency > 180 hari, Monetary terancam | Tahap 4 |
| **BQ4** | *Bagaimana tren penjualan setahun dan kapan musim puncak/terendahnya?* | Bagaimana pola bulanan revenue, volume transaksi, dan basket value? | Revenue/bulan, MoM growth, AOV | Tahap 1 |
| **BQ5** | *Strategi promosi mana yang menghasilkan dampak tertinggi dengan biaya terendah?* | Tindakan mana yang paling layak berdasarkan urgensi, biaya, dampak, dan kemudahan? | Skor prioritas, proyeksi uplift | Tahap 6 |
| **BQ6** *(bonus)* | *Rekomendasi produk apa yang tepat untuk tiap segmen pelanggan?* | Bagaimana menggabungkan aturan Apriori dengan profil klaster K-Means? | Rules per segmen, attach rate target | Tahap 5 (integrasi) |

---

### 1.3 Value Creation — Bagaimana Data Mining Mendukung Keputusan Eksekutif

```
        KAPABILITAS DATA MINING          │   KEPUTUSAN EKSEKUTIF YANG DIDUKUNG      │   NILAI BISNIS
    ─────────────────────────────────────┼──────────────────────────────────────────┼─────────────────────────
    EDA & KPI Monitoring   (Descriptif)  │  "Sehatkah penjualan & di mana titik      │  Transparansi real-time,
                                         │   lemahnya?"                              │  baseline objektif
                                         │                                           │
    RFM + K-Means          (Diagnostik)  │  "Siapa yang layak dipertahankan,         │  Biaya akuisisi turun,
    Segmentasi Pelanggan                  │   siapa yang harus dimenangkan kembali?"  │  retensi meningkat
                                         │                                           │
    Apriori                (Preskriptif) │  "Produk apa yang dipasangkan &           │  Basket size naik,
    Association Rules                     │   diletakkan di mana?"                    │  cross-sell terukur
                                         │                                           │
    Integrasi Apriori×K-Means (Preskriptif)│ "Apa penawaran tepat untuk tiap          │  Personalisasi promosi,
                                         │   segmen di periode ini?"                 │  ROI kampanye naik
    ─────────────────────────────────────┴──────────────────────────────────────────┴─────────────────────────
     MATURITAS ANALITIK:  REPORTING  →  DIAGNOSIS  →  PREDIKSI/REKOMENDASI  →  KEPUTUSAN OTOMATIS
                            ▲                                                         ▲
                     kondisi awal NusaRetail                              target transformasi digital
```

**Empat Dimensi Penciptaan Nilai:**

1. **Keputusan berbasis bukti, bukan opini** — setiap rekomendasi pada Tahap 6 dapat ditelusuri (*traceable*) ke angka: lift, confidence, jumlah pelanggan, dan revenue riil.
2. **Alokasi anggaran presisi** — promosi diarahkan ke segmen & kombinasi produk dengan dampak terukur, bukan diskon menyeluruh yang menggerus margin.
3. **Pencegahan *revenue leakage*** — 266 pelanggan Churn Risk (Rp 64,84 juta kontribusi/tahun) dipantau melalui KPI Recency pada dashboard.
4. **Skala keputusan** — satu model berjalan otomatis di dashboard: 5.998 transaksi → 25 aturan → 3 segmen → daftar aksi, tanpa rekap manual.

---

### 1.4 Hasil Eksplorasi Data (EDA)

#### 1.4.1 Struktur Dataset

| Objek | Sheet | Dimensi | Kolom | Peran dalam Sistem |
|---|---|---|---|---|
| Fakta transaksi | `Data_Raw` | **18.513 × 13** | Transaction_ID, Transaction_Date, Customer_ID, Region, Customer_Type, Product_ID, Product_Name, Category, Quantity, Unit_Price, Discount_Rate, Line_Total, Payment_Method | Faktanya (*fact table*) untuk seluruh analisis |
| Dimensi produk | `Data_Produk` | **30 × 4** | Product_ID, Product_Name, Category, Reference_Unit_Price_Rp | Master produk, normalisasi kategori & imputasi harga |
| Dimensi pelanggan | `Data_Pelanggan` | **1.500 × 5** | Customer_ID, Gender_Code, Region, Customer_Type, Age_Group | Enrichment demografi (match rate **99,8%**) |

**Tipe Data & Rentang:**

| Kolom | Tipe | Nilai Kosong (Raw) | Catatan |
|---|---|---:|---|
| `Transaction_ID` | teks | 0 | 6.000 transaksi unik |
| `Transaction_Date` | datetime | 0 | **01 Jan 2025 10:10 – 31 Des 2025 21:50** (12 bulan penuh) |
| `Customer_ID` | teks | 28 | 1.480 pelanggan unik |
| `Region` | teks | 33 | 8 wilayah NTT (Atambua, Biboki, Bikomi, Insana, Kefamenanu, Kupang, Miomaffo, Naibenu) |
| `Customer_Type` | teks | 34 | Member / Non-Member |
| `Product_ID` / `Product_Name` | teks | 26 | 30 SKU aktif |
| `Category` | teks | 0 | 9 kategori (mentah: 12 variasi ejaan) |
| `Quantity` | float | 33 | Rentang anomali −2 s/d **999** |
| `Unit_Price` | float | 18 | Rentang anomali −100 s/d **999.999** |
| `Discount_Rate` | float | 0 | 0% – 15% (rerata 5,04%) |
| `Line_Total` | float | 28 | 16 baris tidak sesuai rumus |
| `Payment_Method` | teks | 37 | Debit · QRIS · Transfer · Tunai (7 variasi ejaan mentah) |

#### 1.4.2 Statistik Deskriptif (Setelah Pembersihan Tahap Awal)

| Metrik | Nilai | Interpretasi Bisnis |
|---|---:|---|
| **Total Revenue (`Line_Total`)** | **Rp 696.085.375** | Basis perhitungan seluruh KPI & uplift |
| Gross sebelum diskon | Rp 733.291.000 | Nilai transaksi sebelum potongan |
| Total diskon terberikan | Rp 37.205.625 (**5,09%**) | Rerata diskon 5,04%, maksimum 15% |
| **Unique Customers** | **1.480** | + 28 baris `Customer_ID` kosong (0,15% baris) |
| **Unique Products** | **30** | Terdistribusi di 9 kategori |
| **Unique Transactions** | **5.998** | dari 6.000 mentah (2 tereduksi akibat duplikasi) |
| **Avg Basket Size** | **3,05 produk/transaksi** (median 3) | Peluang cross-singkat terbesar |
| Avg Basket Value | Rp 116.053/transaksi (median Rp 88.725; P90 Rp 243.013) | *Basket value* kanan-meruncing (*right-skewed*) |
| Avg Nilai per Item Line | Rp 38.100 | Dasar kalkulasi uplift per baris |
| Avg Quantity per baris | 1,91 unit | Mayoritas pembelian 1–2 unit |
| Avg Revenue per Pelanggan | Rp 469.755/tahun | Median Rp 415.900 |

**Distribusi Basket Size (produk unik per transaksi):**

```
 1 produk │████████                        485 trx  ( 8,1%)   ◄ peluang attach tertinggi
 2 produk │█████████████████████████████   1.527 trx (25,5%)
 3 produk │████████████████████████████████████ 1.929 trx (32,2%)  ◄ MODUS (median)
 4 produk │█████████████████████████       1.343 trx (22,4%)
 5 produk │██████████████                   714 trx  (11,9%)
          └──────────────────────────────────────────────
           485 + 1.527 + 1.929 + 1.343 + 714 = 5.998 transaksi
```

#### 1.4.3 Kontribusi Kategori & Produk Teratas

| Rank | Kategori | Revenue | Pangsa | | Rank | Produk Teratas | Revenue | Jml Baris |
|---|---|---:|---:|---|---|---|---:|---:|
| 1 | **Bayi** | Rp 198.336.250 | **28,5%** | | 1 | Susu Formula | Rp 103.877.200 | 642 |
| 2 | **Sembako** | Rp 149.065.300 | **21,4%** | | 2 | Beras Premium 5kg | Rp 92.075.100 | 667 |
| 3 | Rumah Tangga | Rp 81.830.800 | 11,8% | | 3 | Popok Bayi | Rp 73.208.800 | 571 |
| 4 | Minuman | Rp 74.889.975 | 10,8% | | 4 | Telur Ayam 1kg | Rp 35.831.350 | 631 |
| 5 | Makanan | Rp 60.593.075 | 8,7% | | 5 | Lampu LED | Rp 27.342.000 | 558 |
| 6 | Perawatan | Rp 42.211.325 | 6,1% | | 6 | Susu UHT 1L | Rp 24.508.575 | 655 |
| 7 | Elektronik | Rp 40.717.600 | 5,8% | | 7 | Gula Pasir 1kg | Rp 22.870.650 | 763 |
| 8 | Protein | Rp 35.831.350 | 5,1% | | 8 | Sampo 170ml | Rp 22.505.250 | 638 |
| 9 | ATK | Rp 12.609.700 | 1,8% | | 9 | Deterjen 1kg | Rp 21.778.900 | 552 |
| | | | | | 10 | Minyak Goreng 1L | Rp 21.493.300 | 641 |

> **Temuan:** 2 kategori teratas (Bayi + Sembako) menghasilkan **49,9% revenue** — 50% pasar berasal dari separuh kategori (*Pareto terbalik 80/20 ≈ 60/40*). Catatan penting: **ATK berada di posisi terendah berdasarkan revenue (1,8%) tetapi muncul sebagai pasangan asosiasi terkuat** (Pulpen → Buku Tulis) — bukti bahwa revenue rendah ≠ peluang cross-sell rendah.

#### 1.4.4 Tren Bulanan (Basis BQ4)

| Bulan | Revenue | Trx | Basket Value | MoM |
|---|---:|---:|---:|---:|
| Jan 2025 | Rp 57.185.675 | 517 | Rp 110.611 | — |
| Feb 2025 | Rp 55.901.175 | 469 | Rp 119.192 | −2,2% |
| Mar 2025 | Rp 62.104.925 | 510 | Rp 121.774 | +11,1% |
| Apr 2025 | **Rp 51.740.775** | 465 | Rp 111.270 | −16,7% ▼ *terendah* |
| Mei 2025 | Rp 56.640.275 | 498 | Rp 113.735 | +9,5% |
| Jun 2025 | Rp 56.425.100 | 484 | Rp 116.581 | −0,4% |
| Jul 2025 | Rp 59.019.000 | 502 | Rp 117.568 | +4,6% |
| Agu 2025 | Rp 57.495.250 | 517 | Rp 111.209 | −2,6% |
| Sep 2025 | Rp 55.205.325 | 469 | Rp 117.709 | −4,0% |
| **Okt 2025** | **Rp 65.180.225** | 528 | Rp 123.447 | **+18,1% ▲ puncak** |
| Nov 2025 | Rp 56.760.625 | 513 | Rp 110.644 | −13,0% |
| Des 2025 | Rp 62.427.025 | 526 | Rp 118.683 | +10,0% |

```
Revenue bulanan (Rp juta)
66 ┤                                        ╭╮
64 ┤                                     ╭──╯╰──╮
62 ┤        ╭╮                        ╭──╯      ╰╮        ╭╮
60 ┤        ╰╯    ╭╮                 ╰╯          ╰╮       ╰╯
58 ┤   ╭╮    ╭╮ ╭╮╰╮   ╭╮   ╭╮  ╭╮ ╭╮            ╰╮ ╭╮ ╭╮╰╮
56 ┤  ╭╯╰╮╭╮╯╰╮╯╰╮╰╮ ╭╯╰╮ ╭╯╰╮ ╰╮╰╮││            ╰╮╯╰╮││ ╰╮
54 ┤──╯   ╰╯   ╰   ╰─╯   ╰─╯   ╰──╰─╯╰╯            ╰╯  ╰╯   ╰──
52 ┤                                          ╰╮
   └──┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──
     Jan Feb Mar Apr Mei Jun Jul Agu Sep Okt Nov Des
   Rerata: Rp 58,0 juta/bulan · Volatilitas (CV): 7,0% · Puncak Okt (+12,4% vs rerata)
```

**Temuan EDA Lain:**

- **Pola hari:** Sabtu tertinggi **Rp 107,18 juta**, Rabu Rp 104,01 juta, Minggu terendah **Rp 92,28 juta** → peluang *weekend campaign*.
- **Wilayah:** Bikomi (Rp 98,28 jt), Miomaffo (Rp 93,47 jt), Insana (Rp 89,47 jt) — 3 wilayah teratas menyumbang 40,5%.
- **Metode bayar merata:** Transfer 25,6% · Tunai 25,3% · Debit 24,9% · QRIS 24,0% → tidak ada ketergantungan pada satu kanal.
- **Demografi (join master, match 99,8%):** Gender hampir seimbang (L 765 / P 735); kelompok usia 18–25 tertinggi (Rp 147,56 jt), >55 (Rp 145,16 jt) → pasar lintas-usia.
- **Outlier musiman:** tidak ditemukan *spike* tak wajar; seluruh bulan berada di rentang Rp 51,7–65,2 juta (data stabil, aman untuk pemodelan).

#### 1.4.5 Temuan Awal Kualitas Data (Data Quality Findings)

| Temuan | Jumlah | Severity | Bukti | Dampak jika Diabaikan |
|---|---:|---|---|---|
| Duplikat baris | **217** | 🔴 High | 216 identik persis + 1 akibat normalisasi spasi | Revenue & support terdistorsi |
| Sel kosong | **237** | 🔴 High | Customer_ID 28 · Region 33 · Customer_Type 34 · Product_ID 26 · Quantity 33 · Unit_Price 18 · Line_Total 28 · Payment_Method 37 | Baris tak terpakai / error agregasi |
| Quantity tak valid | **37** | 🔴 High | 26 baris ≤ 0 (termasuk −2) · 11 baris ≥ 100 (maks 999) | Mean qty membengkak 2,5 → 1,91 |
| Harga tak wajar | **18** | 🔴 High | 13 baris ≤ 0 (−Rp100) · 5 baris > Rp500.000 (maks Rp999.999) | Revenue mentah lebih besar Rp 9,07 juta |
| Inkonsistensi kategori | **1.400** | 🟡 Medium | `SEMBAKO/Sembako/Sembako␣/sembako` | Kategori ≠ katalog → analisis per kategori bocor |
| Inkonsistensi metode bayar | **4.543** | 🟡 Medium | `QRIS/QRIS␣/Qris/qris` | Pengelompokan pembayaran terpecah |
| `Line_Total` tak sesuai rumus | **16** | 🟡 Medium | Selisih > 1% dari `Qty × Harga × (1−Diskon)` | Selisih Rp 8,5 juta vs basis bersih |
| Baris tanpa `Product_ID` | **26** | 🔴 High | Kunci relasi ke dimensi produk hilang | Tak bisa dianalisis (buang) |
| Duplikat residu pasca-imputasi | **1** | 🟢 Low | Dua baris kembali identik setelah imputasi median | Dibersihkan pada *drop final* |

---
---
=== TAHAP 2 ══════════════════════════════════════════════════════════════
## DATA PREPROCESSING & FEATURE ENGINEERING
=== TAHAP 2 ══════════════════════════════════════════════════════════════
---

**Prinsip Pemrosesan:** *Deterministic, Auditable, Reversible* — setiap transformasi dapat ditelusuri ke aturan tertulis, dapat dijalankan ulang dengan hasil identik, dan tidak menghapus informasi tanpa dokumentasi.

### 2.1 Cleaning & Imputation Strategy

| # | Masalah | Metode Penanganan | Alasan Pemilihan (argumentasi bisnis/teknis) |
|---|---|---|---|
| C1 | **Missing `Product_ID` (26 baris)** | **Drop row** (*listwise deletion*) | Kunci relasi hilang → baris tidak dapat diatribusikan ke produk mana pun; 0,14% dari data (dampak < 0,05% revenue) |
| C2 | **Missing `Quantity`/`Unit_Price` (33/18)** | **Imputasi median** qty (modus data=2) & **imputasi harga katalog** `Data_Produk` | Median lebih tahan terhadap outlier dibanding mean; harga katalog adalah *ground truth* bisnis (bukan tebakan statistik) |
| C3 | **Missing `Customer_ID` (28 baris)** | Isi konstanta **`UNKNOWN`** → **dikecualikan dari model RFM**, tetap dipertahankan untuk analisis produk/revenue | Menjaga 848.625 revenue tidak hilang, sambil mencegah "pelanggan hantu" merusak klasterisasi |
| C4 | **Missing `Region`/`Customer_Type`/`Payment_Method`** | Isi **"Tidak Diketahui"** sebagai kategori eksplisit | Kategori eksplisit ≠ data hilang: angka kecil (1,1 jt) tetap terlihat di dashboard alih-alih disembunyikan |
| C5 | **Duplikat 217 baris** | **`drop_duplicates()`** *setelah* normalisasi teks | Duplikat "tersembunyi" baru terdeteksi setelah `Sembako␣` → `Sembako`; jika dibersihkan sebelum normalisasi, 1 duplikat lolot |
| C6 | **Quantity ≤ 0 / ≥ 100 (37 baris)** | **Imputasi median** dari populasi valid (0 < qty < 100) | Retur/kesalahan input tak bisa dipisahkan dari data → median menjaga distribusi tanpa memindahkan pusat data |
| C7 | **Unit_Price ≤ 0 / > Rp500.000 (18 baris)** | Ganti dengan **harga katalog**; jika SKU tak dikenal → median global | Harga negatif/Rp999.999 adalah *keying error*; harga katalog menjamin margin calculation valid |
| C8 | **Inkonsistensi teks kategori (1.400) & bayar (4.543)** | `str.strip()` + `.title()` + **mapping ke katalog produk** + *alias* (`Qris → QRIS`) | Kategori produk **mengikuti dimensi produk sebagai *golden source*** (mencegah konflik sumber kebenaran) |
| C9 | **`Line_Total` tak konsisten (16 baris)** | **Hitung ulang** `Qty × Unit_Price × (1 − Discount_Rate)` di SEMUA baris | Rekonsiliasi menyeluruh lebih konsisten daripada membetulkan per-baris yang terdeteksi saja |
| C10 | **Duplikat residu pasca-imputasi (1 baris)** | *Final drop* pada langkah penutup pipeline | Imputasi membuat dua baris identik; dibersihkan agar agregasi tidak menghitung ganda |

**Alur Pipeline Pembersihan:**

```
 Data_Raw (18.513)
    │
    ├─(1) Normalisasi teks: strip(), Title Case, alias QRIS, mapping kategori ← Data_Produk
    ├─(2) Drop baris tanpa Product_ID (−26)
    ├─(3) Drop duplikat hasil normalisasi (−217)
    ├─(4) Imputasi: Quantity ← median · Unit_Price ← harga katalog · ID/Wilayah ← konstanta
    ├─(5) Rekonsiliasi Line_Total = Qty × Harga × (1 − Diskon)
    ├─(6) Drop baris gagal validasi (−0) + final dedup (−0..1)
    ▼
 Data_Clean (18.270 × 14)  ──[tambah basket_size]──►  18.270 × 14
    ├─► basket / matriks transaksi :  5.998 × 30   (basis Apriori)
    └─► agregasi per pelanggan     :  1.480 baris  (basis RFM/K-Means)
```

---

### 2.2 Feature Engineering

#### 2.2.1 Matriks RFM (Recency · Frequency · Monetary)

**Definisi & Formulasi:**

```
  Tanggal Acuan (t_ref)  =  max(Transaction_Date) + 1 hari  =  01 Januari 2026

  Recency   (R)  =  t_ref  −  tanggal transaksi terakhir pelanggan i      [hari]
  Frequency (F)  =  jumlah Transaction_ID unik milik pelanggan i          [transaksi]
  Monetary  (M)  =  Σ Line_Total seluar baris milik pelanggan i           [Rp]
```

**Contoh Kalkulasi Nyata (transparansi perhitungan):**

```
  Pelanggan C0001 (join: L · Kefamenanu · Non-Member · 26-35)
    Transaksi terakhir : 27 Nov 2025  → R = 01 Jan 2026 − 27 Nov 2025 = 35 hari
    Jumlah transaksi   : 4 trx (T001307, T001571, T003342, T004996) → F = 4
    Σ Line_Total       : Rp 324.125   → M = Rp 324.125
    => vektor RFM = (35, 4, 324.125)
```

**Distribusi RFM (n = 1.480 pelanggan, eksklusif `UNKNOWN`):**

| Statistik | Recency (hari) | Frequency (trx) | Monetary (Rp) |
|---|---:|---:|---:|
| Minimum | 1 | 1 | 3.600 |
| Q1 | 25,75 | 3 | 243.650 |
| **Median** | **60** | **4** | **415.900** |
| Mean | 83,46 | 4,05 | 469.755 |
| Q3 | 121 | 5 | 636.081 |
| Maksimum | 363 | 13 | 2.220.850 |
| Std Dev | 75,58 | 1,92 | 298.157 |

> **Interpretasi:** Median R = 60 hari menunjukkan separuh pelanggan terakhir belanja > 2 bulan sebelum periode berakhir; F terkumpul rapat di 3–5 (rentang sempit, std 1,92) → **K-Means harus mengandalkan kombinasi ketiga fitur**, karena Frequency sendiri berdiskriminasi rendah. Skew distribusi Monetary (mean > median, ekor kanan) menegaskan perlunya **standardisasi + interpretasi segmen berbasis median**.

#### 2.2.2 Fitur `basket_size`

```
  basket_size(Transaction_ID)  =  COUNT(DISTINCT Product_ID) per transaksi

  Contoh : TRX-000432 memuat {P001 Beras, P002 Minyak, P029 Pulpen}  → basket_size = 3
```

| Ukuran Basket | 1 | 2 | 3 | 4 | 5 | **Rerata** |
|---|---:|---:|---:|---:|---:|---:|
| Jumlah transaksi | 485 | 1.527 | **1.929** | 1.343 | 714 | **5.998** |
| Pangsa | 8,1% | 25,5% | 32,2% | 22,4% | 11,9% | **3,05 item** |

> **Nilai bisnis:** 1.527 transaksi 2-item + 485 transaksi 1-item = **33,6% transaksi berada di bawah rata-rata** → inilah populasi target *attach rate* (KPI Tahap 6).

#### 2.2.3 Transformasi ke Format Binary One-Hot / Basket Format (untuk Apriori)

```
  LONG FORMAT (Data_Clean)              BINARY BASKET MATRIX (transaksi × produk)
  ────────────────────────               ──────────────────────────────────────
  TRX-01 │ P001 │ qty 2 │              TRX-01 │ P001 │ P002 │ P003 │ ... │ P030 │
  TRX-01 │ P002 │ qty 1 │              ───────┼──────┼──────┼──────┼─────┼──────│
  TRX-02 │ P001 │ qty 1 │              TRX-01 │  1   │  1   │  0   │ ... │  0   │
  TRX-02 │ P005 │ qty 2 │        ──►   TRX-02 │  1   │  0   │  0   │ ... │  0   │
  TRX-03 │ P029 │ qty 1 │              TRX-03 │  0   │  0   │  0   │ ... │  1   │
  TRX-03 │ P030 │ qty 1 │                   ... (5.998 baris × 30 kolom)
  ...                                    ────── margin of error: nilai ∈ {0,1}
                                         Sparsity = 89,85% (wajar untuk market basket)
```

- **Satuan observasi diubah** dari *baris item* (18.270) menjadi *transaksi* (**5.998**) — inilah yang menurunkan volume sekaligus menjadi *unit of analysis* Apriori.
- Nilai **1** = produk pernah muncul dalam transaksi (kemunculan ganda tetap 1 — sesuai definisi *support* klasik Agrawal & Srikant).

---

### 2.3 Standardisasi Data untuk K-Means

| Keputusan | **`StandardScaler` (z-score)** | Min-Max Scaling | Robust Scaling |
|---|---|---|---|
| Rumus | z = (x − μ) / σ | x′ = (x − min)/(max − min) | (x − median)/IQR |
| Dipilih | ✅ **YA** | ⛔ | ⛔ |
| Alasan | Menstandarkan ke **mean 0, std 1** → ketiga fitur RFM berkontribusi **setara** pada jarak Euclidean | Rentang Monetery (Rp 3.600–2,2 jt) akan mendominasi jarak bila hanya diskalakan 0–1; outlier tetap mengunci skala | Lebih tahan outlier, tetapi K-Means pada data RFM ini (std terkendali setelah pembersihan) tidak membutuhkannya |

**Justifikasi teknis terukur:**

```
  SEBELUM standardisasi (skala asli):
     Recency    : mean  83,5  |  std  75,6   ┐
     Frequency  : mean   4,05 |  std   1,92  ├─ rasio std tertinggi: Monetary ≈ 3.900× Frequency
     Monetary   : mean 469.755|  std 298.157 ┘   ⇒ Monetary menguasai 99,99% jarak Euclidean

  SESUDAH StandardScaler:
     Recency    : mean 0.00 | std 1.00  ┐
     Frequency  : mean 0.00 | std 1.00  ├─ kontribusi jarak seimbang 1 : 1 : 1
     Monetary   : mean 0.00 | std 1.00  ┘
```

> **Konsekuensi jika tidak discaling:** seluruh klaster hanya akan memisahkan pelanggan kaya-miskin; dimensi perilaku (sering belanja / baru) hilang → segmen "Churn Risk" tidak akan pernah terbentuk.

---

### 2.4 Data Scalability Strategy

| Strategi | Implementasi | Kapan Dipakai | Kapasitas yang Ditangani |
|---|---|---|---|
| **1. Agregasi Awal (utama)** | Fakta 18.270 baris langsung diagregat ke **5.998 basket** (Apriori) & **1.480 baris RFM** (K-Means) | Selalu — jalur produksi saat ini | Volume model turun **92,1%** (Apriori) dan **99,2%** (K-Means) |
| **2. Chunking** | Baca Excel/CSV per potongan 50.000 baris (`chunksize`), agregasi parsial per chunk lalu digabung | Saat file > 1 juta baris / RAM < 8 GB | Memori tetap konstan O(chunk), bukan O(n) |
| **3. Stratified Sampling** | Sampel berimbang per bulan × kategori (mis. 30% per strata) untuk eksplorasi | *Prototyping* aturan baru dalam hitungan detik | Pola musiman & proporsi kategori terjaga (bukan sampel acak yang bias) |
| **4. Pruning Apriori** | `min_support` 2% memangkas itemset sejak L1; `max_len = 3` membatasi ruang kombinasi (30 → 435 pasangan → maks 4.060 triplet) | Selalu | Kompleksitas turun eksponensial |
| **5. K-Means di ruang fitur 3D** | Hanya 3 fitur (R/F/M) × 1.480 baris → `n_init=10`, konvergen < 22 iterasi | Selalu | K-Means linear terhadap n — aman hingga ratusan ribu pelanggan |
| **6. Materialisasi & Cache** | Matriks & hasil model disimpan sebagai artefak (CSV/parquet) + cache lapisan aplikasi | Agar interaksi filter tidak menghitung ulang | Latensi dashboard < 1 dtk (model hanya dihitung saat parameter berubah) |

---

### 2.5 Data Audit Table — Sebelum vs Sesudah Preprocessing

| # | Aspek yang Diaudit | **Sebelum** | **Sesudah** | Metode Perubahan | Status |
|---|---|---:|---:|---|---|
| 1 | Jumlah baris | **18.513** | **18.270** | −26 tanpa produk, −217 duplikat (setelah normalisasi), sisanya lolos validasi | ✅ |
| 2 | Jumlah kolom | 13 | **14** | +`basket_size` (feature engineering) | ✅ |
| 3 | Sel kosong (missing) | **237** | **0** | Drop 26 · Imputasi 51 · Fill kategori 132 · hitung ulang 28 | ✅ |
| 4 | Baris duplikat | **217** | **1 residu** → **0** *(final dedup)* | `drop_duplicates()` dua tahap | ⚠️ → ✅ |
| 5 | Quantity tak valid (≤0 / ≥100) | **37** | **0** | Imputasi median populasi valid | ✅ |
| 6 | Harga tak wajar (≤0 / >500rb) | **18** | **0** | Imputasi harga katalog | ✅ |
| 7 | `Line_Total` tak konsisten | **16** | **0** | Rekonsiliasi formula menyeluruh | ✅ |
| 8 | Inkonsistensi kategori | **1.400** | **0** | Trim + Title Case + mapping katalog | ✅ |
| 9 | Inkonsistensi metode bayar | **4.543** | **0** | Normalisasi + alias `Qris→QRIS` | ✅ |
| 10 | Transaksi unik | 6.000 | **5.998** | Deduplikasi transaksi identik | ✅ |
| 11 | Pelanggan teridentifikasi | 1.480 | **1.480** (28 baris `UNKNOWN` dieksekutasi model) | *Exclusion rule* RFM | ✅ |
| 12 | Produk unik | 30 | **30** | Tidak ada SKU terbuang | ✅ |
| 13 | Total revenue | Rp 705.156.825 *(raw, ter-bias)* | **Rp 696.085.375** *(clean)* | Selisih Rp 9.071.450 (−1,30%) akibat outlier & duplikat | ✅ |
| 14 | Mean Quantity | 2,50 (ter-bias outlier 999) | **1,91** | Outlier terimputasi | ✅ |
| 15 | Rentang tanggal | 01 Jan – 31 Des 2025 | 01 Jan – 31 Des 2025 | Tidak ada data terbuang pada dimensi waktu | ✅ |
| 16 | Matriks Apriori (baris × kolom) | — | **5.998 × 30** (sparsity 89,85%) | Pivot binary one-hot | ✅ |
| 17 | Tabel RFM | — | **1.480 × 4** (C_ID, R, F, M) | Agregasi per pelanggan | ✅ |

---
---
=== TAHAP 3 ══════════════════════════════════════════════════════════════
## MARKET BASKET ANALYSIS — ALGORITMA APRIORI
=== TAHAP 3 ══════════════════════════════════════════════════════════════
---

**Input:** matriks biner `5.998 transaksi × 30 produk` (sparsity 89,85%).
**Rumus Metrik:**

```
  Support (X→Y)    =  |X ∩ Y| / N                 ← seberapa sering kombinasi muncul
  Confidence (X→Y) =  Support(X∩Y) / Support(X)    ← prob Y saat X dibeli
  Lift (X→Y)       =  Confidence(X→Y) / Support(Y) ← 1 = independen; >1 = saling menarik
  Leverage (X→Y)   =  Support(X∩Y) − Support(X)·Support(Y)  ← keuntungan absolut vs kebetulan
```

### 3.1 Parameter Setup — Justifikasi Ambang

| Parameter | Nilai Terpilih | Alasan Berbasis Data (bukan asumsi) |
|---|---:|---|
| **Minimum Support** | **0,02 (2%)** = 120 transaksi | **Pembuktian empiris:** *support* maksimum pasangan produk teramati hanya **4,05%** (Pulpen+Buku Tulis). Ambang 5% → **0 itemset ukuran-2, 0 aturan** (seluruh analisis kosong); ambang 1% → melonjak ke 93 itemset dengan banyak aturan lemah. Titik 2% menangkap **14 pasangan signifikan** tanpa aturan sampah — *sweet spot* berbasis sebaran data, bukan konvensi. |
| **Minimum Confidence** | **0,20 (20%)** | Dalam 28 kandidat aturan directional, **4 aturan mencapai ≥30%** dan **sebaran median ≈ 21%**. Ambang 30% hanya menyisakan 4 aturan (kehilangan 86% informasi); ambang 10% menyertakan aturan yang tak layak ditindaklanjuti. 20% = ambang minimum "layak dipromosikan" (1 dari 5 pelanggan yang membeli X ikut membeli Y). |
| **Minimum Lift** | **1,05** (evaluasi terpisah di 1,00–3,00) | Lift > 1 = ketergantungan positif (bukan kebetulan). Data menunjukkan **seluruh 25 aturan memiliki lift 1,927–3,209 (rata-rata 2,319)** — jauh di atas ambang, sehingga fungsi lift di sini lebih berperan sebagai *guardrail* anti-korelasi semu ketika parameter diturunkan pengguna. |
| **Ukuran itemset maksimal** | **k = 3** | Ruang kombinasi C(30,3) = 4.060; dengan pruning Apriori (setiap subset harus frequent) hanya 44 itemset lolos pada k≤2. Membatasi k=3 menjaga interpretabilitas bundling (maks 3 produk wajar dalam 1 paket). |
| **Ranking aturan** | Skor = 0,5·Lift + 0,3·Confidence + 0,2·Support | Lift diberi bobot tertinggi karena paling menentukan *additive value* promosi; confidence menangkap kepastian; support menjaga basis transaksi tetap material. |

**Pembuktian sensitivitas (dijalankan pada data ini):**

| min_support | min_confidence | Frequent Itemsets | Aturan Dihasilkan | Penilaian |
|---:|---:|---:|---:|---|
| 0,05 | 0,20 | 30 (hanya L1) | **0** | ❌ Terlalu ketat — analisis mati |
| 0,02 | 0,20 | **44** (30 L1 + 14 L2) | **25** | ✅ **Terpilih — seimbang** |
| 0,015 | 0,20 | 44 | 25 | Tidak menambah aturan (stabil) |
| 0,010 | 0,20 | 93 | 25 | Menambah 49 itemset lemah, aturan tidak bertambah |

> **Insight parameter:** kurva aturan **jenuh pada 2%** — menurunkan support ke 1% hanya memperkaya *itemset* tanpa menghasilkan aturan baru, yang membuktikan ambang 2% sudah berada di **titik efisiensi maksimum**.

---

### 3.2 Frequent Itemsets & Rules Generation

#### 3.2.1 Frequent Itemsets Teratas

**Itemset Ukuran-1 (Single Items) — Top 12 dari 30:**

| # | Produk | Support | Basis Transaksi |
|---|---|---:|---:|
| 1 | Gula Pasir 1kg | **12,72%** | 763 trx |
| 2 | Buku Tulis | **12,45%** | 747 trx |
| 3 | Beras Premium 5kg | 11,12% | 667 trx |
| 4 | Pembersih Piring | 10,95% | 657 trx |
| 5 | Pasta Gigi | 10,94% | 656 trx |
| 6 | Susu UHT 1L | 10,92% | 655 trx |
| 7 | Bubur Bayi | 10,90% | 654 trx |
| 8 | Susu Formula | 10,70% | 642 trx |
| 9 | Pewangi Pakaian | 10,69% | 641 trx |
| 10 | Minyak Goreng 1L | 10,69% | 641 trx |
| 11 | Sampo 170ml | 10,64% | 638 trx |
| 12 | Telur Ayam 1kg | 10,52% | 631 trx |

**Itemset Ukuran-2 (Frequent Pairs) — Lengkap 14 dari 14:**

| # | Pasangan Produk | Support | Transaksi |
|---|---|---:|---:|
| 1 | **Pulpen + Buku Tulis** | **4,05%** | 243 |
| 2 | **Beras Premium 5kg + Minyak Goreng 1L** | **3,78%** | 227 |
| 3 | Minyak Goreng 1L + Gula Pasir 1kg | 2,92% | 175 |
| 4 | Beras Premium 5kg + Gula Pasir 1kg | 2,73% | 164 |
| 5 | Mi Instan + Kopi Bubuk | 2,38% | 143 |
| 6 | Popok Bayi + Susu Formula | 2,35% | 141 |
| 7 | Deterjen 1kg + Pembersih Piring | 2,27% | 136 |
| 8 | Sabun Mandi + Pasta Gigi | 2,20% | 132 |
| 9 | Sabun Mandi + Sampo 170ml | 2,15% | 129 |
| 10 | Roti Tawar + Telur Ayam 1kg | 2,12% | 127 |
| 11 | Mi Instan + Air Mineral 600ml | 2,10% | 126 |
| 12 | Deterjen 1kg + Pewangi Pakaian | 2,08% | 125 |
| 13 | Susu UHT 1L + Roti Tawar | 2,02% | 121 |
| 14 | Popok Bayi + Bubur Bayi | 2,00% | 120 |

#### 3.2.2 Tabel Top 10 Association Rules

**Ringkasan:** 14 itemset pasangan → 28 kandidat aturan directional → **25 aturan lolos** (3 gagal ambang confidence) · **21 aturan lift ≥ 2,0** · 4 aturan confidence ≥ 30%.

| # | Antecedent (X) | Consequent (Y) | Support | Confidence | Lift | Leverage |
|---|---|---|---:|---:|---:|---:|
| 1 | **Pulpen** | **Buku Tulis** | 4,05% | **39,97%** | **3,209** | 0,0279 |
| 2 | **Buku Tulis** | **Pulpen** | 4,05% | 32,53% | **3,209** | 0,0279 |
| 3 | **Minyak Goreng 1L** | **Beras Premium 5kg** | 3,78% | 35,41% | **3,185** | 0,0260 |
| 4 | **Beras Premium 5kg** | **Minyak Goreng 1L** | 3,78% | 34,03% | **3,185** | 0,0260 |
| 5 | Mi Instan | Kopi Bubuk | 2,38% | 25,04% | 2,450 | 0,0141 |
| 6 | Kopi Bubuk | Mi Instan | 2,38% | 23,33% | 2,450 | 0,0141 |
| 7 | Popok Bayi | Susu Formula | 2,35% | 24,69% | 2,307 | 0,0133 |
| 8 | Susu Formula | Popok Bayi | 2,35% | 21,96% | 2,307 | 0,0133 |
| 9 | Deterjen 1kg | Pembersih Piring | 2,27% | 24,64% | 2,249 | 0,0126 |
| 10 | Pembersih Piring | Deterjen 1kg | 2,27% | 20,70% | 2,249 | 0,0126 |

**Aturan 11–25 (kualifikasi lanjutan):**

| Aturan | Sup. | Conf. | Lift | | Aturan | Sup. | Conf. | Lift |
|---|---:|---:|---:|---|---|---:|---:|---:|
| Minyak Goreng → Gula Pasir | 2,92% | 27,30% | 2,146 | | Sabun Mandi → Sampo | 2,15% | 22,79% | 2,143 |
| Gula Pasir → Minyak Goreng | 2,92% | 22,94% | 2,146 | | Sabun Mandi → Pasta Gigi | 2,20% | 23,32% | 2,132 |
| Mi Instan → Air Mineral | 2,10% | 22,07% | 2,135 | | Sampo → Sabun Mandi | 2,15% | 20,22% | 2,143 |
| Deterjen → Pewangi Pakaian | 2,08% | 22,64% | 2,119 | | Air Mineral → Mi Instan | 2,10% | 20,32% | 2,135 |
| Pasta Gigi → Sabun Mandi | 2,20% | 20,12% | 2,132 | | Roti Tawar → Telur Ayam | 2,12% | 22,16% | 2,107 |
| Telur Ayam → Roti Tawar | 2,12% | 20,13% | 2,107 | | Beras → Gula Pasir | 2,73% | 24,59% | 1,933 |
| Gula Pasir → Beras | 2,73% | 21,49% | 1,933 | | Roti Tawar → Susu UHT | 2,02% | 21,12% | 1,934 |
| Popok Bayi → Bubur Bayi | 2,00% | 21,02% | 1,927 | | | | | |

**Interpretasi 3 Aturan Teratas:**

1. **Pulpen → Buku Tulis (lift 3,21 / conf 40,0%)** — pelanggan yang membeli pulpen **3,2× lebih mungkin** membeli buku tulis dibanding pembeli acak. Ini aturan dengan *confidence* tertinggi: **2 dari 5 pembeli pulpen langsung mengambil buku tulis.** Kelas ATK hanya menyumbang 1,8% revenue, tetapi aturan ini terkuat → *traffic driver* kecil yang berpotensi menaikkan basket pelajar/pegawai.
2. **Minyak Goreng → Beras Premium (lift 3,19 / conf 35,4%)** — inti belanja bulanan rumah tangga. Dengan nilai baris Beras rata-rata **Rp 138.044**, konversi tambahan 5 pp pada 641 pembeli minyak menghasilkan ~Rp 4,4 juta/tahun (lihat model uplift Tahap 6).
3. **Popok Bayi → Susu Formula (lift 2,31 / conf 24,7%)** — pasangan kategori **Bayi (28,5% revenue)** dengan *nilai baris tertinggi* (**Rp 161.802**). Ini aturan dengan nilai ekonomi per konversi terbesar.

---

### 3.3 Interpretasi & Visualisasi UI/UX

#### 3.3.1 Network Graph — "Association Constellation"

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  ATURAN ASOSIASI — NETWORK VIEW     [ukuran node = support · tebal edge = lift]      │
│  ● Angka pada edge = LIFT (semua nilai terverifikasi dari 25 aturan aktif)            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│        KOMUNITAS SEMBAKO (inti belanja bulanan)                                     │
│                                                                                     │
│           [Minyak Goreng]══3,19══[Beras Premium 5kg]                                │
│               │  ╲                        ║                                        │
│             2,15 ╲  ╲ lift                 ║ 1,93                                   │
│                   ╲  ╲ support 2,92%       ║                                        │
│           [Gula Pasir 1kg]═════════════════╝                                        │
│                                                                                     │
│        [Pulpen]══3,21══[Buku Tulis]        ◄ LIFT TERTINGGI (support 4,05%)         │
│                                                                                     │
│  ┌ KOMUNITAS RUMAH TANGGA ──────────┐ ┌ KOMUNITAS BAYI ────────┐ ┌ SARAPAN ──────┐│
│  │[Deterjen]──2,25──[Pembersih]     │ │[Popok]──2,31──[Susu    │ │[Mi]──2,45──   ││
│  │[Sabun]────2,14──[Sampo]          │ │       Formula]         │ │     [Kopi]    ││
│  │[Sabun]────2,13──[Pasta Gigi]     │ │[Popok]──1,93──[Bubur   │ │[Mi]────2,14── ││
│  │[Deterjen]─2,12──[Pewangi]        │ │       Bayi]            │ │    [Air Min.] ││
│  └──────────────────────────────────┘ └────────────────────────┘ │[Roti]─2,11──  ││
│  ▲ klik cluster → cross-filter            ▲ nilai baris terbesar│    [Telur Ayam]││
│    ke tabel produk & segmen K-Means        di komunitas ini      └────────────────┘│
├─────────────────────────────────────────────────────────────────────────────────────┤
│  LEGENDA:  ═══ lift ≥ 3,0 (sangat kuat)   ─── lift 2,0–2,9 (kuat)   ── lift < 2,0  │
│  INTERAKSI: klik node → isolasi hubungan · hover → tooltip (support/conf/lift)      │
│             klik komunitas → filter dashboard · toggle arah panah on/off            │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

**Spesifikasi visual:** node memakai warna kategori (9 kategori dari palet desain), *edge weight* dipetakan ke lebar garis 1–6 px, *force-directed layout* (Fruchterman-Reingold), *self-loops* dimatikan, panah directional hanya ditampilkan bila kedua arah lolos ambang berbeda.

#### 3.3.2 Heatmap "Cross-Selling Matrix" (Matriks Interaktif)

```
   LIFT PASANGAN (matriks simetris — lift(X→Y) = lift(Y→X))
   Baris = Antecedent · Kolom = Consequent · sel kosong (·) = di bawah ambang 1,05

              CONSEQUENT ▸
            Beras   Gula   Kopi   Air   SusuF  Piring  Buku   Sampo  Pasta
           ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬──────┐
  Minyak   │ 3,19 │ 2,15 │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │  ▲
  Gula     │ 1,93 │  —   │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │  A
  Mi Instan│  ·   │  ·   │ 2,45 │ 2,14 │  ·   │  ·   │  ·   │  ·   │  ·   │  N
  Popok    │  ·   │  ·   │  ·   │  ·   │ 2,31 │  ·   │  ·   │  ·   │  ·   │  T
  Deterjen │  ·   │  ·   │  ·   │  ·   │  ·   │ 2,25 │  ·   │  ·   │  ·   │  E
  Pulpen   │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │ 3,21 │  ·   │  ·   │  C
  Sabun    │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │  ·   │ 2,14 │ 2,13 │  E
           └──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘  D
  Sel:  ▐█▌ = lift ≥ 3,0 (sangat kuat) · ▐▌ = 2,5–2,9 · ▌ = 2,0–2,4 · 1,91–1,99 = tipis
  Interaksi: klik sel → panel rekomendasi bundling (harga paket, estimasi uplift)
             filter segmen (K-Means) → lift dihitung ulang khusus transaksi segmen tsb
  → 3 pasangan tertinggi: Pulpen+Buku 3,21 · Minyak+Beras 3,19 · Mi+Kopi 2,45
  → sel Gula–Gula "—" = diagonal matriks (tidak relevan); pasangan lain (Roti–Telur 2,11,
    Roti–Susu UHT 1,93, Deterjen–Pewangi 2,12, Popok–Bubur 1,93) tersedia via tooltip
```

#### 3.3.3 Rekomendasi Aksi Bisnis dari Aturan

| Kategori Aksi | Aturan Pendorong | Aksi Konkret | Kanal Eksekusi |
|---|---|---|---|
| **Cross-Selling** | Popok Bayi → Susu Formula (conf 24,7%); Minyak → Beras (conf 35,4%) | *Prompt* kasir / *pop-up e-commerce*: **"Pelanggan membeli X — lengkapi dengan Y (diskon bundling 5%)"** | POS kasir · halaman produk · struk digital |
| **Product Bundling** | 5 pasangan lift ≥ 2,3 | Buat 3 paket bernilai: **"Paket Masak Hemat"** (Minyak+Beras+Gula) · **"Paket Sehat Sarapan"** (Mi Instan+Kopi+Air Mineral) · **"Paket Perawatan Keluarga"** (Sabun+Sampo+Pasta Gigi) | Promo mingguan · katalog |
| **Penataan Rak (Store Layout)** | Pulpen═Buku Tulis; Popok═Susu Formula; Deterjen═Pembersih Piring | Letakkan pasangan ber-lift tinggi **satu rak berdekatan / bersebelahan pada jalur utama**; jauhkan dari jalur yang memaksa detour | Planogram toko fisik · *end-cap* |
| **Harga & Opsi Paket** | Beras+Minyak+Gula (3 aturan saling terkait) | *Bundle discount* Rp 5.000 untuk paket 3-item — target naikkan proporsi basket ≥ 4 item dari 34,3% ke 40% | Aplikasi · kasir |
| **Konten & Penempatan Iklan** | Mi Instan → Kopi Bubuk & Air Mineral | *Morning routine bundle* di jam 06.00–09.00 (varian hari kerja) | Push notification · banner |
| **Prioritas Berdasarkan Nilai** | Susu Formula & Beras punya nilai baris terbesar | Fokuskan percobaan A/B pada pasangan ber-**nilai baris tertinggi**, bukan lift tertinggi saja | Roadmap Tahap 6 |

---
---
=== TAHAP 4 ══════════════════════════════════════════════════════════════
## SEGMENTASI PELANGGAN — ALGORITMA K-MEANS (RFM)
=== TAHAP 4 ══════════════════════════════════════════════════════════════
---

**Input:** tabel RFM `1.480 pelanggan × 3 fitur`, telah distandardisasi (`StandardScaler`).
**Konfigurasi model:** `KMeans(n_init=10, random_state=42)` — 10 inisialisasi k-centroid untuk menghindari perangkap lokal; seed tetap agar hasil **reproducible**.

### 4.1 Optimal Cluster Determination (Elbow Method & Silhouette Score)

**Definisi:**

```
  Inertia (Elbow)    = Σᵢ Σ_{x ∈ Cᵢ} ‖x − μᵢ‖²        ← jumlah kuadrat jarak ke centroid (turun monoton)
  Silhouette Score   = (b − a) / max(a, b)              ← a = jarak rata-rata intra-cluster
                                                           b = jarak rata-rata ke cluster terdekat
  Rentang: −1 … +1   ( >0,5 solid · 0,26–0,50 struktur moderat · <0,26 lemah )
```

**Hasil Evaluasi (dijalankan untuk k = 2 sampai 8):**

| k | Inertia | Δ Inertia vs k−1 | Silhouette | Penilaian |
|---:|---:|---:|---:|---|
| 2 | 2.628,86 | — | 0,3475 | Terlalu kasar — membelah hanya "aktif vs pasif" |
| **3** | **1.774,40** | **−854,46 (−32,5%)** | **0,3607 ★ maksimum** | ✅ **TERPILIH — elbow + silhouette terbaik** |
| 4 | 1.427,98 | −346,42 (−19,5%) | 0,3020 ▼ | Silhouette turun tajam — klaster mulai terpecah artifak |
| 5 | 1.216,14 | −211,84 (−14,8%) | 0,3153 | Pulih sebagian, masih di bawah k=3 |
| 6 | 1.061,10 | −155,04 (−12,8%) | 0,3005 | Fragmentasi berlebih |
| 7 | 959,55 | −101,55 (−9,6%) | 0,2880 ▼ | Silhouette terburuk sejak k=2 |
| 8 | 868,40 | −91,15 (−9,5%) | 0,2918 | Diminishing returns |

```
   Inertia                                                        Silhouette
  2629 ┤●                                                        0,361 ┤        ● k=3 ★
  1774 ┤  ╲●  ◄ ELBOW                                             0,348 ┤ ●
  1428 ┤    ╲●                                                    0,315 ┤       ╲   ╲●
  1216 ┤      ╲●                                                  0,302 ┤      ╲●  ╲   ╲●
  1061 ┤        ╲●                                                0,288 ┤             ╲   ╲●
   960 ┤          ╲●                                              0,280 ┤
   868 ┤            ╲●                                            └──── k=2  3  4  5  6  7  8
       └── k=2  3  4  5  6  7  8
       Lengkungan tajam berhenti setelah k=3 → penambahan klaster     Puncak silhouette di k=3
       berikutnya hanya memotong inertia 19,5% s/d 9,5% tanpa         (0,3607) — struktur klaster
       memperbaiki pemisahan geometris                                paling terpisah & seimbang
```

**Argumentasi Pemilihan k = 3 (konvergensi dua metode):**

1. **Elbow:** penurunan inertia terbesar terjadi k=2→3 (−32,5%); setelah k=3 kelengkungan meland (−19,5% → −9,5%) — titik "siku" matematis jelas.
2. **Silhouette:** **nilai maksimum di k=3 (0,3607)**; setiap k lain lebih rendah → pemisahan antar-klaster paling bersih.
3. **Argumentasi bisnis:** 3 klaster persis mewakili 3 keputusan yang berbeda secara fundamental — (a) *pertahankan & hargai* (Loyal), (b) *dorong naik kelas* (Potential), (c) *menangkan kembali* (Churn Risk). Lebih dari 3 segmen akan memecah segmen dengan perilaku serupa menjadi sub-segmen yang **tidak punya playbook pemasaran berbeda** → *insight tidak actionable* = segmentasi gagal.

---

### 4.2 Kluster Profiling & RFM Labelling

#### 4.2.1 Tabel Profil Lengkap (k = 3)

| Metrik | **Cluster 0 — Loyal Customers** | **Cluster 1 — Churn Risk** | **Cluster 2 — Potential Loyal** |
|---|---:|---:|---:|
| Jumlah pelanggan | **461 (31,1%)** | **266 (18,0%)** | **753 (50,9%)** |
| **Recency** (mean / median) | **51,9 / 41 hari** 🟢 terbaru | **211,8 / 198 hari** 🔴 | 57,4 / 50 hari 🟡 |
| **Frequency** (mean / median) | **6,18 / 6 trx** 🟢 tertinggi | 2,20 / 2 trx 🔴 terendah | 3,41 / 3 trx |
| **Monetary** (mean / median) | **Rp 797.268 / Rp 757.825** 🟢 | Rp 243.748 / Rp 208.912 🔴 | Rp 349.083 / Rp 335.700 |
| Total Monetary segmen | **Rp 367.540.525** | Rp 64.836.850 | Rp 262.859.375 |
| **Pangsa Revenue** | **52,9%** | 9,3% | 37,8% |
| Transaksi dimiliki | 2.847 | 585 | 2.566 |
| Rata-rata basket | **3,11 item** | 3,09 item | 2,95 item |
| Revenue / pelanggan | Rp 797.268 | Rp 243.748 | Rp 349.083 |
| Aturan Apriori dominan | Pulpen → Buku Tulis (conf 42,0% / lift **3,42**) | Kopi → Mi Instan (conf 33,3% / lift **3,20**); Popok → Susu Formula (conf 32,0% / lift 3,07) | Pulpen → Buku Tulis (conf 39,2% / lift 3,10) |
| Kategori dominan | Bayi **31,0%** · Sembako 22,2% | Bayi 26,8% · Sembako 19,2% · **Minuman 12,0%** | Bayi 25,4% · Sembako 20,9% |
| Produk teratas | Susu Formula (Rp 59,7 jt) · Beras (Rp 54,0 jt) · Popok (Rp 43,0 jt) | Susu Formula (Rp 10,0 jt) · Beras (Rp 7,3 jt) · Popok (Rp 5,9 jt) | Susu Formula (Rp 34,3 jt) · Beras (Rp 30,8 jt) · Popok (Rp 24,2 jt) |

#### 4.2.2 Aturan Penamaan (Label berbasis data, bukan tebakan)

```
  Aturan dihitung pada level PROFIL KLUSTER (mean RFM per klaster), memakai kuantil
  antar-klaster sehingga penamaan sepenuhnya reproducible & bebas subjektivitas:

  IF   Frequency_mean ≥ kuantil-66% (4,30)  DAN  Monetary_mean ≥ kuantil-66% (Rp 492.502)
       ─────────────────────────────────────────────────────────────────────►  Loyal Customers
  ELIF Recency_mean ≤ kuantil-33% (55,5 hari) DAN Frequency_mean ≤ kuantil-50% (3,41)
       ────────────────────────────────────────────────────────────────►  New Customers *(tidak muncul;
                                                                           semua pelanggan baru telah
                                                                           bertransaksi ≥3× di data ini)
  ELIF Recency_mean ≥ kuantil-66% (106,8 hari)
       ───────────────────────────────────────────────────────────────────►  Churn Risk
  ELIF Frequency_mean ≥ kuantil-50% (3,41)
       ───────────────────────────────────────────────────────────────────►  Potential Loyal
  ELSE  ────────────────────────────────────────────────────────────────►  Hibernating *(tidak muncul pada k=3)
```

**Verifikasi penerapan aturan (3 klaster → 3 label):**

| Klaster | F_mean ≥ 4,30 **&** M_mean ≥ 492.502? | R_mean ≤ 55,5? | R_mean ≥ 106,8? | F_mean ≥ 3,41? | Label Hasil |
|---|---|---|---|---|---|
| C0 (R 51,9 · F 6,18 · M 797 rb) | ✅ Ya | — | — | — | **Loyal Customers** |
| C1 (R 211,8 · F 2,20 · M 244 rb) | ✗ | ✗ | ✅ Ya | — | **Churn Risk** |
| C2 (R 57,4 · F 3,41 · M 349 rb) | ✗ | ✗ (57,4 > 55,5) | ✗ | ✅ Ya | **Potential Loyal** |

> Hasil k=3 memunculkan persis **3 label: Loyal Customers, Churn Risk, Potential Loyal** — tanpa memaksakan label "New" yang tidak didukung distribusi data (Recency minimum = 1 hari, tetapi pelanggan tersebut sudah memiliki Frequency > median).

#### 4.2.3 RFM Persona Cards (Karakteristik Setiap Segmen)

```
┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
│ 🏆 LOYAL CUSTOMERS           │ │ 🌱 POTENTIAL LOYAL           │ │ ⚠ CHURN RISK                 │
│ 461 pelanggan · 31,1%        │ │ 753 pelanggan · 50,9%        │ │ 266 pelanggan · 18,0%         │
│ ─────────────────────────    │ │ ─────────────────────────    │ │ ─────────────────────────    │
│ R: 41 hari  (baru)           │ │ R: 50 hari                   │ │ R: 198 hari  (jauh)           │
│ F: 6 trx    (sering)         │ │ F: 3 trx    (cukup)          │ │ F: 2 trx     (jarang)         │
│ M: Rp 758 rb (tinggi)        │ │ M: Rp 336 rb (menengah)      │ │ M: Rp 209 rb (rendah)         │
│ ─────────────────────────    │ │ ─────────────────────────    │ │ ─────────────────────────    │
│ 💡 "Tulang punggung revenue" │ │ 💡 "Kuda pacu — naikkan      │ │ 💡 "Sedang pergi — setiap     │
│    52,9% pendapatan dari     │ │    frekuensi & basket"       │ │    hari diam-diam mahal"      │
│    1/3 pelanggan             │ │    butuh dorongan berikutnya │ │    9,3% pendapatan, terancam │
│ ─────────────────────────    │ │ ─────────────────────────    │ │ ─────────────────────────    │
│ 🎯 Retensi & Rewards         │ │ 🎯 Upgrade & Cross-sell      │ │ 🎯 Win-back & Re-engagement   │
│ Kanal: VIP WA · early access │ │ Kanal: promo bundling        │ │ Kanal: push "kami rindu"      │
│ Aturan: Pulpen→Buku (42%)    │ │ Aturan: Pulpen→Buku (39%)    │ │ Aturan: Kopi→Mi (33%)         │
└──────────────────────────────┘ └──────────────────────────────┘ └──────────────────────────────┘
```

---

### 4.3 Visualisasi Scatter Plot UI/UX — "RFM Segment Space"

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  SEGMENTASI K-MEANS — SCATTER RFM          [● Loyal] [● Potential] [● Churn]    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Y ▲ Monetary (Rp jt, log-scaled)                                              │
│  2,2 ┤                                          ╭──╮                            │
│      │                                ●●●      │CHURN│ ← balon = centroid       │
│  1,5 ┤                        ●●●●●●●●   ●●●   ╰──╯    ukuran balon ∝          │
│      │              ●●●●●●●●●          ●●●●            jumlah pelanggan        │
│  0,8 ┤     ●●●●●●●●●        ●●●●●                       ●●●●●●                │
│      │ ●●●●●        ●●●●●●●●      ●●●●●●●●●●●●●●●●●●●●●●                     │
│  0,4 ┤●●  ◄─────────────────────────────────────────────────                    │
│      │  ●●●●●●●●●●●●●●●●●●●●●●●  [POTENTIAL — hamparan terbesar]              │
│  0,1 ┤                                                                          │
│      └──┬──────┬──────┬──────┬──────┬──────┬──────┬──────▶ X                    │
│        0     50     100    150    200    250    300    363      Recency (hari)   │
│                                                                              │
│  AXIS ALTERNATIF (toggle): Frequency (X) · bubble size = Monetary              │
│  ─────────────────────────────────────────────────────────────────────         │
│  INTERAKSI:                                                                     │
│  • Klik legend segmen  → cross-filter seluruh dashboard (KPI, produk, aturan)   │
│  • Box-select area     → bandingkan rentang R/M dalam seleksi → drill-down     │
│  • Hover titik         → tooltip: C-ID · R/F/M · kategori favorit · revenue    │
│  • Toggle "Log scale"  → meratakan sebaran Monetary (skew kanan)               │
│  • Filter periode      → titik pelanggan direkomputasi (segmentasi dinamis)     │
│  OUTLIER: ● R=363 (paling lama) · M=Rp 2,22 jt (paling besar) → keduanya       │
│           ditandai ring emas & masuk daftar tindak lanjut prioritas             │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Tata letak visualisasi segmentasi:** scatter menempati **kolom 1–8** (visual utama), disandingkan **kolom 9–12** dengan (a) *donut distribution* jumlah pelanggan per segmen, (b) *stacked bar* pangsa revenue per segmen, dan (c) kartu persona terpilih (sinkron dengan titik yang di-hover).

---

### 4.4 Strategi Retensi — Tindakan Preskriptif per Segmen

| Segmen | Tujuan Bisnis | Aksi Preskriptif (spesifik & terukur) | Kanal | KPI Pengukuran | Prioritas |
|---|---|---|---|---|---|
| 🏆 **Loyal Customers** (461) | **Pertahankan & perbesar share-of-wallet** | 1. Program VIP: *early access* promo & poin 2× lipat · 2. *Upsell* paket premium (Susu Formula + Popok bayi ukuran besar) · 3. Undang ke program *referral* — 1 rekomendasi = Rp 25.000 kredit | WhatsApp Broadcast · kartu member · app | Retention rate ≥ 95%; Avg basket 3,11 → 3,40; Share revenue ≥ 55% | 🟡 Sedang |
| 🌱 **Potential Loyal** (753) | **Naikkan frekuensi (Frequency 3 → 5)** | 1. Kampanye *bundle* rekomendasi aturan Apriori (Pulpen+Buku, Beras+Minyak) · 2. *Milestone reward*: "belanja ke-5 bulan ini = gratis ongkir" · 3. Targetkan kenaikan basket 2,95 → 3,25 | App notification · SMS · banner in-store | Upgrade rate ke Loyal ≥ 15% (113 pelanggan); Frequency +0,8 trx/pelanggan | 🟢 **Tinggi** *(populasi terbesar)* |
| ⚠ **Churn Risk** (266) | **Menangkan kembali sebelum kehilangan permanen** | 1. *Win-back campaign* personal: diskon 15% dengan **kedaluwarsa 7 hari** (urgency) · 2. Rekomendasikan pasangan aturan favorit historisnya (Kopi+Mi Instan, Popok+Susu Formula) · 3. *Survey* ringan "apa yang membuat Anda jarang kembali?" | Push notification · SMS · telepon CS | Reactivation rate ≥ 25% (66 pelanggan); Recency 212 → <90 hari; Pulihkan ≥ Rp 16,2 jt/tahun | 🔴 **Tinggi** *(urgensi waktu)* |

**Peta Segmentasi Terhadap Kesiapan Aksi:**

```
   FREQUENCY ▲
     tinggi  │  🏆 LOYAL              │  (belum terbentuk: "Champions
             │  461 · 52,9% revenue   │   hyper-active" tidak ada pada k=3)
             │  ► pertahankan          │
    ─────────┼─────────────────────────┼────────────────────────
     rendah  │  🌱 POTENTIAL           │  ⚠ CHURN RISK
             │  753 · 37,8%           │  266 · 9,3%
             │  ► dorong naik kelas    │  ► menangkan kembali
             └─────────────────────────┴────────────────────────►
              RECENCY baru (R < 60)     RECENCY lama (R > 180)
```

---
---
=== TAHAP 5 ══════════════════════════════════════════════════════════════
## BUSINESS INTELLIGENCE DASHBOARD — UI/UX BLUEPRINT
=== TAHAP 5 ══════════════════════════════════════════════════════════════
---

**Prinsip Arahan:** seluruh rancangan menggunakan **Design System Dark Executive Mode** (Bagian 0B), grid 12-kolom, dan hierarki **KPI → Visual → Tabel/Insight**. Implementasi produksi berjalan sebagai aplikasi BI *"NusaRetail Intelligence"* dengan 7 modul navigasi (`00 Ringkasan → 01 EDA → 02 Preprocessing → 03 Apriori → 04 K-Means → 05 Dashboard → 06 Rekomendasi`).

### 5.1 Global Shell (Kerangka Seluruh Halaman)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ ◆ NusaRetail INTELLIGENCE          [ 00 | 01 | 02 | 03 | 04 | 05 | 06 ]   ● user ▸  │ ← topbar 56px
├──────────┬───────────────────────────────────────────────────────────────────────────┤
│          │  BREADCRUMB  Beranda ▸ Dashboard ▸ Segmen: Churn Risk        ⟳ 1 filter  │
│  S       │                                                                          │
│  I       │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐            │
│  D       │  │Rp 696,1J│ │  5.998  │ │  1.480  │ │  3,05   │ │ +10,0%  │  ◄ ZONA 1  │
│  E       │  │ ▲10,0%  │ │ ▲ 2,5%  │ │ ▬ 0,0%  │ │ ▬ med.3 │ │ MoM Des │   KPI      │
│  B       │  │ spark〜〜│ │ spark〜〜│ │ spark〜〜│ │ spark〜〜│ │ spark〜〜│            │
│  A       │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘            │
│  R       │                                                                          │
│  ┌────┐  │  ┌───────────────────────────────────┐ ┌────────────────────────────┐    │
│  │Filter│ │  ▓ ZONA 2a — VISUAL UTAMA          │ │ ▓ ZONA 2b — PENDAMPING     │    │
│  │────│  │  (kolom 1–8)                        │ │ (kolom 9–12)               │    │
│  │Periode│ │   tren bulanan / heatmap /         │ │   donut · ranking ·        │    │
│  │Kategor│ │   scatter RFM / network graph      │ │   persona cards            │    │
│  │Segmen│ │                                    │ │                            │    │
│  │Wilayah│ └───────────────────────────────────┘ └────────────────────────────┘    │
│  │Reset │                                                                          │
│  └────┘  │  ┌──────────────────────────────────────────────────────────────┐        │
│          │  │ ▓ ZONA 3 — TABEL DETAIL (drill-down) + INSIGHT PANEL (kanan) │        │
│  Export  │  └──────────────────────────────────────────────────────────────┘        │
└──────────┴───────────────────────────────────────────────────────────────────────────┘
```

### 5.2 KPI Cards Section (Zona 1 — Orientasi)

| KPI Card | Nilai (basis data) | Delta (vs bulan sebelumnya) | Sub-informasi | Aksi Klik |
|---|---:|---:|---|---|
| **Total Revenue** | **Rp 696.085.375** | Des 62,43 jt vs Nov 56,76 jt = **▲ 10,0% MoM** | Sparkline 12 bulan · target garis horizontal | Drill-down ke komposisi bulanan |
| **Total Transaksi** | **5.998** (526 bulan Des) | **▲ 2,5% MoM** (513 → 526) | Rerata 499 trx/bulan | Buka tabel transaksi |
| **Unique Active Customers** | **1.480** | **▬ 0,0%** *(basis stabil)* | 1.480 teridentifikasi + 28 baris `UNKNOWN` | Buka daftar pelanggan |
| **Avg Basket Size** | **3,05 produk/trx** | **▬ 0,00** *(median 3 · stabil)* | Median 3 · 33,6% transaksi ≤ 2 item · P90 basket value Rp 243.013 | Lihat distribusi basket |
| **Avg Basket Value** | **Rp 116.053/trx** | MoM Des ▲ 7,2% | Median Rp 88.725 | Lihat produk kontributor |
| **Bonus — Aturan Aktif** | **25 rules · 44 itemsets** | dihitung ulang saat filter berubah | Lift maks 3,21 | Buka modul Apriori |

**Spesifikasi komponen KPI Card:**

```
┌──────────────────────────────┐   bg #1E293B · radius 16px · border 1px #334155
│ TOTAL REVENUE        [icon]  │   Label : 11px uppercase tracking +12% #94A3B8
│ Rp 696.085.375               │   Nilai : 32px weight 800 tabular-nums #F8FAFC
│ ▲ 10,0%  vs bulan lalu       │   Delta : 12px · ▲ #10B981 · ▼ #EF4444
│ ▁▂▃▂▃▄▃▄▅▄▆▇ (sparkline)    │   Spark : 60×24px, stroke 1.5px #38BDF8, fill gradien
└──────────────────────────────┘   Hover : card terangkat 2px + border #38BDF8 (150ms)
```

### 5.3 Sales Analytics View (Zona 2a/2b)

```
┌───────────────────────────────────────────────┬──────────────────────────────────────┐
│  💹 TREN PENJUALAN BULANAN 2025               │  🥇 TOP 10 PRODUK (revenue)          │
│  Mode: [Revenue ▾] [Transaksi ▾] [AOV ▾]     │  ┌────────────────────────────────┐  │
│                                               │  │ 1 Susu Formula   Rp 103,9 jt ▐▌│  │
│  66 ┤                          ╭╮             │  │ 2 Beras Premium  Rp  92,1 jt ▐ │  │
│  62 ┤    ╭╮   ╭╮          ╭╮╭──╯╰╮            │  │ 3 Popok Bayi     Rp  73,2 jt ▐ │  │
│  58 ┤ ╭╮ ╰╮╭╮ ╰╮╭╮ ╭╮ ╭╮ ╰╯     ╰╮   ╭╮     │  │ 4 Telur Ayam     Rp  35,8 jt ▌ │  │
│  54 ┤ ╰╯  ╰╯ ╰─╯╰╯ ╰╯╰╮╯       ╰╮╭╮╯╰╮╭╮   │  │ 5 Lampu LED      Rp  27,3 jt ▌ │  │
│  51 ┤                 ╰╯          ╰╯╰╯  ╰╯╰   │  │ 6 Susu UHT       Rp  24,5 jt ▌ │  │
│     └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬─    │  │ 7 Gula Pasir     Rp  22,9 jt ▌ │  │
│       J  F  M  A  M  J  J  A  S  O  N  D     │  │ 8 Sampo          Rp  22,5 jt ▌ │  │
│                                               │  │ 9 Deterjen       Rp  21,8 jt ▌ │  │
│  ▸ Area chart + line MA(3) · aksen #38BDF8    │  │10 Minyak Goreng  Rp  21,5 jt ▌ │  │
│  ▸ Anotasi otomatis: puncak Okt (Rp 65,2 jt)  │  └────────────────────────────────┘  │
│    & titik terendah Apr (Rp 51,7 jt)          │  ▸ Horizontal bar · warna per kategori│
│  ▸ Click month → seluruh widget terfilter      │  ▸ Click bar → drill-down produk      │
├───────────────────────────────────────────────┤  ▸ Toggle: Revenue / Jumlah Baris     │
│  📊 KOMPOSISI KATEGORI (donut)                │──────────────────────────────────────│
│         Bayi 28,5% ▓▓▓▓                        │  💳 RINGKASAN PEMBAYARAN & WILAYAH    │
│         Sembako 21,4% ▓▓▓                      │  Transfer 25,6% · Tunai 25,3%        │
│         9 kategori · klik slice = cross-filter │  Debit 24,9% · QRIS 24,0%           │
│                                                │  Top wilayah: Bikomi Rp 98,3 jt     │
└───────────────────────────────────────────────┴──────────────────────────────────────┘
```

### 5.4 Apriori View (Cross-Selling Intelligence)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ 3a. PARAMETER │ Min Support [0,02 ▾] Min Confidence [0,20 ▾] Min Lift [1,05 ▾] ⟲Reset│
│ KPI: Frequent Itemsets 44 │ Aturan Aktif 25 │ Basis 5.998 transaksi │ Lift maks 3,21 │
├─────────────────────────────────────────────────────┬────────────────────────────────┤
│ 3b. INTERACTIVE CROSS-SELLING MATRIX (heatmap lift)│ 3c. ASSOCIATION NETWORK        │
│          ▸ Beras Gula Kopi Susu Pirs Buku Air      │                                │
│  Minyak  │ 3,2 │ 2,1 │  ·  │  ·  │  ·  │  ·  │  · │     [Gula]                    │
│  Gula    │ 1,9 │  —  │  ·  │  ·  │  ·  │  ·  │  · │  [Minyak]═3,19═[Beras]        │
│  Mi      │  ·  │  ·  │ 2,5 │  ·  │  ·  │  ·  │ 2,1│      ▲ 18% node = support      │
│  Popok   │  ·  │  ·  │  ·  │ 2,3 │  ·  │  ·  │  · │ [Pulpen]══3,21══[Buku Tulis]   │
│  Deterjen│  ·  │  ·  │  ·  │  ·  │ 2,2 │  ·  │  · │[Popok]──2,31──[Susu Formula]   │
│  Pulpen  │  ·  │  ·  │  ·  │  ·  │  ·  │ ══ │  · │[Deterjen]─2,25─[Pembersih]     │
│  (angka = lift pasangan; arah & confidence muncul pada tooltip)                     │
│ ▸ Klik sel → panel: harga paket, uplift, tombol     ├────────────────────────────────┤
│   "Buat Promo Bundling"                             │ 3d. ATURAN TERATAS (TOP 10)    │
│ ▸ Filter segmen → matrix dihitung per segmen        │  X → Y        Sup Conf  Lift   │
│ ▸ Toggle: Lift / Confidence / Support               │  Pulpen→Buku  4,1% 40,0% 3,21  │
│                                                     │  Minyak→Beras 3,8% 35,4% 3,19  │
│                                                     │  Mi→Kopi      2,4% 25,0% 2,45  │
│                                                     │  Popok→Susu   2,4% 24,7% 2,31  │
│                                                     │  Deterjen→Piring 2,3% 24,6%2,25 │
│                                                     │  [ekspor CSV ▾] [lihat 25 ▾]    │
└─────────────────────────────────────────────────────┴────────────────────────────────┘
```

**Catatan UX:** sebelum aturan dimuat, tampilkan *skeleton loading* + teks *"Menghitung 435 pasangan kandidat…"*; bila aturan kosong, beri pesan panduan (*"Turunkan minimum support ke 1%"*) — bukan layar kosong.

### 5.5 K-Means View (Customer Segmentation)

```
┌──────────────────────────────────────────────┬──────────────────────────────────────┐
│ 4a. CLUSTER DISTRIBUTION   [Jumlah ▾|Rev ▾]  │ 4b. RFM PERSONA CARDS                │
│                                              │ ┌──────────────────────────────────┐ │
│  Potential   ████████████████████ 50,9% (753)│ │ 🏆 LOYAL CUSTOMERS    461 · 31,1% │ │
│  Loyal       ██████████████       31,1% (461)│ │ R 41 · F 6,18 · M Rp 797 rb       │ │
│  Churn Risk  ██████               18,0% (266)│ │ Revenue 52,9%         [aksi ▸]    │ │
│                                              │ ├──────────────────────────────────┤ │
│  Revenue share:                              │ │ 🌱 POTENTIAL LOYAL   753 · 50,9%  │ │
│   Loyal 52,9% │ Pot. 37,8% │ Churn 9,3%     │ │ R 50 · F 3,41 · M Rp 349 rb       │ │
│                                              │ │ Revenue 37,8%         [aksi ▸]    │ │
│  ▸ klik bar → cross-filter segmen            │ ├──────────────────────────────────┤ │
│                                              │ │ ⚠ CHURN RISK        266 · 18,0%  │ │
│                                              │ │ R 198 · F 2,20 · M Rp 244 rb     │ │
│                                              │ │ Revenue 9,3%           [aksi ▸]  │ │
│                                              │ └──────────────────────────────────┘ │
├──────────────────────────────────────────────┼──────────────────────────────────────┤
│ 4c. SCATTER RFM (bubble = Monetary)          │ 4d. METRIK SEGMENT TERPILIH          │
│                                              │  Pelanggan  : 461                    │
│  Y Monetary ▲                                │  Revenue    : Rp 367,5 jt (52,9%)    │
│   Rp 2,2 jt ┤  ●●● [CHURN]                  │  Recency    : 51,9 hari (mean)       │
│   Rp 0,8 jt ┤ ●●●●●●●●●●●●●●●●●●●●●        │  Avg basket : 3,11 produk            │
│   Rp 0,35 jt┤●●●●●●●●●● [POTENTIAL]         │  Top rule   : Pulpen → Buku (42%)    │
│              │ ●●●●●●●● [LOYAL]              │  Kategori   : Bayi 31% · Sembako 22% │
│              └──────────────────────▶ X       │  Aksi ▸ [Buka playbook segmen]      │
│              0    60   120   180   240  363   ├──────────────────────────────────────┤
│              Recency (hari)                   │ ▸ Toggle X: Recency | Frequency      │
│                                              │ ▸ Log-scale Y saat Monetary skew    │
└──────────────────────────────────────────────┴──────────────────────────────────────┘
```

**Spesifikasi RFM Persona Card:** badge segmen (warna eksklusif per Bagian 0B.2) · 3 chip metrik `R / F / M` · baris *share of revenue* · tombol aksi `▸` yang membuka rekomendasi preskriptif dari Tahap 6.

### 5.6 Interactive Controls (Filter) — Spesifikasi Perilaku

| Kontrol | Tipe | Opsi | Perilaku Cross-filter | State Management |
|---|---|---|---|---|
| **Filter Periode** | Date-Range Picker + preset | 7H · 30D · QTD · YTD · **Jan–Des 2025** · Custom | Semua KPI, chart, tabel, **dan basis perhitungan Apriori/K-Means** ikut tersaring | `session_state['date_range']` · debounce 300 ms |
| **Filter Kategori Produk** | **Dropdown Multi-select** + chip | 9 kategori (ATK … Sembako) | Memfilter produk → matrix Apriori & top products dihitung ulang | Chip dapat dihapus satu per satu; tampil "N aktif" |
| **Filter Segmentasi Pelanggan** | Dropdown + tombol toggle cepat | Semua · Loyal (461) · Potential (753) · Churn Risk (266) | **Inti integrasi:** KPI, sales, aturan, dan scatter hanya memakai transaksi segmen tsb | Klik legend scatter/kartu persona = aksi yang sama (bidireksional) |
| **Filter Wilayah** *(opsional)* | Multi-select | 8 wilayah + "Tidak Diketahui" | Memfilter basis pelanggan & revenue per wilayah | Konsisten dg filter lain (AND logic) |
| **Tombol Reset** | Button + badge counter | ⟲ Reset semua | Mengembalikan ke *default state* periode penuh 2025 | Muncul hanya bila ≥1 filter aktif |
| **Micro-feedback** | Toast + skeleton | "Menyegarkan 6 modul…" | *Skeleton* per widget selama rekomputasi | Auto-dismiss 2,5 detik |

### 5.7 Fitur Bonus — Integrasi Apriori × K-Means

**Konsep:** aturan asosiasi dihitung **secara terpisah untuk transaksi masing-masing klaster** → menghasilkan rekomendasi kombinasi produk yang **spesifik per segmen**, bukan rekomendasi generik.

**Hasil perhitungan (basis: transaksi ber-ID milik tiap klaster):**

| Segmen | # Aturan lolos | Rekomendasi #1 | Conf / Lift | Rekomendasi #2 | Rekomendasi #3 | Alasan Bisnis |
|---|---:|---|---|---|---|---|
| 🏆 **Loyal** (2.847 trx) | **23** | Pulpen → Buku Tulis | **41,96% / 3,42** | Minyak → Beras Premium (42,53% / 3,25) | Deterjen → Pembersih Piring (23,79% / 2,16) | *Upsell* ke nilai tinggi — pelanggan sudah loyal, dorong basket lebih besar |
| 🌱 **Potential** (2.566 trx) | **18** | Pulpen → Buku Tulis | 39,22% / 3,10 | Beras → Minyak Goreng (33,33% / 3,07) | Mi Instan → Kopi Bubuk (26,21% / 2,64) | Paket *bundle* hemat untuk menaikkan frequency & basket |
| ⚠ **Churn Risk** (585 trx) | **17** | **Kopi Bubuk → Mi Instan** | **33,33% / 3,20** | Beras → Minyak Goreng (29,41% / 3,19) | Popok → Susu Formula (32,00% / 3,07) | *Win-back* memakai kebiasaan hemat & kebutuhan wajib historisnya |

**Tampilan UI modul bonus (panel "Untuk Anda"):**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  🎯 REKOMENDASI PERSONAL — Apriori × K-Means        Segmen terpilih: [⚠ Churn ▾]   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  Untuk 266 pelanggan Churn Risk, kombinasi terbukti paling sering dibeli bersama:   │
│                                                                                     │
│  ┌──────────────────────────┐  ┌──────────────────────────┐  ┌────────────────┐     │
│  │ "Paket Nongkrong Pagi"   │  │ "Paket Dapur Hemat"      │  │ "Paket Bayi    │     │
│  │ Kopi Bubuk + Mi Instan   │  │ Beras 5kg + Minyak Goreng│  │  Lengkap"      │     │
│  │ lift 3,20 · conf 33,3%   │  │ lift 3,19 · conf 29,4%  │  │ Popok + Susu   │     │
│  │ ▸ kirim promo "kami      │  │ ▸ voucher Rp 10rb        │  │ Form.          │     │
│  │   rindu" + paket ini     │  │ ▸ deadline 7 hari        │  │ lift 3,07      │     │
│  └──────────────────────────┘  └──────────────────────────┘  └────────────────┘     │
│  [ Ekspor daftar pelanggan (CSV) ]   [ Buat kampanye ]   [ Lihat aturan lain (17) ] │
└─────────────────────────────────────────────────────────────────────────────────────┘
   Filter segmen & periode di atas memicu rekomputasi aturan → rekomendasi selalu segar
```

---
---
=== TAHAP 6 ══════════════════════════════════════════════════════════════
## REKOMENDASI KEPUTUSAN BISNIS PRESCRIFTIF
=== TAHAP 6 ══════════════════════════════════════════════════════════════
---

### 6.1 Action Matrix — Prioritas Tindakan

**Metode Penilaian (transparan & terukur):**

```
  Skor Prioritas  =  ( URGENSI × DAMPAK × KEMUDAHAN ) / BIAYA          skala 1–5 tiap dimensi
                     U = seberapa cepat harus dilakukan (5 = segera)
                     D = besaran dampak ke revenue/retensi (5 = sangat besar)
                     K = kemudahan eksekusi dengan sumber daya saat ini (5 = sangat mudah)
                     B = biaya relatif (1 = murah/bersifat prosedural · 5 = butuh investasi besar)

  Interpretasi:  ≥ 50 = PRIORITAS 1 (Quick Win) · 20–49 = PRIORITAS 2 · 10–19 = PRIORITAS 3 · < 10 = Backlog
```

| # | Inisiatif | U | D | K | B | **Skor** | Prioritas | Pemilik | Landasan Data |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| A1 | **Bundling & penataan rak** untuk 5 pasangan lift ≥ 2,3 (Pulpen+Buku, Minyak+Beras, Popok+Susu, Deterjen+Pembersih, Mi+Kopi) | 5 | 4 | 5 | 1 | **100** | 🔴 P1 *Quick Win* | Ops. Store | Lift 2,25–3,21 · conf 20,7–40,0% |
| A5 | **Paket "Masak Hemat"** (Minyak+Beras+Gula) — 3 aturan saling terkait, diskon bundling Rp 5.000 | 4 | 5 | 5 | 2 | **50** | 🔴 P1 *Quick Win* | Marketing | Revenue 2 top kategori = 49,9% |
| A2 | **Win-back campaign segmen Churn Risk** (266 pelanggan, kedaluwarsa 7 hari, paket kebiasaan historis) | 5 | 4 | 3 | 2 | **30** | 🟡 P2 | Marketing + CS | Recency 212 hari · 9,3% revenue |
| A6 | **Integrasi Apriori × K-Means** — rekomendasi personal per segmen pada dashboard & POS | 3 | 4 | 4 | 2 | **24** | 🟡 P2 | Data / IT | 23·18·17 aturan per segmen terbukti |
| A8 | **A/B testing & evaluasi KPI** — uji paket promosi terhadap kelompok kontrol | 3 | 4 | 4 | 2 | **24** | 🟡 P2 | Data / Marketing | Menjamin uplift terukur, bukan asumsi |
| A4 | **Cross-sell prompt di POS/e-commerce** ("pelanggan membeli X — lengkapi dengan Y") | 4 | 4 | 3 | 3 | **16** | 🟡 P2 | IT + Vendor POS | Target +5 pp attach rate |
| A7 | **ETL & data-quality check otomatis** (validasi duplikat/missing/rumus harian) | 4 | 3 | 4 | 3 | **16** | 🟡 P2 | Data Engineer | 4.543 inkonsistensi terdeteksi manual saat ini |
| A3 | **Program loyalitas/VIP** segmen Loyal (461 pelanggan) | 3 | 4 | 3 | 3 | **12** | 🟢 P3 | Marketing | 52,9% revenue · pertahanan = prioritas jangka panjang |

**Peta Aksi (Dampak × Kemudahan):**

```
   DAMPAK ▲
    tinggi │  A5 ●                     │  A1 ●
           │      "Masak Hemat"        │      "Bundling + Rak"     ← QUICK WINS
           │  A2 ●            A6/A8 ●  │  A4 ●
           │   Win-back        Integrsi│   POS prompt
    ───────┼────────────────────────────┼─────────────────────────
    rendah │  A3 ●                      │  A7 ●
           │   Loyal VIP                │   ETL otomatis
           └────────────────────────────┴────────────────────────►
            MURAH / MUDAH                 MAHAL / SULIT
                                    (biaya & upaya eksekusi)
```

---

### 6.2 Estimasi Dampak Bisnis (Proyeksi Uplift & KPI Evaluasi)

#### 6.2.1 Model Perhitungan (Asumsi Ditandai Eksplisit)

| ID | Skenario Uplift | Asumsi *(wajib divalidasi via A/B test — A8)* | Dasar Hitung (data riil) | **Proyeksi Tahunan** |
|---|---|---|---|---:|
| **S1** | Cross-sell 5 aturan teratas | Confidence tiap aturan naik **+5 pp** (Δ attach rate) | 608–641 trx basis antecedent × 5% × nilai baris consequent (Rp 11.050–161.802) | **Rp 10.791.432** (1,55%) |
| **S2** | Perbesar basket segmen Loyal | Avg basket Loyal naik **3,11 → 3,40 item** (+0,29) | 2.847 transaksi × 0,29 item × Rp 38.100/item | **Rp 31.460.000** (4,52%) |
| **S3** | Reaktivasi segmen Churn Risk | Berhasil mengambil kembali **25% kontribusi** segmen (≈66 pelanggan) | 25% × Rp 64.836.850 | **Rp 16.210.000** (2,33%) |
| **S4** | Upgrade Potential → Loyal | **15% dari 753** pelanggan menaik +1 transaksi/tahun | 113 pelanggan × Rp 116.053 (avg basket value) | **Rp 13.110.000** (1,88%) |
| | | | **TOTAL KONSERVATIF** | **Rp 71.570.000 ≈ 10,3% dari revenue** |

```
  PROYEKSI UPLIFT TERHADAP BASELINE Rp 696.085.375

  Baseline  ════════════════════════════════════════════════════════════  Rp 696,1 jt (100%)
  + S2 Loyal basket    ▐ 4,5%   Rp 31,5 jt
  + S3 Win-back churn  ▐ 2,3%   Rp 16,2 jt
  + S4 Potential upgr. ▐ 1,9%   Rp 13,1 jt
  + S1 Cross-sell 5    ▐ 1,6%   Rp 10,8 jt
  ──────────────────────────────────────────────
  Proyeksi  ══════════════════════════════════════════════════════════════  Rp 767,7 jt (110,3%)
  Asumsi konservatif: tanpa efek sinergi, tanpa kenaikan trafik baru, uplift hanya dari basis pelanggan eksisting
```

**Rincian kalkulasi S1 (per aturan — dapat diaudit):**

| Aturan | Basis trx antecedent | Δtrx (+5 pp) | Nilai rata-rata baris consequent | Uplift |
|---|---:|---:|---:|---:|
| Pulpen → Buku Tulis | 608 | +30 | Rp 11.050 | Rp 335.920 |
| Minyak → Beras Premium | 641 | +32 | Rp 138.044 | Rp 4.424.310 |
| Mi Instan → Kopi Bubuk | 571 | +29 | Rp 27.063 | Rp 772.649 |
| Popok → Susu Formula | 571 | +29 | Rp 161.802 | Rp 4.619.447 |
| Deterjen → Pembersih Piring | 552 | +28 | Rp 23.156 | Rp 639.106 |
| | | | **TOTAL S1** | **Rp 10.791.432** |

#### 6.2.2 KPI Evaluasi Keberhasilan

| # | KPI | Baseline (2025) | Target 3 bulan | Target 6 bulan | Frekuensi Ukur | Sumber Data |
|---|---|---:|---:|---:|---|---|
| 1 | **Attach rate** (transaksi berisi ≥1 pasangan aturan) | lihat dasar confidence 20,7–40,0% | **+3 pp** | **+5 pp** | Mingguan | Matriks basket |
| 2 | **Avg basket size** | 3,05 item | 3,15 | **3,40** (segmen Loyal) | Mingguan | `basket_size` |
| 3 | **Repeat purchase rate** (pelanggan ≥2 trx/bulan) | F mean 4,05/tahun | +5% | **+10%** | Bulanan | Tabel RFM |
| 4 | **Reactivation rate Churn Risk** | 0% (belum ada program) | **15%** (≈40 orang) | **25%** (≈66 orang) | Bulanan | Segmentasi berjalan |
| 5 | **Revenue per segmen** | Loyal 52,9% · Pot 37,8% · Churn 9,3% | Churn ≥ 10,5% | Churn ≥ 12% & Pot → Loyal ≥ 15% | Bulanan | Faktur |
| 6 | **Total revenue bulanan** | rerata Rp 58,0 jt | Rp 61 jt | **Rp 64 jt** (+10,3%) | Bulanan | Dashboard |
| 7 | **Promo ROI** | belum terukur | > 1,5× | **> 2,5×** | Per kampanye | Biaya promo vs uplift |
| 8 | **Kualitas data** (baris lolos validasi) | 98,7% (243 baris terbuang) | **≥ 99,5%** | ≥ 99,9% + otomatis | Harian | Data quality check |

#### 6.2.3 Risiko & Mitigasi Estimasi

| Risiko | Probabilitas | Dampak | Mitigasi |
|---|---|---|---|
| Asumsi +5 pp confidence tidak tercapai | Sedang | Uplift S1 menyusut hingga Rp 0 | Uji A/B per paket (A8); naikkan bertahap 2 pp → 5 pp |
| Diskon bundling menekan margin | Sedang | Profit turun meski revenue naik | Batasi diskon ≤ 5% dan hanya untuk item dengan margin di atas rata-rata; hitung *contribution margin* per paket |
| Respon win-back rendah (<15%) | Rendah–Sedang | S3 tertunda | Uji 3 varian pesan (diskon / konten edukatif / survei); segmentasi ulang pelanggan *most-likely-to-return* |
| Fatigue promo pada segmen Loyal | Rendah | Loyal justru churn | Batasi frekuensi ≤ 2 kontak/bulan; komunikasi bernilai (early access, bukan diskon) |
| Perubahan musiman 2026 | Sedang | Proyeksi tidak linier | Restrukturisasi proyeksi per kuartal, gunakan MoM & YoY ketika data 2026 tersedia |

---

### 6.3 Implementation Roadmap

```
 FASE 0 (Minggu 1)          FASE 1 — QUICK WIN (Bulan 1–3)            FASE 2 — PENGUATAN (Bulan 3–6)
 ─────────────────          ─────────────────────────────────          ────────────────────────────────
 ✓ Finalisasi model         A1  Bundling & penataan rak   ░░░░░░░░░░    A3  Program loyalitas/VIP
 ✓ Baseline KPI             A5  Paket "Masak Hemat"       ░░░░░░░       A6  Integrisi Apriori×K-Means
 ✓ Definisi ambang          A2  Win-back Churn Risk       ░░░░░░░░░░░   A4  Cross-sell prompt POS
                            A7  ETL & DQ check (mulai)    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                            A8  A/B testing (mulai)          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ───────────────────────────────────────────────────────────────────────────────────────────────────
 M1                    M2                     M3                     M4          M5          M6
 Go-live dashboard →  Evaluasi 1 →           Evaluasi 2 →           Pivot/stop → Skala →     Review
 + quick wins         +3 pp attach           +15% reactivation       keputusan    optimal     Direksi
```

**Rencana Aksi Jangka Pendek (1–3 bulan):**

| Bulan | Aksi | Keluaran (Deliverable) | KPI Pemeriksaan |
|---|---|---|---|
| **M1** | 1. *Go-live* dashboard Dark Executive Mode · 2. Terapkan A1 (planogram 5 pasangan) & A5 (paket Masak Hemat) · 3. Mulai A7 (validasi data harian) | Dashboard aktif · Planogram baru · Laporan DQ harian | 100% toko menerapkan planogram · data quality ≥ 99% |
| **M2** | 1. Jalankan A2 *win-back* (266 pelanggan, 3 varian pesan) · 2. Mulai A8 A/B testing S1 · 3. Review attach rate mingguan | Kampanye terkirim · Laporan A/B gelombang 1 | Attach rate +2 pp · 10% churn mulai bereaksi |
| **M3** | 1. Evaluasi hasil Q1 · 2. Kalibrasi parameter Apriori bila perlu · 3. Keputusan *scale/hold/stop* tiap inisiatif | Laporan evaluasi Q1 · Revisi parameter | **+3 pp attach · +15% reactivation · avg basket 3,15** |

**Rencana Aksi Jangka Menengah (3–6 bulan):**

| Bulan | Aksi | Keluaran (Deliverable) | KPI Pemeriksaan |
|---|---|---|---|
| **M4** | 1. Implementasi A4 (prompt POS pada 2 kategori dengan lift tertinggi) · 2. Integrasikan A6 (rekomendasi personal per segmen di aplikasi/kasir) | Modul rekomendasi aktif · Daftar target pelanggan per segmen | Uptake rekomendasi ≥ 15% kasir |
| **M5** | 1. Luncurkan A3 (VIP Loyal: poin 2×, early access, referral) · 2. Optimasi paket berdasarkan data A/B terbaru | Program keanggotaan berjalan · Paket final teruji | Retention Loyal ≥ 95% · basket Loyal → 3,40 |
| **M6** | 1. Review menyeluruh oleh Direksi · 2. Finalisasi proyeksi 2026 · 3. Rencanakan skala multi-cabang & prediktif (churn scoring) | Laporan akhir 6 bulan · Blueprint kuartal berikutnya | **Revenue bulanan Rp 64 jt (+10,3%) · reactivation 25% · promo ROI > 2,5×** |

---
=== LAMPIRAN ═════════════════════════════════════════════════════════════
---

### LAMPIRAN A — Katalog Produk (30 SKU · 9 Kategori)

| ID | Produk | Kategori | Harga Ref. | ID | Produk | Kategori | Harga Ref. |
|---|---|---|---:|---|---|---|---:|
| P001 | Beras Premium 5kg | Sembako | Rp 78.000 | P016 | Sampo 170ml | Perawatan | Rp 18.500 |
| P002 | Minyak Goreng 1L | Sembako | Rp 18.500 | P017 | Pasta Gigi | Perawatan | Rp 12.500 |
| P003 | Gula Pasir 1kg | Sembako | Rp 16.500 | P018 | Deterjen 1kg | Rumah Tangga | Rp 22.000 |
| P004 | Tepung Terigu 1kg | Sembako | Rp 12.500 | P019 | Pewangi Pakaian | Rumah Tangga | Rp 14.500 |
| P005 | Mi Instan | Makanan | Rp 3.500 | P020 | Tisu Wajah | Rumah Tangga | Rp 11.000 |
| P006 | Kopi Bubuk | Minuman | Rp 14.500 | P021 | Popok Bayi | Bayi | Rp 68.000 |
| P007 | Teh Celup | Minuman | Rp 9.000 | P022 | Susu Formula | Bayi | Rp 92.000 |
| P008 | Susu UHT 1L | Minuman | Rp 19.500 | P023 | Bubur Bayi | Bayi | Rp 17.500 |
| P009 | Air Mineral 600ml | Minuman | Rp 4.000 | P024 | Air Galon | Minuman | Rp 21.000 |
| P010 | Roti Tawar | Makanan | Rp 16.000 | P025 | Pembersih Lantai | Rumah Tangga | Rp 16.000 |
| P011 | Telur Ayam 1kg | Protein | Rp 31.000 | P026 | Pembersih Piring | Rumah Tangga | Rp 13.500 |
| P012 | Sarden Kaleng | Makanan | Rp 17.500 | P027 | Baterai AA | Elektronik | Rp 14.000 |
| P013 | Biskuit Cokelat | Makanan | Rp 12.000 | P028 | Lampu LED | Elektronik | Rp 28.000 |
| P014 | Cokelat Batang | Makanan | Rp 9.500 | P029 | Pulpen | ATK | Rp 4.000 |
| P015 | Sabun Mandi | Perawatan | Rp 5.500 | P030 | Buku Tulis | ATK | Rp 6.000 |

---

### LAMPIRAN B — Glosarium Metrik

| Istilah | Definisi Operasional | Rumus / Nilai pada Data Ini |
|---|---|---|
| **Support** | Proporsi transaksi yang memuat itemset X | \|X\| / 5.998 · maks 12,72% (Gula Pasir) |
| **Confidence** | Probabilitas membeli Y saat X dibeli | Support(X∪Y) / Support(X) · maks 39,97% |
| **Lift** | Rasio probabilitas vs kebetulan independen | Confidence / Support(Y) · 1 = independen; data: 1,93–3,21 |
| **Leverage** | Kelebihan co-occurrence di atas ekspektasi independen | Support(XY) − S(X)·S(Y) · maks 0,0279 |
| **RFM** | Recency (hari sejak belanja terakhir), Frequency (jumlah trx), Monetary (total belanja) | t_ref 01-01-2026 · median (60, 4, Rp 415.900) |
| **Basket Size** | Jumlah produk unik per transaksi | Rerata 3,05 · median 3 |
| **Basket Value** | Total nilai penjualan per transaksi | Rerata Rp 116.053 · median Rp 88.725 |
| **Attach Rate** | Proporsi transaksi dengan ≥2 produk / pasangan aturan | KPI target +5 pp |
| **Inertia** | Total kuadrat jarak ke centroid (K-Means) | k=3 → 1.774,40 |
| **Silhouette** | Kualitas pemisahan klaster (−1 s/d +1) | k=3 → **0,3607** (maksimum) |
| **Churn Risk** | Pelanggan dengan Recency sangat tinggi & frequency rendah | 266 pelanggan · R mean 212 hari |
| **Uplift** | Kenaikan metrik akibat intervensi (vs baseline) | Proyeksi +Rp 71,57 jt/tahun (+10,3%) |

---

### LAMPIRAN C — Arsitektur Sistem

```
 ┌─────────────────────── SUMBER DATA ────────────────────────┐
 │  P8. UTS_Business Intelligence.xlsx                        │
 │  [Data_Raw 18.513×13] [Data_Produk 30×4] [Data_Pelanggan 1.500×5] │
 └──────────────────────────┬─────────────────────────────────┘
                            ▼
 ┌────────────────── LAPISAN PIPELINE (core/) ─────────────────┐
 │  data_pipeline.py      : load · audit_kualitas · bersihkan  │
 │                          · tambah_basket_size · buat_rfm     │
 │                          · buat_matriks_transaksi            │
 │  apriori_engine.py     : frequent_itemsets (Apriori k≤3)     │
 │                          · association_rules (sup/conf/lift)  │
 │  segmentasi.py         : StandardScaler · evaluasi_k (2–8)   │
 │                          · latih_kmeans · profil · label      │
 │  report_pdf.py         : eksekutif summary PDF               │
 └──────────────────────────┬─────────────────────────────────┘
                            ▼
 ┌──────────── LAPISAN APLIKASI — "NusaRetail Intelligence" ────┐
 │  app.py (Streamlit) · 7 modul: 00 Ringkasan → 06 Rekomendasi │
 │  assets/style.css (tema) · assets/foto.jpeg (identitas)      │
 │  Session state: matriks · rfm · model · filter aktif         │
 └──────────────────────────┬─────────────────────────────────┘
                            ▼
 ┌────────────────── OUTPUT & EKSPOR ──────────────────────────┐
 │  output/Laporan_Analisis_BI.pdf · Data_Clean.csv            │
 │  RFM_Pelanggan.csv · Association_Rules.csv                  │
 └─────────────────────────────────────────────────────────────┘
```

---

### LAMPIRAN D — Parameter Teknis (Reproducibility)

| Komponen | Parameter | Nilai |
|---|---|---|
| Pembersihan | Aturan duplikat / imputasi | 2 tahap `drop_duplicates` · median qty · harga katalog |
| Tanggal acuan RFM | `t_ref` | `max(Transaction_Date) + 1 hari` = **01-01-2026** |
| Apriori | `min_support` / `min_confidence` / `min_lift` / `max_len` | **0,02 / 0,20 / 1,05 / 3** |
| Apriori | Peringkat aturan | `0,5·lift + 0,3·confidence + 0,2·support` |
| Scaler | Metode | `StandardScaler` (mean 0, std 1) |
| K-Means | `k` / `n_init` / `random_state` / kandidat uji | **3** / 10 / 42 / k = 2…8 |
| Label segmen | Kuantil | kuantil 33% & 66% Recency/Frequency/Monetary |
| Basis transaksi | Matriks biner | 5.998 × 30 · sparsity 89,85% |
| Seed & versi | Reproducibility | Seluruh langkah deterministik; hasil identik saat dijalankan ulang |

---

### PENUTUP

Laporan ini membuktikan bahwa **18.513 baris data mentah** yang semula tidak termanfaatkan dapat diubah menjadi **aset keputusan yang terukur**: 25 aturan asosiasi yang menuntun strategi cross-sell, 3 segmen pelanggan dengan playbook pemasaran berbeda, dashboard eksekutif yang menjawab pertanyaan bisnis dalam satu layar, serta proyeksi uplift **Rp 71,57 juta per tahun (+10,3% revenue)** yang seluruh asumsinya dapat diuji melalui mekanisme A/B testing. Integrasi **Apriori × K-Means** pada modul rekomendasi personal merupakan diferensiasi utama: satu-satunya lapisan yang menjawab *"penawaran apa, untuk siapa, kapan"* — inti dari Business Intelligence preskriptif.

---

**Caecillia Jessica Kinbenu — NIM 51230131**
**Program Studi Teknologi Informasi · Mata Kuliah Business Intelligence · Semester 7**

![Foto Profil Penyusun](../assets/foto.jpeg)

*— Akhir Dokumen —*
