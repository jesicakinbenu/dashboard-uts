"""Sistem Business Intelligence - Studi Kasus Analisis Data Transaksi Toko.

Aplikasi ini mengintegrasikan seluruh tahap UTS:
  Tahap 1 : Business Understanding & EDA
  Tahap 2 : Data Preprocessing & Feature Engineering
  Tahap 3 : Apriori / Market Basket Analysis
  Tahap 4 : K-Means / Segmentasi Pelanggan
  Tahap 5 : Dashboard Business Intelligence
  Tahap 6 : Rekomendasi Keputusan Bisnis

Tema visual "Soft Sage" dengan font Plus Jakarta Sans & Fraunces.
"""

from __future__ import annotations

import base64
import os
import sys

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import data_pipeline as dp
from core import apriori_engine as ae
from core import segmentasi as seg
from core import report_pdf as rp
from core.config import OUTPUT_DIR

# ---------------------------------------------------------------------------
# Konfigurasi halaman & tema
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="NusaRetail Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
with open(os.path.join(ASSETS, "style.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

PALETTE = ["#38BDF8", "#10B981", "#C9A24B", "#F59E0B",
           "#818CF8", "#2DD4BF", "#EF4444", "#A78BFA",
           "#F472B6", "#A3E635"]

FONT_SANS = "Plus Jakarta Sans, Segoe UI, sans-serif"
FONT_MONO = "JetBrains Mono, Consolas, monospace"

PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(30,41,59,0.35)",
    font=dict(family=FONT_SANS, color="#CBD5E1", size=12),
    title=dict(font=dict(family=FONT_SANS, color="#F8FAFC", size=15, weight=700),
               x=0.01, xanchor="left"),
    xaxis=dict(gridcolor="rgba(51,65,85,0.55)", zerolinecolor="rgba(56,189,248,0.35)",
               tickfont=dict(size=11, color="#94A3B8"), tickformat=",.0f",
               linecolor="#334155", mirror=True),
    yaxis=dict(gridcolor="rgba(51,65,85,0.55)", zerolinecolor="rgba(56,189,248,0.35)",
               tickfont=dict(size=11, color="#94A3B8"), tickformat=",.0f",
               linecolor="#334155", mirror=True),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#CBD5E1", size=11),
                orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    margin=dict(l=70, r=30, t=64, b=64),
    height=400,
    separators=",.",
    hoverlabel=dict(bgcolor="#1E293B", bordercolor="#38BDF8",
                    font=dict(family=FONT_SANS, size=12, color="#F8FAFC")),
    colorway=PALETTE,
)
px.defaults.template = None
px.defaults.color_discrete_sequence = PALETTE


def gaya(fig: go.Figure, tinggi: int | None = None,
         mr: int | None = None, ml: int | None = None,
         mb: int | None = None, mt: int | None = None) -> go.Figure:
    fig.update_layout(template=None, **PLOTLY_TEMPLATE)
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    if tinggi:
        fig.update_layout(height=tinggi)
    m = {}
    if mr is not None:
        m["r"] = mr
    if ml is not None:
        m["l"] = ml
    if mb is not None:
        m["b"] = mb
    if mt is not None:
        m["t"] = mt
    if m:
        fig.update_layout(margin=m)
    return fig


# ---------------------------------------------------------------------------
# Format angka gaya Indonesia: pemisah ribuan titik ("1.000.000"),
# desimal koma ("3,05"). Berlaku untuk KPI, tabel, teks, label, hover & PDF.
# ---------------------------------------------------------------------------

def _rib(n: int) -> str:
    """Kelompokkan ribuan dengan titik: 696085375 -> 696.085.375."""
    return f"{n:,}".replace(",", ".")


def fmt_rupiah(x: float) -> str:
    return "Rp " + _rib(int(round(x)))


def fmt_angka(x: float) -> str:
    return _rib(int(round(x)))


def fmt_des(x: float, n: int = 2) -> str:
    s = f"{float(x):,.{n}f}"          # gaya AS: 1,234.56
    s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return s


def fmt_pct(x: float, n: int = 2) -> str:
    return fmt_des(x, n) + "%"


def ticks_ribuan(vals, maks: int = 4, nol: bool = True) -> tuple[list, list]:
    """(tickvals, ticktext) gaya Indonesia dengan jumlah tick terbatas.

    Dipakai pada sumbu nilai uang/angka besar agar label panjang
    (mis. 60.000.000) tidak bertumpuk di lebar separuh layar.
    """
    import math
    hi = float(np.nanmax(vals)) if len(vals) else 0.0
    lo = 0.0 if nol else float(np.nanmin(vals))
    if not np.isfinite(hi) or hi <= lo:
        hi = lo + 1.0
    span = hi - lo
    kasar = span / max(maks, 1)
    p = 10.0 ** math.floor(math.log10(kasar)) if kasar > 0 else 1.0
    step = 10.0 * p
    for m in (1, 2, 5):
        if kasar <= m * p * (1 + 1e-9):
            step = m * p
            break
    start = math.ceil(lo / step) * step
    tv, v = [], start
    while v <= hi + 1e-6 * step:
        tv.append(round(v, 6))
        v += step
    if not tv:
        tv, v = [lo, hi], hi
    tt = [_rib(int(round(t))) if abs(t - round(t)) < 1e-9 else fmt_des(t, 2)
          for t in tv]
    return tv, tt


# ---------------------------------------------------------------------------
# Komponen tampilan
# ---------------------------------------------------------------------------

def kartu_kpi(items: list[tuple[str, str, str]]) -> None:
    """Kartu KPI berwarna. items = [(label, nilai, warna_hex), ...]."""
    cells = "".join(
        f'<div class="kpi" style="--k:{w}"><div class="v">{v}</div>'
        f'<div class="l">{l}</div></div>'
        for l, v, w in items)
    st.markdown(f'<div class="kpi-grid">{cells}</div>', unsafe_allow_html=True)


def tabel_html(df: pd.DataFrame, num_cols=(), wrap_cols=()) -> str:
    """Tabel HTML rapi; nilai diasumsikan string berformat (tanpa titik)."""
    cols = list(df.columns)
    th = "".join(f'<th class="{"num" if c in num_cols else ""}">{c}</th>'
                 for c in cols)
    rows = []
    for _, r in df.iterrows():
        tds = "".join(
            f'<td class="{("num" if c in num_cols else ("wrap" if c in wrap_cols else ""))}">'
            f"{r[c]}</td>"
            for c in cols)
        rows.append(f"<tr>{tds}</tr>")
    return ('<div class="tbl-wrap"><table class="tbl"><thead>'
            f"<tr>{th}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>")


def hero(judul: str, sub: str, warna: str = "#38BDF8") -> None:
    st.markdown(
        f'<div class="hero" style="--acc:{warna}"><h1>{judul}</h1>'
        f"<p>{sub}</p></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Memuat & memproses data (di-cache agar cepat)
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def siapkan_semua():
    raw = dp.load_raw()
    produk = dp.load_produk()
    pelanggan = dp.load_pelanggan()
    audit = dp.audit_kualitas(raw)
    clean = dp.bersihkan_data(raw, produk)
    clean = dp.tambah_basket_size(clean)
    rfm, tgl_acuan = dp.buat_rfm(clean)
    matriks = dp.buat_matriks_transaksi(clean)
    return raw, produk, pelanggan, audit, clean, rfm, tgl_acuan, matriks


@st.cache_data(show_spinner=False)
def jalankan_apriori_cached(matriks_key, min_sup, min_conf, min_lift, max_len=3):
    return ae.jalankan_apriori(st.session_state["matriks"], min_sup, min_conf, min_lift,
                               max_len=max_len)


@st.cache_data(show_spinner=False)
def jalankan_kmeans_cached(rfm_key, k, random_state=42):
    rfm = st.session_state["rfm"]
    Xs, scaler, kolom = seg.siapkan_fitur(rfm)
    ev = seg.evaluasi_k(Xs)
    km, labels = seg.latih_kmeans(Xs, k, random_state)
    prof = seg.label_segmen(seg.profil_segmen(rfm, labels))
    return Xs, ev, labels, prof


# ---------------------------------------------------------------------------
# Inisialisasi
# ---------------------------------------------------------------------------

if "init" not in st.session_state:
    raw, produk, pelanggan, audit, clean, rfm, tgl_acuan, matriks = siapkan_semua()
    st.session_state.update(dict(
        raw=raw, produk=produk, pelanggan=pelanggan, audit=audit,
        clean=clean, rfm=rfm, tgl_acuan=tgl_acuan, matriks=matriks,
        init=True,
    ))
else:
    raw = st.session_state["raw"]
    produk = st.session_state["produk"]
    pelanggan = st.session_state["pelanggan"]
    audit = st.session_state["audit"]
    clean = st.session_state["clean"]
    rfm = st.session_state["rfm"]
    tgl_acuan = st.session_state["tgl_acuan"]
    matriks = st.session_state["matriks"]

nama_produk = dict(zip(produk["Product_ID"], produk["Product_Name"]))


def label_item(items) -> str:
    if isinstance(items, str):
        items = [x.strip() for x in items.split(",")]
    return ", ".join(nama_produk.get(i, i) for i in items)


def pendek(teks: str, maks: int = 22) -> str:
    return teks if len(teks) <= maks else teks[: maks - 1] + "…"


# ---------------------------------------------------------------------------
# Identitas & Cover
# ---------------------------------------------------------------------------

IDENTITAS = {
    "nama": "Caecillia Jessica Kinbenu",
    "nim": "51230131",
    "prodi": "Teknologi Informasi",
    "semester": "7",
    "kegiatan": "Ujian Tengah Semester",
    "mata_kuliah": "Business Intelligence",
}


def cari_foto() -> str | None:
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(ASSETS, f"foto.{ext}")
        if os.path.exists(p):
            return p
    return None


def foto_base64(sisi: int = 84) -> str | None:
    p = cari_foto()
    if not p:
        return None
    with open(p, "rb") as fh:
        return base64.b64encode(fh.read()).decode()


def tampilkan_cover() -> None:
    foto = cari_foto()
    if foto:
        with open(foto, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        ext = foto.rsplit(".", 1)[-1].lower()
        mime = {"jpg": "jpeg", "jpeg": "jpeg", "png": "png", "webp": "webp"}[ext]
        foto_html = (f'<img class="foto-bingkai" '
                     f'src="data:image/{mime};base64,{b64}" alt="Foto">')
    else:
        foto_html = '<div class="foto-mono">CK</div>'

    rev = fmt_rupiah(clean["Line_Total"].sum())
    trx = fmt_angka(clean["Transaction_ID"].nunique())

    st.markdown(
        f"""
<div class="cover-wrap">
  <div class="cover-card">
    <div class="cov-head">
      <span class="cov-brand"><span class="dot"></span>
        Business Intelligence &middot; Laporan UTS</span>
    </div>
    <div class="cov-rule"></div>
    <div class="cov-body">
      <div class="cov-main">
        <div class="cov-eyebrow">Laporan Analisis Sistem &amp; Integrasi Data Mining</div>
        <div class="cov-title">BUSINESS INTELLIGENCE DASHBOARD
          <span>Sistem Terintegrasi Analitika Ritel</span></div>
        <div class="cov-sub">Strategi <b>Cross-Selling (Apriori)</b> &amp;
          <b>Segmentasi Pelanggan (K-Means RFM)</b>
          Berbasis Data Transaksi Ritel 2025</div>
        <div class="cov-meta">
          <div class="cov-meta-h">&#9632; Dokumen Metadata</div>
          <div class="cov-row"><span class="k">Mata Kuliah</span>
            <span class="v">Business Intelligence</span></div>
          <div class="cov-row"><span class="k">Kegiatan</span>
            <span class="v">{IDENTITAS['kegiatan']} &middot; Semester {IDENTITAS['semester']}</span></div>
          <div class="cov-row"><span class="k">Program Studi</span>
            <span class="v">{IDENTITAS['prodi']}</span></div>
          <div class="cov-row"><span class="k">Objek Studi</span>
            <span class="v">Data Transaksi Toko Ritel
              <span class="teal">(18.270 baris &middot; 30 produk)</span></span></div>
          <div class="cov-row"><span class="k">Metode</span>
            <span class="v">EDA &middot; Preprocessing &middot; Apriori &middot; K-Means RFM</span></div>
        </div>
      </div>
      <div class="cov-side">
        {foto_html}
        <div class="catatan-foto">Penyusun</div>
        <div class="identitas">
          <div class="baris"><span class="label">Nama</span>
            <span class="nilai">{IDENTITAS['nama']}</span></div>
          <div class="baris"><span class="label">NIM</span>
            <span class="nilai">{IDENTITAS['nim']}</span></div>
          <div class="baris"><span class="label">Program Studi</span>
            <span class="nilai" style="font-size:.86rem">{IDENTITAS['prodi']}</span></div>
        </div>
      </div>
    </div>
    <div class="cover-stats">
      <div class="cs"><div class="n">{rev}</div><div class="l">Total Revenue</div></div>
      <div class="cs"><div class="n">{trx}</div><div class="l">Transaksi Unik</div></div>
      <div class="cs"><div class="n">25</div><div class="l">Aturan Apriori</div></div>
      <div class="cs"><div class="n">3</div><div class="l">Segmen RFM</div></div>
    </div>
    <div class="cover-foot">
      <span>Semester 7 &middot; UTS Business Intelligence</span>
      <span>{IDENTITAS['nama']} &middot; {IDENTITAS['nim']}</span>
      <span>Dokumen v1.0 &mdash; Final</span>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")
    _, kol_b, _ = st.columns([1.2, 1, 1.2])
    if kol_b.button("Masuk ke Sistem Analisis", type="primary",
                    use_container_width=True):
        st.session_state["sudah_masuk"] = True
        st.rerun()


# ---------------------------------------------------------------------------
# Gerbang cover
# ---------------------------------------------------------------------------

if not st.session_state.get("sudah_masuk", False):
    tampilkan_cover()
    st.stop()

# ---------------------------------------------------------------------------
# Topbar + menu navigasi pil
# ---------------------------------------------------------------------------

st.markdown(
    f"""
<div class="topbar">
  <div><span class="tb-logo">◆</span><span class="tb-brand">NusaRetail Intelligence</span>
  <span class="tb-sub">Business Intelligence Suite</span></div>
  <div class="tb-who">{IDENTITAS['nama']} &middot; {IDENTITAS['nim']}</div>
</div>
""",
    unsafe_allow_html=True,
)

NAV = [
    "00 · Ringkasan",
    "01 · EDA & Pemahaman",
    "02 · Preprocessing",
    "03 · Apriori",
    "04 · K-Means",
    "05 · Dashboard",
    "06 · Rekomendasi",
]

st.markdown('<div class="nav-wrap"></div>', unsafe_allow_html=True)
halaman = st.radio("Menu analisis", NAV, horizontal=True,
                   label_visibility="collapsed", key="nav_utama")

# ---------------------------------------------------------------------------
# Sidebar: identitas, info data, ekspor
# ---------------------------------------------------------------------------

with st.sidebar:
    b64 = foto_base64()
    if b64:
        img = (f'<img src="data:image/jpeg;base64,{b64}" alt="Foto">')
    else:
        img = '<div class="id-fallback">CK</div>'
    st.markdown(
        f"""
<div class="id-card">
  {img}
  <div class="id-name">{IDENTITAS['nama']}</div>
  <div class="id-meta">{IDENTITAS['nim']} &middot; Semester {IDENTITAS['semester']}</div>
  <div class="id-meta">Teknologi Informasi</div>
</div>
""",
        unsafe_allow_html=True,
    )

    n_trx = clean["Transaction_ID"].nunique()
    n_pel = clean.loc[clean.Customer_ID != "UNKNOWN", "Customer_ID"].nunique()
    st.markdown(
        f"""
<div class="side-info">
  Periode data: <b>{clean['Transaction_Date'].min():%b %Y} –
  {clean['Transaction_Date'].max():%b %Y}</b><br>
  Baris bersih: <b>{fmt_angka(len(clean))}</b><br>
  Transaksi: <b>{fmt_angka(n_trx)}</b> &middot;
  Pelanggan: <b>{fmt_angka(n_pel)}</b><br>
  Total penjualan: <b>{fmt_rupiah(clean['Line_Total'].sum())}</b>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("#### Ekspor Laporan")
    if st.button("Buat Laporan PDF", use_container_width=True):
        with st.spinner("Menyusun laporan PDF..."):
            try:
                res = ae.jalankan_apriori(matriks, 0.02, 0.2, 1.05,
                                          max_len=st.session_state.get("max_len", 3))
                rules = res["rules"]
                if not rules.empty:
                    rules = rules.copy()
                    rules["Aturan"] = rules.apply(
                        lambda r: f"{label_item(r['antecedents'])} → "
                                  f"{label_item(r['consequents'])}", axis=1)
                _, _, _, prof = jalankan_kmeans_cached("rfm", 3)
                path_pdf = rp.buat_laporan(
                    os.path.join(OUTPUT_DIR, "Laporan_Analisis_BI.pdf"),
                    identitas=IDENTITAS,
                    kpi={
                        "total_penjualan": fmt_rupiah(clean["Line_Total"].sum()),
                        "transaksi": fmt_angka(clean["Transaction_ID"].nunique()),
                        "pelanggan": fmt_angka(
                            clean.loc[clean.Customer_ID != "UNKNOWN",
                                      "Customer_ID"].nunique()),
                        "basket": (fmt_des(clean.groupby('Transaction_ID')
                                            ['Product_ID'].nunique().mean())
                                   + " produk"),
                        "produk": fmt_angka(clean["Product_ID"].nunique()),
                    },
                    ringkas_preprocessing=pd.DataFrame([
                        {"Aspek": "Jumlah baris",
                         "Sebelum": fmt_angka(audit["jumlah_baris_awal"]),
                         "Sesudah": fmt_angka(len(clean))},
                        {"Aspek": "Sel kosong",
                         "Sebelum": fmt_angka(audit["missing_total"]),
                         "Sesudah": "0"},
                        {"Aspek": "Baris duplikat",
                         "Sebelum": fmt_angka(audit["duplikat_eksekak"]),
                         "Sesudah": "0"},
                        {"Aspek": "Qty tidak valid",
                         "Sebelum": fmt_angka(audit["quantity_invalid"]),
                         "Sesudah": "0"},
                        {"Aspek": "Harga tidak wajar",
                         "Sebelum": fmt_angka(audit["harga_invalid"]),
                         "Sesudah": "0"},
                        {"Aspek": "Line_Total tak konsisten",
                         "Sebelum": fmt_angka(audit["line_total_tidak_konsisten"]),
                         "Sesudah": "Konsisten"},
                    ]),
                    rules_top=rules.head(10) if not rules.empty else pd.DataFrame(
                        columns=["Aturan", "support", "confidence", "lift"]),
                    prof_segmen=prof,
                    rekomendasi=pd.DataFrame([
                        {"Prioritas": 1,
                         "Tindakan": "Bundling & penempatan rak (produk lift tertinggi)",
                         "Urgensi": "Tinggi", "Kemudahan": "Mudah"},
                        {"Prioritas": 2,
                         "Tindakan": "Win-back campaign segmen Churn Risk",
                         "Urgensi": "Tinggi", "Kemudahan": "Sedang"},
                        {"Prioritas": 3,
                         "Tindakan": "Program loyalitas Loyal Customers",
                         "Urgensi": "Sedang", "Kemudahan": "Sedang"},
                        {"Prioritas": 4,
                         "Tindakan": "Cross-sell onboarding New Customers",
                         "Urgensi": "Sedang", "Kemudahan": "Mudah"},
                    ]),
                    temuan=[
                        f"Data mentah {fmt_angka(audit['jumlah_baris_awal'])} baris dibersihkan "
                        f"menjadi {fmt_angka(len(clean))} baris; {fmt_angka(audit['duplikat_eksekak'])} duplikat "
                        f"dan {fmt_angka(audit['missing_total'])} sel kosong ditangani.",
                        "Aturan asosiasi terkuat ditemukan antar produk dengan lift "
                        "jauh di atas 1 (lihat bab Apriori).",
                        f"Segmentasi K-Means menghasilkan segmen Loyal, Potential, dan "
                        f"Churn Risk berdasarkan profil RFM.",
                        "Rata-rata basket_size sekitar 3 produk per transaksi - peluang "
                        "cross-selling.",
                    ])
                with open(path_pdf, "rb") as fh:
                    st.session_state["pdf_bytes"] = fh.read()
                st.success("Laporan PDF siap diunduh.")
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")

    if st.session_state.get("pdf_bytes"):
        st.download_button("Unduh Laporan PDF", st.session_state["pdf_bytes"],
                           "Laporan_Analisis_BI.pdf", "application/pdf",
                           use_container_width=True)

    with st.expander("Unduh Data (CSV)"):
        st.download_button("Data Bersih", clean.to_csv(index=False).encode("utf-8-sig"),
                           "Data_Clean.csv", "text/csv", use_container_width=True)
        st.download_button("RFM Pelanggan", rfm.to_csv(index=False).encode("utf-8-sig"),
                           "RFM_Pelanggan.csv", "text/csv", use_container_width=True)
        res_def = ae.jalankan_apriori(matriks, 0.02, 0.2, 1.05,
                                      max_len=st.session_state.get("max_len", 3))
        if not res_def["rules"].empty:
            rr = res_def["rules"].head(20).copy()
            rr["Aturan"] = rr.apply(
                lambda r: f"{label_item(r['antecedents'])} → "
                          f"{label_item(r['consequents'])}", axis=1)
            st.download_button("Aturan Apriori",
                               rr.to_csv(index=False).encode("utf-8-sig"),
                               "Aturan_Apriori.csv", "text/csv",
                               use_container_width=True)


# ---------------------------------------------------------------------------
# Halaman 00 - Ringkasan
# ---------------------------------------------------------------------------

def halaman_ringkasan():
    hero("Ringkasan Eksekutif",
         "Gambaran menyeluruh hasil analisis: EDA, preprocessing, Apriori, "
         "K-Means, hingga rekomendasi bisnis.", "#38BDF8")

    kartu_kpi([
        ("Total Penjualan", fmt_rupiah(clean["Line_Total"].sum()), "#38BDF8"),
        ("Transaksi Unik", fmt_angka(clean["Transaction_ID"].nunique()), "#C9A24B"),
        ("Pelanggan Unik", fmt_angka(clean.loc[clean.Customer_ID != 'UNKNOWN',
                                               'Customer_ID'].nunique()), "#818CF8"),
        ("Produk", fmt_angka(clean["Product_ID"].nunique()), "#F59E0B"),
    ])

    st.markdown("### Peta Jalan Analisis")
    peta = [
        ("Tahap 1 - EDA", "Memahami masalah bisnis, eksplorasi & temuan kualitas data.", "10%"),
        ("Tahap 2 - Preprocessing", "Pembersihan, transformasi, RFM & basket_size.", "25%"),
        ("Tahap 3 - Apriori", "Market basket: frequent itemsets & aturan asosiasi.", "20%"),
        ("Tahap 4 - K-Means", "Segmentasi pelanggan berbasis RFM, Elbow & Silhouette.", "20%"),
        ("Tahap 5 - Dashboard BI", "KPI, tren, integrasi Apriori x segmen, filter interaktif.", "15%"),
        ("Tahap 6 - Rekomendasi", "Strategi preskriptif, prioritas & estimasi dampak.", "10%"),
    ]
    cols = st.columns(2)
    for i, (judul, isi, bobot) in enumerate(peta):
        with cols[i % 2].expander(f"{judul}  -  Bobot {bobot}"):
            st.write(isi)

    st.markdown("### Tren Penjualan & Produk Teratas")
    v1, v2 = st.columns(2)
    bulanan = (clean.set_index("Transaction_Date")
               .resample("ME")["Line_Total"].sum().reset_index())
    bulanan["Bulan"] = bulanan["Transaction_Date"].dt.strftime("%b")
    with v1:
        fig = px.line(bulanan, x="Bulan", y="Line_Total", markers=True,
                      title="Tren Penjualan Bulanan (2025)",
                      color_discrete_sequence=["#10B981"])
        fig.update_traces(line=dict(width=3),
                          hovertemplate="%{x}: Rp %{y:,.0f}<extra></extra>")
        tv, tt = ticks_ribuan(bulanan["Line_Total"], maks=4)
        fig.update_yaxes(tickvals=tv, ticktext=tt, title_text="Penjualan (Rp)")
        gaya(fig, tinggi=400, mb=70)
        st.plotly_chart(fig, use_container_width=True)
    with v2:
        tp = (clean.groupby("Product_Name")["Line_Total"].sum()
              .sort_values(ascending=False).head(8).reset_index())
        tp["LabelNilai"] = tp["Line_Total"].map(fmt_angka)
        fig = px.bar(tp, x="Line_Total", y="Product_Name", orientation="h",
                     text="LabelNilai", title="8 Produk Penjualan Tertinggi",
                     labels={"Line_Total": "Penjualan (Rp)", "Product_Name": "Produk"},
                     color_discrete_sequence=["#C9A24B"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(tp["Line_Total"], maks=3)
        fig.update_xaxes(tickvals=tv, ticktext=tt, range=[0, tp["Line_Total"].max() * 1.22])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}<br>Rp %{x:,.0f}<extra></extra>")
        gaya(fig, tinggi=400, mr=100, ml=110)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Ringkasan Temuan Kunci")
    res = ae.jalankan_apriori(matriks, 0.02, 0.2, 1.05,
                              max_len=st.session_state.get("max_len", 3))
    rules = res["rules"]
    top_rule = "belum cukup data"
    if not rules.empty:
        r0 = rules.iloc[0]
        top_rule = (f"pasangan **{label_item(r0['antecedents'])} → "
                    f"{label_item(r0['consequents'])}** (lift {fmt_des(r0['lift'])}, "
                    f"confidence {fmt_pct(r0['confidence'] * 100, 1)})")
    _, _, _, prof = jalankan_kmeans_cached("rfm", 3)
    seg_count = prof["label_segmen"].value_counts().index[0]
    st.markdown(
        f"""
- **Kualitas data:** {fmt_angka(audit['duplikat_eksekak'])} baris duplikat, {fmt_angka(audit['missing_total'])} sel kosong,
  {fmt_angka(audit['quantity_invalid'])} nilai Quantity tidak valid, dan {fmt_angka(audit['harga_invalid'])} harga tidak wajar
  ditemukan pada {fmt_angka(audit['jumlah_baris_awal'])} baris data mentah - semuanya telah ditangani.
- **Pola belanja:** aturan paling menarik adalah {top_rule}.
- **Segmentasi:** k terbaik menurut Silhouette = **{int(ev_best_k())} klaster**; segmen terbesar **{seg_count}**.
- **Implikasi:** hasil analisis menjadi dasar rekomendasi bundling, penempatan rak, dan retensi pelanggan.
        """
    )


def ev_best_k() -> int:
    _, ev, _, _ = jalankan_kmeans_cached("rfm", 3)
    return int(ev.sort_values("silhouette", ascending=False).iloc[0]["k"])


# ---------------------------------------------------------------------------
# Halaman 01 - EDA
# ---------------------------------------------------------------------------

def halaman_eda():
    hero("01 - Business Understanding & EDA",
         "Memahami permasalahan bisnis dan mengeksplorasi karakteristik data transaksi.",
         "#818CF8")

    st.markdown("### 1a. Permasalahan Bisnis & Pertanyaan Analitis")
    st.markdown(
        """
Perusahaan ritel hanya memakai data transaksi untuk **laporan rutin**, belum untuk memahami
pola belanja, kombinasi produk, segmentasi pelanggan, dan strategi pemasaran. Data juga berpotensi
bermasalah (missing, duplikat, outlier, format tidak konsisten).

**Pertanyaan bisnis yang dirumuskan:**
1. **Produk apa yang sering dibeli bersama?** - untuk bundling & penempatan rak (Apriori).
2. **Segmen pelanggan mana yang paling bernilai dan mana yang berisiko hilang?** - retensi (K-Means).
3. **Kapan penjualan meningkat & produk mana yang mendominasi?** - perencanaan stok & promosi (EDA).
4. **Bagaimana karakteristik transaksi (basket_size) memengaruhi nilai penjualan?** - strategi cross-sell.
        """
    )

    st.markdown("### 1b. Profil Data (Sebelum Pembersihan)")
    kartu_kpi([
        ("Baris x Kolom",
         f"{fmt_angka(audit['jumlah_baris_awal'])} x {fmt_angka(audit['jumlah_kolom'])}",
         "#818CF8"),
        ("Transaksi Unik", fmt_angka(audit["transaksi_unik"]), "#38BDF8"),
        ("Pelanggan Unik", fmt_angka(audit["pelanggan_unik"]), "#C9A24B"),
        ("Rentang Tanggal",
         f"{audit['tanggal_min']:%d/%m/%y} - {audit['tanggal_maks']:%d/%m/%y}", "#F59E0B"),
    ])

    st.markdown("### 1c. Statistik Deskriptif")
    desc = raw[["Quantity", "Unit_Price", "Discount_Rate", "Line_Total"]].describe().T
    desc = desc.rename(columns={"count": "Jumlah", "mean": "Rata-rata", "std": "Std",
                                "min": "Min", "25%": "Q1", "50%": "Median",
                                "75%": "Q3", "max": "Max"})
    desc_fmt = desc.copy()
    for c in desc_fmt.columns:
        if c == "Jumlah":
            desc_fmt[c] = desc[c].map(fmt_angka)
        elif c == "Std":
            desc_fmt[c] = desc[c].map(lambda v: fmt_des(v, 1))
        else:
            desc_fmt[c] = desc[c].map(lambda v: fmt_des(v, 1))
    desc_fmt.insert(0, "Statistik", desc_fmt.index)
    st.markdown(tabel_html(desc_fmt.reset_index(drop=True),
                           num_cols=["Jumlah", "Rata-rata", "Std", "Min", "Q1",
                                     "Median", "Q3", "Max"]),
                unsafe_allow_html=True)

    st.markdown("### 1d. Kualitas Data (Missing, Duplikat, Outlier)")
    q1, q2 = st.columns(2)
    miss = pd.Series(audit["missing_per_kolom"])
    miss = miss[miss > 0].sort_values(ascending=False)
    with q1:
        md = pd.DataFrame({"Kolom": miss.index, "Jumlah": miss.values,
                           "Label": [fmt_angka(v) for v in miss.values]})
        fig = px.bar(md, x="Jumlah", y="Kolom", orientation="h", text="Label",
                     title="Missing Values per Kolom",
                     color_discrete_sequence=["#F59E0B"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        vmax = float(md["Jumlah"].max())
        fig.update_xaxes(tickvals=ticks_ribuan(md["Jumlah"], maks=4)[0],
                         ticktext=ticks_ribuan(md["Jumlah"], maks=4)[1],
                         range=[0, vmax * 1.25])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}: %{x} sel<extra></extra>")
        gaya(fig, tinggi=390, mr=70, ml=130)
        st.plotly_chart(fig, use_container_width=True)
    with q2:
        masalah = pd.DataFrame({
            "Jenis": ["Duplikat Baris", "Sel Kosong", "Qty Tidak Valid",
                      "Harga Tidak Wajar", "Line_Total Tak Konsisten"],
            "Jumlah": [audit["duplikat_eksekak"], audit["missing_total"],
                       audit["quantity_invalid"], audit["harga_invalid"],
                       audit["line_total_tidak_konsisten"]],
        })
        masalah["Label"] = masalah["Jumlah"].map(fmt_angka)
        fig = px.bar(masalah, x="Jumlah", y="Jenis", orientation="h", text="Label",
                     title="Rekap Masalah Kualitas Data",
                     color_discrete_sequence=["#C9A24B"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        vmax = float(masalah["Jumlah"].max())
        fig.update_xaxes(tickvals=ticks_ribuan(masalah["Jumlah"], maks=4)[0],
                         ticktext=ticks_ribuan(masalah["Jumlah"], maks=4)[1],
                         range=[0, vmax * 1.25])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}: %{x} baris<extra></extra>")
        gaya(fig, tinggi=390, mr=70, ml=165)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 1e. Visualisasi Awal")
    v1, v2 = st.columns(2)
    bulanan = (clean.set_index("Transaction_Date")
               .resample("ME")["Line_Total"].sum().reset_index())
    bulanan["Bulan"] = bulanan["Transaction_Date"].dt.strftime("%b")
    with v1:
        fig = px.area(bulanan, x="Bulan", y="Line_Total",
                      title="Tren Penjualan Bulanan (2025)",
                      color_discrete_sequence=["#10B981"])
        fig.update_traces(line=dict(width=3),
                          hovertemplate="%{x}: Rp %{y:,.0f}<extra></extra>")
        tv, tt = ticks_ribuan(bulanan["Line_Total"], maks=4)
        fig.update_yaxes(tickvals=tv, ticktext=tt, title_text="Penjualan (Rp)")
        gaya(fig, tinggi=400, mb=70)
        st.plotly_chart(fig, use_container_width=True)
    with v2:
        top_produk = (clean.groupby("Product_Name")["Line_Total"].sum()
                      .sort_values(ascending=False).head(8).reset_index())
        top_produk["LabelNilai"] = top_produk["Line_Total"].map(fmt_angka)
        fig = px.bar(top_produk, x="Line_Total", y="Product_Name", orientation="h",
                     text="LabelNilai", title="8 Produk Penjualan Tertinggi",
                     labels={"Line_Total": "Penjualan (Rp)", "Product_Name": "Produk"},
                     color_discrete_sequence=["#818CF8"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(top_produk["Line_Total"], maks=3)
        fig.update_xaxes(tickvals=tv, ticktext=tt,
                         range=[0, top_produk["Line_Total"].max() * 1.22])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}<br>Rp %{x:,.0f}<extra></extra>")
        gaya(fig, tinggi=400, mr=100, ml=110)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 1f. Temuan Awal (min. 3)")
    st.markdown(
        f"""
1. **Pola penjualan relatif stabil sepanjang 2025** dengan sedikit kenaikan menjelang akhir tahun,
   menandakan kebutuhan promosi terjadwal pada periode tertentu.
2. **Konsentrasi produk** - beberapa produk berkontribusi besar pada pendapatan; produk harga
   lebih tinggi (kategori Sembako & Elektronik) mendominasi nilai, bukan volume transaksi.
3. **Masalah kualitas nyata & terukur** - ditemukan {fmt_angka(audit['duplikat_eksekak'])} duplikat,
   {fmt_angka(audit['missing_total'])} sel kosong, dan outlier ekstrem (Quantity 999, harga 999999)
   yang jika dibiarkan akan menaikkan nilai penjualan secara artifisial.
4. **Basket multi-item umum** - rata-rata tiap transaksi memuat sekitar 3 produk berbeda,
   peluang nyata untuk cross-selling via bundling.
        """
    )


# ---------------------------------------------------------------------------
# Halaman 02 - Preprocessing
# ---------------------------------------------------------------------------

def halaman_preprocessing():
    hero("02 - Data Preprocessing & Feature Engineering",
         "Pembersihan transparan, transformasi format, penanganan outlier, RFM & basket_size.",
         "#C9A24B")

    st.markdown("### 2a. Ringkasan Perubahan Data (Sebelum → Sesudah)")
    before = audit["jumlah_baris_awal"]
    after = len(clean)
    ringkasan = pd.DataFrame([
        {"Aspek": "Jumlah baris", "Sebelum": fmt_angka(before),
         "Sesudah": fmt_angka(after),
         "Aksi": f"Menghapus {fmt_angka(before - after)} baris (duplikat + invalid)"},
        {"Aspek": "Sel kosong", "Sebelum": fmt_angka(audit["missing_total"]),
         "Sesudah": "0",
         "Aksi": "Imputasi median/harga katalog + modus kategori"},
        {"Aspek": "Baris duplikat", "Sebelum": fmt_angka(audit["duplikat_eksekak"]),
         "Sesudah": "0", "Aksi": "Drop duplikat persis setelah normalisasi teks"},
        {"Aspek": "Qty tidak valid", "Sebelum": fmt_angka(audit["quantity_invalid"]),
         "Sesudah": "0", "Aksi": "Nilai <=0 atau >=100 diganti median qty"},
        {"Aspek": "Harga tidak wajar", "Sebelum": fmt_angka(audit["harga_invalid"]),
         "Sesudah": "0", "Aksi": "Diganti harga referensi katalog produk"},
        {"Aspek": "Inkonsistensi teks", "Sebelum": "Kategori & pembayaran campur",
         "Sesudah": "Seragam (Title Case + QRIS)",
         "Aksi": "Normalisasi huruf/spasi & mapping kategori ke katalog"},
        {"Aspek": "Line_Total", "Sebelum": "16 baris tidak konsisten",
         "Sesudah": "Konsisten", "Aksi": "Dihitung ulang Qty x Harga x (1 - Diskon)"},
    ])
    st.markdown(tabel_html(ringkasan, num_cols=["Sebelum", "Sesudah"],
                           wrap_cols=["Aksi"]), unsafe_allow_html=True)

    st.markdown("### 2b. Alasan Metode Penanganan")
    st.markdown(
        """
- **Missing Customer_ID** → diisi `UNKNOWN` (bukan dihapus) agar baris transaksi tetap
  berkontribusi pada analisis produk/Apriori; pelanggan tak dikenal dikeluarkan dari RFM.
- **Duplikat** → dihapus karena mewakili pencatatan ganda, bukan transaksi nyata.
- **Outlier Quantity/harga ekstrem** → diimputasi (bukan dibuang) karena tetap mewakili
  produk nyata; imputasi median/harga katalog menjaga distribusi tanpa memicu bias nilai.
- **Kategori/pembayaran campur huruf** → diseragamkan agar agregasi tidak terpecah.
- **Line_Total** → dihitung ulang agar konsisten secara finansial.
        """
    )

    st.markdown("### 2c. Fitur Engineering")
    bs = (clean.groupby("Transaction_ID")["Product_ID"].nunique()
          .rename("basket_size").reset_index())
    kartu_kpi([
        ("Rata-rata basket_size", fmt_des(bs["basket_size"].mean()) + " produk", "#38BDF8"),
        ("Median basket_size", fmt_angka(bs["basket_size"].median()) + " produk", "#C9A24B"),
        ("Maks basket_size", fmt_angka(bs["basket_size"].max()) + " produk", "#818CF8"),
        ("Pelanggan ter-RFM", fmt_angka(len(rfm)), "#F59E0B"),
    ])

    bs_cnt = bs["basket_size"].value_counts().sort_index().reset_index()
    bs_cnt.columns = ["basket_size", "Jumlah"]
    bs_cnt["Label"] = bs_cnt["Jumlah"].map(fmt_angka)
    fig = px.bar(bs_cnt, x="basket_size", y="Jumlah", text="Label",
                 title="Distribusi basket_size per Transaksi",
                 color_discrete_sequence=["#818CF8"])
    fig.update_traces(textposition="outside", textfont=dict(size=10),
                      hovertemplate="basket_size %{x}: %{y:,.0f} transaksi<extra></extra>")
    fig.update_xaxes(dtick=1)
    tv, tt = ticks_ribuan(bs_cnt["Jumlah"], maks=4)
    fig.update_yaxes(tickvals=tv, ticktext=tt,
                     range=[0, float(bs_cnt["Jumlah"].max()) * 1.18])
    gaya(fig, tinggi=370, mt=64)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Recency · Frequency · Monetary (per Pelanggan)")
    st.caption(f"**Tanggal acuan** = {tgl_acuan:%d %b %Y} (satu hari setelah transaksi "
               f"maksimum, sesuai rekomendasi Info_Dataset).")
    rfm_show = rfm.head(15).copy()
    rfm_tabel = pd.DataFrame({
        "Customer_ID": rfm_show["Customer_ID"],
        "Recency (hari)": rfm_show["Recency"].map(fmt_angka),
        "Frequency": rfm_show["Frequency"].map(fmt_angka),
        "Monetary": rfm_show["Monetary"].map(fmt_rupiah),
    })
    st.markdown(tabel_html(rfm_tabel, num_cols=["Recency (hari)", "Frequency",
                                                "Monetary"]),
                unsafe_allow_html=True)

    st.markdown("#### Matriks Transaksi × Produk (untuk Apriori)")
    st.caption(f"Bentuk one-hot: {fmt_angka(matriks.shape[0])} transaksi x "
               f"{fmt_angka(matriks.shape[1])} produk. "
               f"Nilai 1 = produk dibeli dalam transaksi tersebut.")
    st.dataframe(matriks.iloc[:8, :10], use_container_width=True, hide_index=True)

    st.markdown("### 2d. Strategi untuk Data Besar")
    st.markdown(
        f"""
- **Sampling stratified** - untuk eksplorasi cepat, ambil sampel berimbang per bulan/kategori
  agar pola musiman tidak terdistorsi.
- **Chunking** - baca & proses file dalam potongan (misal 50000 baris) untuk memori terbatas,
  lalu agregasikan hasil tiap chunk.
- **Agregasi awal** - untuk Apriori/K-Means, data langsung diagregat ke level transaksi-item
  dan pelanggan-RFM sehingga volume turun drastis ({fmt_angka(18513)} baris menjadi {fmt_angka(5998)} basket
  dan {fmt_angka(1480)} pelanggan).
        """
    )


# ---------------------------------------------------------------------------
# Halaman 03 - Apriori
# ---------------------------------------------------------------------------

def halaman_apriori():
    hero("03 - Apriori / Market Basket Analysis",
         "Menemukan kombinasi produk yang sering dibeli bersama beserta metrik aturan asosiasi.",
         "#F59E0B")

    st.markdown("### 3a. Parameter Minimum Support, Confidence, Lift & Ukuran Itemset (k)")
    st.caption(
        "Support maksimum pasangan produk pada data ini hanya sekitar 4% (banyak produk, "
        "transaksi menyebar), sehingga ambang 5% akan menghasilkan nol aturan. Support 2% "
        "dipilih agar pola signifikan tertangkap tanpa aturan sampah; confidence 20% dan "
        "lift > 1 menjaga relevansi serta menghindari aturan kebetulan. Ukuran itemset "
        "maksimum (k) menentukan panjang kombinasi maksimal yang dicari: k = 3 berarti "
        "maksimal bundling 3 produk, k = 5 memungkinkan aturan hingga 5 produk sekaligus. "
        "Namun k hanya berpengaruh bila itemset sepanjang itu benar-benar lolos Minimum "
        "Support - pada data ini itemset 3 produk mulai muncul pada support 0,5% (0,005) "
        "dan itemset 4 produk pada support 0,1% (0,001), sehingga untuk k > 2 slider "
        "support harus diturunkan lebih dulu (lihat catatan di bawah kartu hasil).")
    csup, cconf, clift, ck = st.columns(4)
    min_sup = csup.slider("Minimum Support", 0.0005, 0.05, 0.02, 0.0005, format="%.4f")
    min_conf = cconf.slider("Minimum Confidence", 0.1, 0.6, 0.2, 0.05, format="%.2f")
    min_lift = clift.slider("Minimum Lift", 1.0, 3.0, 1.05, 0.05, format="%.2f")
    max_len = ck.slider(
        "Ukuran Itemset Maks (k)", 2, 10, 3, 1,
        help="Panjang kombinasi produk maksimal yang dicari Apriori. Aturan asosiasi "
             "dihasilkan dari itemset berukuran 2 sampai k.")
    st.session_state["max_len"] = max_len

    res = ae.jalankan_apriori(matriks, min_sup, min_conf, min_lift, max_len=max_len)
    freq = res["frequent_itemsets"]
    rules = res["rules"].copy()

    kartu_kpi([
        ("Frequent Itemsets", str(len(freq)), "#38BDF8"),
        ("Aturan Asosiasi", str(len(rules)), "#F59E0B"),
        ("Basis Transaksi", fmt_angka(res["n_transaksi"]), "#C9A24B"),
    ])

    maxlen_ada = int(freq["length"].max()) if not freq.empty else 0
    if freq.empty:
        st.warning(f"Tidak ada itemset yang lolos Minimum Support {min_sup:.4f}. "
                   "Turunkan slider Minimum Support.")
    elif max_len > maxlen_ada:
        st.info(
            f"**Catatan parameter k:** Anda memilih k = {max_len}, tetapi itemset "
            f"terpanjang yang lolos Minimum Support {min_sup:.4f} hanya "
            f"**{maxlen_ada} produk**. Kombinasi {maxlen_ada + 1}-{max_len} produk "
            f"tidak ditemukan, sehingga **k = {max_len} belum mengubah apa pun** - "
            f"hasil identik dengan k = {maxlen_ada}. Penyebab: itemset besar harus "
            f"lolos support lebih dulu, sedangkan itemset {maxlen_ada + 1} produk "
            f"terlalu jarang pada ambang ini. Instruksi: turunkan slider Minimum "
            f"Support (pada data ini itemset 4 produk mulai muncul pada support "
            f"0,1% = 0,001), lalu lihat apakah k = {max_len} menambah itemset "
            f"atau aturan.")

    if rules.empty:
        st.warning("Tidak ada aturan yang memenuhi ambang. Turunkan minimum support/confidence.")
        return

    rules["Aturan"] = rules.apply(
        lambda r: f"{label_item(r['antecedents'])} → {label_item(r['consequents'])}", axis=1)

    st.markdown("### 3b. Frequent Itemsets Teratas")
    fi = freq.head(12).copy()
    fi_tabel = pd.DataFrame({
        "Itemset": fi["items"].apply(label_item),
        "Ukuran": fi["length"].map(str),
        "Support": fi["support"].map(lambda v: fmt_pct(v * 100)),
    })
    st.markdown(tabel_html(fi_tabel, num_cols=["Ukuran", "Support"],
                           wrap_cols=["Itemset"]), unsafe_allow_html=True)

    st.markdown("### 3c. Aturan Asosiasi Terbaik (maks. 10)")
    st.caption("Peringkat berbasis skor gabungan = 0,5 x lift + 0,3 x confidence + "
               "0,2 x support; lift > 1 berarti pembelian produk Y meningkat ketika X ikut dibeli.")
    top10 = rules.head(10).copy()
    top10_tabel = pd.DataFrame({
        "Aturan (X → Y)": top10["Aturan"],
        "Support": top10["support"].map(lambda v: fmt_pct(v * 100)),
        "Confidence": top10["confidence"].map(lambda v: fmt_pct(v * 100, 1)),
        "Lift": top10["lift"].map(lambda v: fmt_des(v)),
        "Leverage": top10["leverage"].map(lambda v: fmt_des(v, 4)),
    })
    st.markdown(tabel_html(top10_tabel, num_cols=["Support", "Confidence", "Lift",
                                                  "Leverage"],
                           wrap_cols=["Aturan (X → Y)"]), unsafe_allow_html=True)

    st.markdown("### 3d. Visualisasi Aturan")
    st.caption(
        "Cara baca: sumbu X = Support (seberapa sering kombinasi muncul), sumbu Y = "
        "Confidence (seberapa yakin aturan berlaku), ukuran & warna titik = Lift "
        "(makin besar/makin gelap = kaitan makin kuat). Nomor pada titik sesuai "
        "daftar pada kotak sorot di bawah; arahkan kursor untuk detail lengkap.")

    d = top10.copy().reset_index(drop=True)
    d["sx"] = d["support"] * 100
    d["cy"] = d["confidence"] * 100
    d["no"] = [str(i + 1) for i in range(len(d))]
    d["info"] = d.apply(
        lambda r: (f"<b>{r['Aturan']}</b><br>"
                   f"Support {fmt_pct(r['support'] * 100)}<br>"
                   f"Confidence {fmt_pct(r['confidence'] * 100, 1)}<br>"
                   f"Lift {fmt_des(r['lift'])}"), axis=1)

    fig = px.scatter(d, x="sx", y="cy", size="lift", color="lift",
                     text="no", custom_data=["info"],
                     color_continuous_scale=["#10B981", "#C9A24B"],
                     size_max=30,
                     title="Peta Aturan: Support x Confidence (ukuran & warna = Lift)")
    fig.update_traces(
        textposition="middle center",
        textfont=dict(size=11, color="#ffffff", family=FONT_SANS),
        hovertemplate="%{customdata[0]}<extra></extra>",
        marker=dict(line=dict(width=1.5, color="#ffffff")))
    fig.update_xaxes(title_text="Support (%)", tickformat=",.2f", ticksuffix="%")
    fig.update_yaxes(title_text="Confidence (%)", tickformat=",.0f", ticksuffix="%")
    fig.update_layout(coloraxis_colorbar=dict(title="Lift"))
    gaya(fig, tinggi=470, mr=40)

    opsi = ["- Semua aturan -"] + [
        f"{i}. {pendek(r['Aturan'], 46)}" for i, r in d.iterrows()]
    pilih = st.selectbox("Sorot aturan pada peta", opsi)
    if pilih != opsi[0]:
        i = int(pilih.split(".", 1)[0]) - 1
        row = d.iloc[i]
        fig.add_trace(go.Scatter(
            x=[row["sx"]], y=[row["cy"]], mode="markers+text",
            marker=dict(size=30, symbol="circle-open",
                        line=dict(width=3, color="#F59E0B")),
            text=[row["no"]], textposition="middle center",
            textfont=dict(size=11, color="#F59E0B"),
            name="Sorotan", hoverinfo="skip", showlegend=False))
        dy = -78 if row["cy"] >= float(np.median(d["cy"])) else 78
        dx = 70 if row["sx"] <= float(np.median(d["sx"])) else -70
        teks_sorot = pilih.split(".", 1)[1].strip()
        fig.add_annotation(
            x=row["sx"], y=row["cy"], text=teks_sorot,
            showarrow=True, arrowhead=2, arrowsize=1.1, arrowwidth=1.6,
            arrowcolor="#F59E0B", ax=dx, ay=dy,
            font=dict(size=11, color="#F8FAFC", family=FONT_SANS),
            bgcolor="rgba(11,18,32,.93)", bordercolor="#F59E0B",
            borderwidth=1, borderpad=5, align="left")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 3e. Heatmap Lift Antar Produk")
    idx_lbl = list(dict.fromkeys(
        pendek(label_item(r["antecedents"]), 24) for _, r in top10.iterrows()))
    col_lbl = list(dict.fromkeys(
        pendek(label_item(r["consequents"]), 24) for _, r in top10.iterrows()))
    z = np.full((len(idx_lbl), len(col_lbl)), np.nan)
    teks = np.full((len(idx_lbl), len(col_lbl)), "", dtype=object)
    for _, r in top10.iterrows():
        i = idx_lbl.index(pendek(label_item(r["antecedents"]), 24))
        j = col_lbl.index(pendek(label_item(r["consequents"]), 24))
        z[i, j] = r["lift"]
        teks[i, j] = fmt_des(r["lift"])
    hm = go.Figure(go.Heatmap(
        z=z, x=col_lbl, y=idx_lbl, text=teks, texttemplate="{text}",
        colorscale=[[0, "#0B1220"], [0.5, "#3F3519"], [1, "#C9A24B"]],
        colorbar=dict(title="Lift"), hovertemplate=
        "%{y} → %{x}<br>Lift %{z:.2f}<extra></extra>"))
    hm.update_layout(title="Lift Antar Produk (Aturan Teratas)")
    gaya(hm, tinggi=max(420, 46 * len(idx_lbl)))
    hm.update_yaxes(autorange="reversed")
    st.plotly_chart(hm, use_container_width=True)

    st.session_state["rules"] = rules
    st.session_state["freq"] = freq


# ---------------------------------------------------------------------------
# Halaman 04 - K-Means
# ---------------------------------------------------------------------------

def halaman_kmeans():
    hero("04 - Segmentasi Pelanggan (K-Means)",
         "Segmentasi berbasis fitur RFM dengan evaluasi Elbow & Silhouette.",
         "#8B5CF6")

    st.markdown("### 4a. Fitur yang Digunakan")
    st.markdown(
        """
- **Recency** - hari sejak transaksi terakhir (makin kecil = makin aktif baru-baru ini).
- **Frequency** - jumlah transaksi unik (loyalitas).
- **Monetary** - total belanja bersih (nilai pelanggan).

Fitur distandardisasi (StandardScaler: mean 0, std 1) karena K-Means berbasis jarak Euclidean;
tanpa scaling, Monetary (ratusan ribu) akan mendominasi Recency (ratusan hari).
        """
    )

    st.markdown("### 4b. Elbow Method & Silhouette Score")
    Xs, ev, labels, prof = jalankan_kmeans_cached("rfm", 3)
    e1, e2 = st.columns(2)
    ev_i = ev.copy()
    ev_i["inertia_lbl"] = ev_i["inertia"].map(fmt_angka)
    ev_i["sil_lbl"] = ev_i["silhouette"].map(lambda v: fmt_des(v, 3))
    with e1:
        fig = px.line(ev_i, x="k", y="inertia", text="inertia_lbl", markers=True,
                      title="Elbow Method (Inertia)", color_discrete_sequence=["#10B981"])
        fig.update_traces(mode="lines+markers+text", line=dict(width=3),
                          textposition="top center", textfont=dict(size=10),
                          hovertemplate="k=%{x}<br>Inertia %{y:,.0f}<extra></extra>")
        tv, tt = ticks_ribuan(ev_i["inertia"], maks=4)
        fig.update_xaxes(dtick=1, title_text="Jumlah klaster (k)")
        fig.update_yaxes(tickvals=tv, ticktext=tt)
        gaya(fig, tinggi=390, mt=74)
        st.plotly_chart(fig, use_container_width=True)
    with e2:
        fig = px.line(ev_i, x="k", y="silhouette", text="sil_lbl", markers=True,
                      title="Silhouette Score", color_discrete_sequence=["#C9A24B"])
        fig.update_traces(mode="lines+markers+text", line=dict(width=3),
                          textposition="top center", textfont=dict(size=10),
                          hovertemplate="k=%{x}<br>Skor %{y:.3f}<extra></extra>")
        fig.update_xaxes(dtick=1, title_text="Jumlah klaster (k)")
        fig.update_yaxes(tickformat=",.3f")
        gaya(fig, tinggi=390, mt=74)
        st.plotly_chart(fig, use_container_width=True)

    ev_tabel = pd.DataFrame({
        "k": ev["k"].map(str),
        "Inertia": ev["inertia"].map(fmt_angka),
        "Silhouette": ev["silhouette"].map(lambda v: fmt_des(v, 3)),
        "Iterasi": ev["n_iter"].map(str),
    })
    st.markdown(tabel_html(ev_tabel, num_cols=["k", "Inertia", "Silhouette", "Iterasi"]),
                unsafe_allow_html=True)

    best_k = int(ev.sort_values("silhouette", ascending=False).iloc[0]["k"])
    skor_best = float(ev.sort_values("silhouette", ascending=False).iloc[0]["silhouette"])
    st.info(f"**k terbaik menurut Silhouette = {best_k}** (skor {fmt_des(skor_best, 3)}). "
            f"Elbow menunjukkan tekukan inertia sekitar k={best_k}-4; dipilih k={best_k} "
            f"karena seimbang antara kepadatan klaster dan kemudahan interpretasi bisnis.")

    st.markdown("### 4c. Jumlah Klaster Final")
    k_final = st.select_slider("Jumlah klaster (k)", options=list(range(2, 9)),
                               value=best_k)
    Xs, ev2, labels, prof = jalankan_kmeans_cached("rfm", int(k_final))

    st.markdown("### 4d. Profil Klaster")
    prof_tabel = pd.DataFrame({
        "Klaster": prof["Cluster"].map(str),
        "Label Segmen": prof["label_segmen"],
        "Jumlah Pelanggan": prof["jumlah_pelanggan"].map(fmt_angka),
        "Recency Rata-rata (hari)": prof["recency_mean"].map(lambda v: fmt_des(v, 1)),
        "Frequency Rata-rata": prof["frequency_mean"].map(lambda v: fmt_des(v, 1)),
        "Monetary Rata-rata": prof["monetary_mean"].map(fmt_rupiah),
        "Total Moneter": prof["monetary_total"].map(fmt_rupiah),
    })
    st.markdown(tabel_html(prof_tabel,
                           num_cols=["Klaster", "Jumlah Pelanggan",
                                     "Recency Rata-rata (hari)", "Frequency Rata-rata",
                                     "Monetary Rata-rata", "Total Moneter"],
                           wrap_cols=["Label Segmen"]), unsafe_allow_html=True)

    st.markdown("### 4e. Visualisasi Segmen")
    rfm_l = rfm.copy()
    rfm_l["Cluster"] = labels
    rfm_l["Label"] = prof.set_index("Cluster")["label_segmen"].reindex(labels).values

    v1, v2 = st.columns(2)
    tv_r, tt_r = ticks_ribuan(rfm_l["Monetary"], maks=4)
    with v1:
        fig = px.scatter(rfm_l, x="Recency", y="Monetary", color="Label",
                         size="Frequency", hover_data=["Customer_ID", "Frequency"],
                         title="Segmen: Recency x Monetary (ukuran = Frequency)",
                         color_discrete_sequence=PALETTE)
        fig.update_yaxes(tickvals=tv_r, ticktext=tt_r)
        fig.update_traces(hovertemplate=
                          "%{customdata[0]}<br>Recency %{x:,.0f} hari<br>"
                          "Rp %{y:,.0f}<extra></extra>")
        gaya(fig, tinggi=460, mr=80)
        st.plotly_chart(fig, use_container_width=True)
    with v2:
        fig = px.box(rfm_l, x="Label", y="Monetary", color="Label",
                     title="Distribusi Monetary per Segmen",
                     color_discrete_sequence=PALETTE)
        fig.update_yaxes(tickvals=tv_r, ticktext=tt_r)
        fig.update_traces(hovertemplate="Rp %{y:,.0f}<extra></extra>")
        gaya(fig, tinggi=460)
        st.plotly_chart(fig, use_container_width=True)

    st.session_state["labels"] = labels
    st.session_state["prof"] = prof
    st.session_state["rfm_l"] = rfm_l


# ---------------------------------------------------------------------------
# Halaman 05 - Dashboard BI
# ---------------------------------------------------------------------------

def halaman_dashboard():
    hero("05 - Dashboard Business Intelligence",
         "Tampilan eksekutif dengan KPI, tren, hasil Apriori & K-Means, serta filter interaktif.",
         "#38BDF8")

    st.markdown('<div class="fb-title-inline">Filter Analisis</div>',
                unsafe_allow_html=True)
    fa, fb, fc = st.columns(3)
    t_min = clean["Transaction_Date"].min().date()
    t_max = clean["Transaction_Date"].max().date()
    rentang = fa.slider("Periode transaksi", t_min, t_max, (t_min, t_max),
                        format="YYYY-MM-DD")
    kategori_list = sorted(clean["Category"].dropna().unique())
    kategori = fb.multiselect("Kategori produk", kategori_list, default=kategori_list)

    labels = st.session_state.get("labels", None)
    if labels is None:
        _, _, labels, _ = jalankan_kmeans_cached("rfm", 3)
    prof = st.session_state.get("prof", None)
    if prof is None:
        _, _, _, prof = jalankan_kmeans_cached("rfm", 3)
    seg_map = prof.set_index("Cluster")["label_segmen"].to_dict()
    cust_seg = {cid: seg_map.get(lab, str(lab))
                for cid, lab in zip(rfm["Customer_ID"], labels)}
    seg_options = ["Semua"] + sorted(set(cust_seg.values()))
    seg_pilih = fc.multiselect("Segmen pelanggan", seg_options, default=["Semua"])

    mask = ((clean["Transaction_Date"].dt.date >= rentang[0]) &
            (clean["Transaction_Date"].dt.date <= rentang[1]) &
            (clean["Category"].isin(kategori)))
    dff = clean[mask]
    if seg_pilih and "Semua" not in seg_pilih:
        cust_ok = {c for c, s in cust_seg.items() if s in seg_pilih}
        dff = dff[dff["Customer_ID"].isin(cust_ok)]

    st.markdown("### KPI Utama")
    bs_mean = dff.groupby("Transaction_ID")["Product_ID"].nunique().mean()
    kartu_kpi([
        ("Total Penjualan", fmt_rupiah(dff["Line_Total"].sum()), "#38BDF8"),
        ("Jumlah Transaksi", fmt_angka(dff["Transaction_ID"].nunique()), "#C9A24B"),
        ("Pelanggan Unik", fmt_angka(dff.loc[dff.Customer_ID != "UNKNOWN",
                                             "Customer_ID"].nunique()), "#818CF8"),
        ("Rata-rata basket_size", (fmt_des(bs_mean) if not np.isnan(bs_mean)
                                   else "0") + " produk", "#F59E0B"),
    ])

    st.markdown("### Analisis Penjualan")
    a1, a2 = st.columns(2)
    bul = (dff.set_index("Transaction_Date").resample("ME")["Line_Total"].sum().reset_index())
    bul["Bulan"] = bul["Transaction_Date"].dt.strftime("%b")
    with a1:
        fig = px.line(bul, x="Bulan", y="Line_Total", markers=True,
                      title="Tren Penjualan Bulanan (2025)",
                      color_discrete_sequence=["#10B981"])
        fig.update_traces(line=dict(width=3),
                          hovertemplate="%{x}: Rp %{y:,.0f}<extra></extra>")
        tv, tt = ticks_ribuan(bul["Line_Total"], maks=4)
        fig.update_yaxes(tickvals=tv, ticktext=tt, title_text="Penjualan (Rp)")
        gaya(fig, tinggi=400, mb=70)
        st.plotly_chart(fig, use_container_width=True)
    with a2:
        tp = (dff.groupby("Product_Name")["Line_Total"].sum()
              .sort_values(ascending=False).head(8).reset_index())
        tp["LabelNilai"] = tp["Line_Total"].map(fmt_angka)
        fig = px.bar(tp, x="Line_Total", y="Product_Name", orientation="h",
                     text="LabelNilai", title="8 Produk Penjualan Tertinggi",
                     color_discrete_sequence=["#C9A24B"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(tp["Line_Total"], maks=3)
        fig.update_xaxes(tickvals=tv, ticktext=tt,
                         range=[0, float(tp["Line_Total"].max()) * 1.22])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}<br>Rp %{x:,.0f}<extra></extra>")
        gaya(fig, tinggi=400, mr=100, ml=110)
        st.plotly_chart(fig, use_container_width=True)

    a3, a4 = st.columns(2)
    kat = (dff.groupby("Category")["Line_Total"].sum()
           .sort_values(ascending=False).reset_index())
    total_kat = kat["Line_Total"].sum()
    with a3:
        kat["Pct"] = [fmt_des(v / total_kat * 100, 1) + "%"
                      for v in kat["Line_Total"]]
        kat["Info"] = [f"{kat['Category'][i]}<br>Penjualan Rp {_rib(int(kat['Line_Total'][i]))} "
                       f"({kat['Pct'][i]})" for i in kat.index]
        fig = px.bar(kat.sort_values("Line_Total", ascending=True),
                     x="Line_Total", y="Category", orientation="h", text="Pct",
                     custom_data=["Info"],
                     title="Distribusi Penjualan per Kategori",
                     color_discrete_sequence=["#10B981"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(kat["Line_Total"], maks=3)
        fig.update_xaxes(tickvals=tv, ticktext=tt,
                         range=[0, float(kat["Line_Total"].max()) * 1.30])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{customdata[0]}<extra></extra>")
        gaya(fig, tinggi=430, mr=70, ml=120)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"Total penjualan terfilter: <b>{fmt_rupiah(total_kat)}</b> "
                   f"dari {fmt_angka(kat.shape[0])} kategori; persen = pangsa "
                   f"terhadap total.", unsafe_allow_html=True)
    with a4:
        pm = (dff.groupby("Payment_Method")["Line_Total"].sum()
              .sort_values(ascending=False).reset_index())
        pm["LabelNilai"] = pm["Line_Total"].map(fmt_angka)
        fig = px.bar(pm, x="Line_Total", y="Payment_Method", orientation="h",
                     text="LabelNilai", title="Penjualan per Metode Bayar",
                     color_discrete_sequence=["#6366F1"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(pm["Line_Total"], maks=3)
        fig.update_xaxes(tickvals=tv, ticktext=tt,
                         range=[0, float(pm["Line_Total"].max()) * 1.32])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}<br>Rp %{x:,.0f}<extra></extra>")
        gaya(fig, tinggi=430, mr=115, ml=125)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Hasil Apriori")
    rules = st.session_state.get("rules", None)
    if rules is None or rules.empty:
        rules = ae.jalankan_apriori(matriks, 0.02, 0.2, 1.05,
                                    max_len=st.session_state.get("max_len", 3))["rules"].copy()
    t10 = rules.head(10).copy()
    t10["Aturan"] = t10.apply(lambda r: f"{label_item(r['antecedents'])} → "
                                        f"{label_item(r['consequents'])}", axis=1)
    t10_tabel = pd.DataFrame({
        "Aturan (X → Y)": t10["Aturan"],
        "Support": t10["support"].map(lambda v: fmt_pct(v * 100)),
        "Confidence": t10["confidence"].map(lambda v: fmt_pct(v * 100, 1)),
        "Lift": t10["lift"].map(lambda v: fmt_des(v)),
    })
    st.markdown(tabel_html(t10_tabel, num_cols=["Support", "Confidence", "Lift"],
                           wrap_cols=["Aturan (X → Y)"]), unsafe_allow_html=True)

    st.markdown("### Hasil K-Means")
    m1, m2 = st.columns(2)
    with m1:
        p1 = prof.copy().sort_values("jumlah_pelanggan", ascending=True)
        p1["LabelNilai"] = p1["jumlah_pelanggan"].map(fmt_angka)
        fig = px.bar(p1, x="jumlah_pelanggan", y="label_segmen", orientation="h",
                     text="LabelNilai", title="Jumlah Pelanggan per Segmen",
                     color_discrete_sequence=["#38BDF8"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(p1["jumlah_pelanggan"], maks=4)
        fig.update_xaxes(tickvals=tv, ticktext=tt,
                         range=[0, float(p1["jumlah_pelanggan"].max()) * 1.28])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}: %{x:,.0f} pelanggan<extra></extra>")
        gaya(fig, tinggi=390, mr=85, ml=135)
        st.plotly_chart(fig, use_container_width=True)
    with m2:
        p2 = prof.copy().sort_values("monetary_mean", ascending=True)
        p2["LabelNilai"] = p2["monetary_mean"].map(fmt_angka)
        fig = px.bar(p2, x="monetary_mean", y="label_segmen", orientation="h",
                     text="LabelNilai", title="Rata-rata Monetary per Segmen (Rp)",
                     color_discrete_sequence=["#C9A24B"])
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        tv, tt = ticks_ribuan(p2["monetary_mean"], maks=3)
        fig.update_xaxes(tickvals=tv, ticktext=tt,
                         range=[0, float(p2["monetary_mean"].max()) * 1.34])
        fig.update_traces(textposition="outside", textfont=dict(size=10),
                          hovertemplate="%{y}<br>Rp %{x:,.0f}<extra></extra>")
        gaya(fig, tinggi=390, mr=105, ml=135)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Bonus · Pola Produk per Segmen")
    st.markdown(
        """
Bagian ini **menggabungkan hasil Apriori x K-Means**: menampilkan seberapa kuat satu
produk "dimiliki" oleh satu segmen pelanggan - dasar untuk menyesuaikan promosi per segmen.

**Cara membaca heatmap di bawah:**
- **Baris** = enam produk terlaris keseluruhan; **kolom** = segmen pelanggan
  (Loyal, Potential Loyal, Churn Risk), diurutkan dari segmen terbesar.
- **Warna & angka sel** = pangsa penjualan produk tersebut *di dalam segmen* (%);
  makin gelap makin dominan.
- **Arahkan kursor** ke sel untuk melihat nilai rupiah absolutnya.
- **Filter periode, kategori, dan segmen** di bagian atas dashboard dipakai ulang
  di sini, sehingga peta bisa dijelajah sesuai kebutuhan.
        """
    )
    if labels is not None and not dff.empty:
        cust_seg2 = dict(zip(rfm["Customer_ID"], labels))
        dseg = dff[dff["Customer_ID"].isin(cust_seg2)].copy()
        dseg["Segmen"] = dseg["Customer_ID"].map(cust_seg2)
        seg_map2 = prof.set_index("Cluster")["label_segmen"].to_dict()
        dseg["NamaSegmen"] = dseg["Segmen"].map(seg_map2)
        produk_seg = (dseg.groupby(["NamaSegmen", "Product_Name"])["Line_Total"].sum()
                      .reset_index())
        pivot = produk_seg.pivot_table(index="Product_Name", columns="NamaSegmen",
                                        values="Line_Total", aggfunc="sum",
                                        fill_value=0)
        urut_seg = [s for s in (prof.sort_values("jumlah_pelanggan",
                                                  ascending=False)["label_segmen"]
                                .tolist()) if s in pivot.columns]
        pivot = pivot.reindex(columns=urut_seg)
        if pivot.empty or not urut_seg:
            st.info("Tidak ada data produk/segmen untuk filter saat ini - longgarkan "
                    "filter di atas untuk melihat pola ini.")
        else:
            top_produk = (pivot.sum(axis=1).sort_values(ascending=False)
                          .head(6).index.tolist())
            pivot = pivot.reindex(top_produk)
            tot_kolom = pivot.sum(axis=0).replace(0, np.nan)
            share = (pivot.div(tot_kolom, axis=1) * 100).fillna(0)

            teks_pct = [[fmt_des(v, 1) + "%" for v in row] for row in share.values]
            rp_cell = [[_rib(int(v)) for v in row] for row in pivot.values]

            fig = go.Figure(go.Heatmap(
                z=share.values, x=urut_seg, y=top_produk,
                text=teks_pct, texttemplate="{text}", textfont=dict(size=11),
                customdata=rp_cell,
                colorscale=[[0, "#0B1220"], [0.55, "#155E75"], [1, "#38BDF8"]],
                colorbar=dict(title="% segmen"),
                hovertemplate=("%{y}<br>%{x}<br>Penjualan Rp %{customdata[0]}"
                               "<br>Pangsa %{z:,.1f}%<extra></extra>")))
            fig.update_layout(title="Pangsa Produk dalam Belanja Tiap Segmen (%)")
            fig.update_yaxes(autorange="reversed")
            gaya(fig, tinggi=max(430, 46 * len(top_produk) + 205),
                 ml=130, mr=40, mb=74)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### Insight per Segmen")
            AKSI_SEG = {
                "Loyal Customers": ("Pertahankan: reward, early access, dan jaga "
                                    "ketersediaan produk andalan."),
                "Potential Loyal": ("Kembangkan: bundling & upsell ke produk "
                                    "ber-lift tinggi (lihat peta aturan Apriori)."),
                "Churn Risk": ("Menangkan kembali: diskon personal, pengingat, dan "
                               "penawaran khusus."),
                "New Customers": ("Onboarding: cross-sell produk populer sejak "
                                  "transaksi awal."),
            }
            kartu = []
            for i, nama_seg in enumerate(urut_seg):
                sub = produk_seg[produk_seg["NamaSegmen"] == nama_seg].sort_values(
                    "Line_Total", ascending=False)
                if sub.empty:
                    continue
                tot_seg = float(sub["Line_Total"].sum())
                r1 = sub.iloc[0]
                p1 = float(r1["Line_Total"]) / tot_seg * 100 if tot_seg else 0.0
                andalan = (f"Produk andalan: <b>{r1['Product_Name']}</b> "
                           f"({fmt_des(p1, 1)}% dari belanja segmen)")
                if len(sub) > 1:
                    r2 = sub.iloc[1]
                    p2 = float(r2["Line_Total"]) / tot_seg * 100 if tot_seg else 0.0
                    andalan += (f", disusul <b>{r2['Product_Name']}</b> "
                                f"({fmt_des(p2, 1)}%)")
                andalan += "."
                warna = PALETTE[i % len(PALETTE)]
                aksi = AKSI_SEG.get(nama_seg,
                                    "Kembangkan potensi lewat promosi bertarget.")
                kartu.append(
                    f'<div class="kpi" style="--k:{warna}">'
                    f'<div class="v" style="font-size:1.02rem">{nama_seg}</div>'
                    f'<div class="l" style="text-transform:none;letter-spacing:.01em;'
                    f'line-height:1.6;margin-top:.4rem">{andalan} '
                    f"Total belanja segmen <b>{fmt_rupiah(tot_seg)}</b>. "
                    f"{aksi}</div></div>")
            if kartu:
                st.markdown(f'<div class="kpi-grid">{"".join(kartu)}</div>',
                            unsafe_allow_html=True)
    else:
        st.info("Tidak ada data pelanggan untuk filter saat ini - longgarkan filter "
                "di atas untuk melihat pola produk per segmen.")


# ---------------------------------------------------------------------------
# Halaman 06 - Rekomendasi
# ---------------------------------------------------------------------------

def halaman_rekomendasi():
    hero("06 - Rekomendasi Keputusan Bisnis",
         "Strategi preskriptif berbasis bukti data, prioritas, estimasi dampak & evaluasi.",
         "#C9A24B")

    rules = st.session_state.get("rules", None)
    if rules is None or rules.empty:
        rules = ae.jalankan_apriori(matriks, 0.02, 0.2, 1.05,
                                    max_len=st.session_state.get("max_len", 3))["rules"].copy()
    prof = st.session_state.get("prof", None)
    if prof is None:
        _, _, _, prof = jalankan_kmeans_cached("rfm", 3)

    st.markdown("### 6a. Rekomendasi Berdasarkan Apriori (Bundling & Penempatan Rak)")
    rec_rows = []
    for i, (_, r) in enumerate(rules.head(5).iterrows(), 1):
        a = label_item(r["antecedents"])
        c = label_item(r["consequents"])
        rec_rows.append({
            "No": str(i),
            "Kombinasi Produk": f"{a} + {c}",
            "Bukti Data": (f"lift {fmt_des(r['lift'])}, "
                           f"confidence {fmt_pct(r['confidence'] * 100, 1)}, "
                           f"support {fmt_pct(r['support'] * 100)}"),
            "Rekomendasi": f"Tempatkan {a} dan {c} berdekatan / tawarkan bundling hemat.",
        })
    st.markdown(tabel_html(pd.DataFrame(rec_rows), num_cols=["No"],
                           wrap_cols=["Kombinasi Produk", "Bukti Data", "Rekomendasi"]),
                unsafe_allow_html=True)

    st.markdown("### 6b. Rekomendasi Retensi Berdasarkan Segmentasi")
    seg_rows = []
    for _, r in prof.iterrows():
        lab = r["label_segmen"]
        if lab == "Loyal Customers":
            strat = "Program loyalitas, early-access promo, referral reward."
            prior = "Pertahankan (nilai tinggi)"
        elif lab == "Churn Risk":
            strat = "Win-back campaign, diskon personal, penawaran kembali."
            prior = "Tinggi - cegah churn"
        elif lab == "New Customers":
            strat = "Onboarding offer, cross-sell produk populer, edukasi katalog."
            prior = "Bangun kebiasaan belanja"
        else:
            strat = "Upsell bundling & pengingat promo berkala."
            prior = "Kembangkan potensi"
        seg_rows.append({
            "Segmen": lab,
            "Jumlah Pelanggan": fmt_angka(r["jumlah_pelanggan"]),
            "Karakteristik": (f"Recency {fmt_des(r['recency_mean'], 0)} hari, "
                              f"Frequency {fmt_des(r['frequency_mean'], 1)}, "
                              f"Monetary {fmt_rupiah(r['monetary_mean'])}"),
            "Strategi": strat,
            "Prioritas": prior,
        })
    st.markdown(tabel_html(pd.DataFrame(seg_rows),
                           num_cols=["Jumlah Pelanggan"],
                           wrap_cols=["Karakteristik", "Strategi", "Prioritas"]),
                unsafe_allow_html=True)

    st.markdown("### 6c. Prioritas Tindakan (Urgensi × Manfaat × Biaya × Kemudahan)")
    prioritas = pd.DataFrame([
        {"Prioritas": "1", "Tindakan": "Bundling & penempatan rak (produk lift tertinggi)",
         "Urgensi": "Tinggi", "Potensi Manfaat": "Sedang-Tinggi", "Biaya": "Rendah",
         "Kemudahan": "Mudah",
         "Alasan": "Memanfaatkan pola belanja nyata; hanya butuh penataan rak & label promo."},
        {"Prioritas": "2", "Tindakan": "Win-back campaign untuk segmen Churn Risk",
         "Urgensi": "Tinggi", "Potensi Manfaat": "Tinggi", "Biaya": "Sedang",
         "Kemudahan": "Sedang",
         "Alasan": "Segmen recency besar & frekuensi rendah berisiko hilang namun masih bisa diaktifkan."},
        {"Prioritas": "3", "Tindakan": "Program loyalitas untuk Loyal Customers",
         "Urgensi": "Sedang", "Potensi Manfaat": "Tinggi", "Biaya": "Sedang",
         "Kemudahan": "Sedang",
         "Alasan": "Melindungi segmen dengan kontribusi moneter terbesar."},
        {"Prioritas": "4", "Tindakan": "Cross-sell onboarding untuk New Customers",
         "Urgensi": "Sedang", "Potensi Manfaat": "Sedang", "Biaya": "Rendah",
         "Kemudahan": "Mudah",
         "Alasan": "Membangun kebiasaan belanja sejak awal hubungan."},
    ])
    st.markdown(tabel_html(prioritas, num_cols=["Prioritas"],
                           wrap_cols=["Tindakan", "Alasan", "Potensi Manfaat"]),
                unsafe_allow_html=True)

    st.markdown("### 6d. Estimasi Dampak, Asumsi & Cara Ukur")
    st.markdown(
        """
**Batas kejujuran analitis:** bagian berikut adalah **estimasi berbasis asumsi**, bukan fakta
terukur. Dampak aktual hanya diketahui setelah implementasi dan pengukuran lanjutan.

- **Asumsi:** kenaikan cross-sell 5-10% pada produk ber-lift tinggi bila bundling & rak
  diterapkan; recovery 15-20% pelanggan Churn Risk dari win-back campaign.
- **Indikator keberhasilan:** (1) rata-rata basket_size naik; (2) penjualan produk ber-lift
  tinggi meningkat; (3) jumlah pelanggan aktif pada segmen Churn Risk pulih; (4) pendapatan
  per pelanggan Loyal naik.
- **Cara mengukur:** bandingkan KPI pra vs pasca implementasi pada periode sama (misal 3 bulan),
  dengan kelompok kontrol toko bila memungkinkan; pantau bulanan melalui dashboard.
        """
    )

    st.markdown("### 6e. Rencana Implementasi")
    st.markdown(
        """
**Jangka pendek (0-1 bulan):**
- Penataan rak & display bundling untuk kombinasi lift tertinggi.
- Susun & jalankan promo win-back untuk pelanggan Churn Risk.

**Jangka menengah (1-3 bulan):**
- Luncurkan program loyalitas berjenjang berbasis Monetary.
- Otomatiskan rekomendasi produk per segmen di kasir/kanal pemasaran.
- Evaluasi bulanan KPI dashboard dan iterasi strategi.
        """
    )

    st.markdown("### 6f. KPI Evaluasi Keberhasilan")
    kpi_tabel = pd.DataFrame([
        {"KPI": "Rata-rata basket_size", "Baseline (data)": "3,05 produk",
         "Target": "Naik 5-10%", "Cara Ukur": "Rerata item unik/transaksi bulanan"},
        {"KPI": "Penjualan produk ber-lift tinggi", "Baseline (data)": "Lihat dashboard",
         "Target": "Naik 8-15%", "Cara Ukur": "Total penjualan produk tersebut/bulan"},
        {"KPI": "Pelanggan Churn Risk aktif kembali", "Baseline (data)": "Lihat dashboard",
         "Target": "Pulih 15-20%", "Cara Ukur": "Jumlah transaksi ulang segmen tersebut"},
        {"KPI": "Pendapatan per pelanggan Loyal", "Baseline (data)": "Lihat dashboard",
         "Target": "Naik 5-10%", "Cara Ukur": "Monetary rata-rata segmen loyal"},
    ])
    st.markdown(tabel_html(kpi_tabel, wrap_cols=["Cara Ukur", "Baseline (data)"]),
                unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

ROUTER = {
    "00 · Ringkasan": halaman_ringkasan,
    "01 · EDA & Pemahaman": halaman_eda,
    "02 · Preprocessing": halaman_preprocessing,
    "03 · Apriori": halaman_apriori,
    "04 · K-Means": halaman_kmeans,
    "05 · Dashboard": halaman_dashboard,
    "06 · Rekomendasi": halaman_rekomendasi,
}
ROUTER[halaman]()
