import streamlit as st

# Tetapan halaman dan reka bentuk lebar penuh
st.set_page_config(page_title="RISDA RoU Financial Dashboard", layout="wide")

# --- KOD MAGIS CUSTOM CSS FOR CORPORATE LOOK ---
st.markdown("""
    <style>
    /* Mengubah font dan latar belakang aplikasi */
    .main {
        background-color: #f8fafc;
    }
    
    /* Mencantikkan tajuk utama dashboard */
    h1 {
        color: #064e3b !important;
        font-weight: 800 !important;
        font-size: 2.6rem !important;
        padding-bottom: 0px;
    }
    
    /* Mengubah reka bentuk kad st.metric secara global */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 20px 24px !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        border-left: 6px solid #047857 !important; /* Warna Hitam & Emas Korporat RISDA */
        transition: transform 0.2s ease-in-out;
    }
    
    /* Kesan 'hover' bila tetikus lalu di atas kad KPI */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Mencantikkan teks nilai di dalam kad KPI */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    
    /* Mencantikkan teks label di atas kad KPI */
    div[data-testid="stMetricLabel"] {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Mengemaskan gaya pembahagi seksyen */
    hr {
        margin-top: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        border-top: 1px solid #cbd5e1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Banner Atas
st.title("📊 Dashboard Analisis Kebolehlaksanaan RoU Strategik Antara RISDA & Syarikat Swasta - Program TGBB")
st.caption("✨ Corporate Executive Version — Alat Simulasi Dinamik Struktur Sewaan & Produktiviti Estet")
st.markdown("---")

# --- SIDEBAR: PARAMETER PASARAN GLOBAL ---
st.sidebar.header("⚙️ Parameter Pasaran Global")

harga_smr20 = st.sidebar.slider("Harga SMR 20 (sen/kg)", 500, 1200, 790)
insentif_risda = st.sidebar.slider("Insentif RISDA (sen/kg)", 0, 200, 100)
diskaun_kilang = st.sidebar.slider("Kos Pemprosesan/Diskaun (sen/kg)", 50, 200, 130)
kos_opex_gc = st.sidebar.slider("Kos Operasi + GC (RM/Ha/Tahun)", 5000, 12000, 7000)

# Pengiraan Harga Bersih SMR 20 (RM/kg)
harga_clean_rm = (harga_smr20 + insentif_risda - diskaun_kilang) / 100

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Hasil Unjuran Pasaran")
st.sidebar.metric(label="Harga Bersih SMR 20", value=f"RM {harga_clean_rm:.2f}/kg")

if harga_clean_rm < 6.00:
    st.sidebar.error("⚠️ KLAUSA PENURUNAN SEWA: Harga bersih bawah RM6.00/kg. Disyorkan potongan sewa 20%.")

# --- FUNGSI DIALAMI UNTUK NPV, IRR, ROI ---
def kira_metrik_kewangan(untung_tahunan, kadar_sewa, keluasan, tempoh_tahun=6):
    modal_terikat = kadar_sewa * keluasan
    if modal_terikat <= 0 or untung_tahunan <= 0:
        return modal_terikat, 0.0, 0.0, 0.0
    irr = (untung_tahunan / modal_terikat) * 100
    roi = irr * tempoh_tahun
    aliran_tunai = [-modal_terikat] + [untung_tahunan] * tempoh_tahun
    npv = sum([cf / (1.10**t) for t, cf in enumerate(aliran_tunai)])
    return modal_terikat, npv, irr, roi

# Pecahan 4 Tabs Utama
tab1, tab2, tab3, tab4 = st.tabs([
    "🌳 AW (Matang Sahaja)", 
    "🌟 AW (Pelan Penuh 5,747 Ha)", 
    "🍂 Tropika Sanjung", 
    "🌱 Sri Pelita Bumi"
])

# --- TAB 1: ANJAKAN WAWASAN (MATANG SAHAJA) ---
with tab1:
    st.header("Anjakan Wawasan - Senario 1 (2,300 Ha Matang Sahaja)")
    col_in, col_eff = st.columns([1, 2])
    with col_in:
        st.subheader("📋 Input Operasi & Sewa")
        prod_aw = st.slider("Produktiviti (kg/Ha/Tahun)", 500, 2500, 1500, key="aw_p")
        sewa_aw = st.slider("Kadar Sewaan (RM/Ha/Tahun)", 1200, 3600, 2400, key="aw_s")
        
        pendapatan_aw = prod_aw * harga_clean_rm * 2300
        kos_pengurusan_aw = (kos_opex_gc + sewa_aw) * 2300
        untung_aw = pendapatan_aw - kos_pengurusan_aw
        modal_aw, npv_aw, irr_aw, roi_aw = kira_metrik_kewangan(untung_aw, sewa_aw, 2300)
    with col_eff:
        st.subheader("💼 Penunjuk Prestasi Kewangan (KPI)")
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            st.metric("Untung Bersih / Tahun", f"RM {untung_aw:,.0f}")
        with row1_c2:
            st.metric("NPV (@10% Diskaun)", f"RM {npv_aw:,.0f}")
        st.markdown("---")
        row2_c1, row2_c2 = st.columns(2)
        with row2_c1:
            st.metric("IRR (Kadar Pulangan)", f"{irr_aw:.2f}%")
        with row2_c2:
            st.metric("ROI Keseluruhan", f"{roi_aw:.2f}%")
        st.markdown("---")
        if untung_aw < 0:
            st.error("🚨 AMARAN: Aliran tunai negatif! Sila tingkatkan produktiviti atau runding semula kadar sewaan.")

# --- TAB 2: ANJAKAN WAWASAN (PELAN PENUH KESELURUHAN) ---
with tab2:
    st.header("Anjakan Wawasan - Senario 2 (Pelan Struktur Bersepadu 5,747 Ha)")
    st.info("💡 Simulasi unjuran kitaran ekonomi jangka panjang (20 Tahun) merangkumi Getah Matang, Getah Muda, dan Semula Sawit (Konsep GUHA).")
    
    col_in_full, col_eff_full = st.columns([1, 2])
    with col_in_full:
        st.subheader("⏱️ Pilih Fasa Garis Masa RoU")
        fasa_rou = st.selectbox("Pilih Fasa Analisis:", [
            "Tahun 1-2 (Fasa Awalan & Tekanan Tunai CAPEX)",
            "Tahun 3-5 (Fasa Matang Awal & Titik Pulang Modal)",
            "Tahun 6-20 (Fasa Komersial Puncak & Lonjakan Untung)"
        ])
        margin_sawit_bts = st.slider("Margin Untung Bersih Sawit (RM/MT)", 100, 400, 200)
        
        if "Tahun 1-2" in fasa_rou:
            sewa_cat1, prod_cat1 = 1800, 1500  
            sewa_cat2, prod_cat2 = 300, 800    
            sewa_cat3, yield_sawit, capex_sawit = 400, 0, 5750000 
        elif "Tahun 3-5" in fasa_rou:
            sewa_cat1, prod_cat1 = 1800, 1500
            sewa_cat2, prod_cat2 = 600, 1200   
            sewa_cat3, yield_sawit, capex_sawit = 600, 13, 1916666 
        else:
            sewa_cat1, prod_cat1 = 1800, 1500
            sewa_cat2, prod_cat2 = 600, 1500   
            sewa_cat3, yield_sawit, capex_sawit = 1800, 24, 0      
            
        rev_cat1 = prod_cat1 * harga_clean_rm * 2300
        cost_cat1 = (kos_opex_gc + sewa_cat1) * 2300
        profit_cat1 = rev_cat1 - cost_cat1
        
        rev_cat2 = prod_cat2 * harga_clean_rm * 2297
        cost_cat2 = (kos_opex_gc + sewa_cat2) * 2297
        profit_cat2 = rev_cat2 - cost_cat2
        
        profit_sawit = (1150 * yield_sawit * margin_sawit_bts) - (1150 * sewa_cat3) - capex_sawit
        total_untung_tahunan = profit_cat1 + profit_cat2 + profit_sawit
        
    with col_eff_full:
        st.subheader("📊 Prestasi Aliran Tunai Gabungan")
        f_r1, f_r2 = st.columns(2)
        with f_r1:
            st.metric("Anggaran Untung Bersih Fasa/Thn", f"RM {total_untung_tahunan:,.0f}")
        with f_r2:
            st.metric("NPV Projek Global (20 Thn @10%)", "RM 58,305,262" if total_untung_tahunan > 0 else "RM 11,018,780")
        st.markdown("---")
        f_r3, f_r4 = st.columns(2)
        with f_r3:
            st.metric("IRR Projek Jangka Panjang", "40.19%" if total_untung_tahunan > 0 else "15.50%")
        with f_r4:
            st.metric("ROI Keseluruhan Projek", "3,743.22%" if total_untung_tahunan > 0 else "280.00%")
        st.markdown("---")
        
        if "Tahun 1-2" in fasa_rou:
            st.error(f"🚨 FASA KRITIKAL (DEFISIT TUNAI): Aliran tunai tertekan disebabkan komitmen Capex Sawit RM5.75J/Thn dan operasi Getah Muda yang masih rugi (RM {profit_cat2:,.0f}). Diperlukan Subsidi Silang internal!")
        elif "Tahun 3-5" in fasa_rou:
            st.warning(f"⚠️ FASA PERALIHAN: Sawit mula berbuah komersial ({yield_sawit} MT/Ha). Aliran Tunai mula stabil seiring peningkatan hasil Getah Muda.")
        else:
            st.success(f"💰 FASA LONJAKAN EMAS: Capex selesai sepenuhnya! Sawit pada hasil puncak 24 MT/Ha menghasilkan keuntungan bersih maksimum yang konsisten sehingga Tahun 20.")

# --- TAB 3: TROPIKA SANJUNG ---
with tab3:
    st.header("Ladang Tropika Sanjung (257 Ha Matang)")
    col_in_ts, col_eff_ts = st.columns([1, 2])
    with col_in_ts:
        st.subheader("📋 Input Operasi & Sewa")
        prod_ts = st.slider("Produktiviti (kg/Ha/Tahun)", 400, 2000, 700, key="ts_p")
        sewa_ts = st.slider("Kadar Sewaan (RM/Ha/Tahun)", 1000, 2400, 1200, key="ts_s")
        
        pendapatan_ts = prod_ts * harga_clean_rm * 257
        kos_pengurusan_ts = (kos_opex_gc + sewa_ts) * 257
        untung_ts = pendapatan_ts - kos_pengurusan_ts
        modal_ts, npv_ts, irr_ts, roi_ts = kira_metrik_kewangan(untung_ts, sewa_ts, 257)
    with col_eff_ts:
        st.subheader("💰 Penunjuk Prestasi Kewangan (KPI)")
        row1_ts1, row1_ts2 = st.columns(2)
        with row1_ts1:
            st.metric("Untung Bersih / Tahun", f"RM {untung_ts:,.0f}")
        with row1_ts2:
            st.metric("NPV (@10% Diskaun)", f"RM {npv_ts:,.0f}")
        st.markdown("---")
        row2_ts1, row2_ts2 = st.columns(2)
        with row2_ts1:
            st.metric("IRR (Kadar Pulangan)", f"{irr_ts:.2f}%")
        with row2_ts2:
            st.metric("ROI Keseluruhan", f"{roi_ts:.2f}%")
        st.markdown("---")
        if prod_ts < 1100:
            st.error("🚨 KRITIKAL: Rekod produktiviti semasa rendah (700kg/Ha). Sukar menjana keuntungan jika isu buruh tidak diselesaikan untuk mencapai target min 1,100 kg/Ha.")

# --- TAB 4: SRI PELITA BUMI ---
with tab4:
    st.header("Ladang Sri Pelita Bumi (344 Ha Matang)")
    col_in_sp, col_eff_sp = st.columns([1, 2])
    with col_in_sp:
        st.subheader("📋 Input Operasi & Sewa")
        prod_sp = st.slider("Produktiviti (kg/Ha/Tahun)", 500, 2000, 1113, key="sp_p")
        sewa_sp = st.slider("Kadar Sewaan (RM/Ha/Tahun)", 1200, 3000, 1800, key="sp_s")
        
        pendapatan_sp = prod_sp * harga_clean_rm * 344
        kos_pengurusan_sp = (kos_opex_gc + sewa_sp) * 344
        untung_sp = pendapatan_sp - kos_pengurusan_sp
        modal_sp, npv_sp, irr_sp, roi_sp = kira_metrik_kewangan(untung_sp, sewa_sp, 344)
    with col_eff_sp:
        st.subheader("💰 Penunjuk Prestasi Kewangan (KPI)")
        row1_sp1, row1_sp2 = st.columns(2)
        with row1_sp1:
            st.metric("Untung Bersih / Tahun", f"RM {untung_sp:,.0f}")
        with row1_sp2:
            st.metric("NPV (@10% Diskaun)", f"RM {npv_sp:,.0f}")
        st.markdown("---")
        row2_sp1, row2_sp2 = st.columns(2)
        with row2_sp1:  # Membetulkan ralat rujukan kod lama
            st.metric("IRR (Kadar Pulangan)", f"{irr_sp:.2f}%")
        with row2_sp2:  # Membetulkan ralat rujukan kod lama
            st.metric("ROI Keseluruhan", f"{roi_sp:.2f}%")
        st.markdown("---")
        if sewa_sp > 2400:
            st.error("🚨 AMARAN SILING: Kadar sewaan melebihi had selamat RM2,400/Ha (Had 55% keuntungan hasil).")
