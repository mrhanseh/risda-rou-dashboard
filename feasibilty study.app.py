import streamlit as st

st.set_page_config(page_title="RISDA RoU Financial Dashboard", layout="wide")

st.title("📊 Dashboard Analisis Kebolehlaksanaan RoU RISDA")
st.caption("Simulasi Dinamik Berasaskan Produktiviti Hasil, Kos Operasi, dan Kadar Sewaan Estet")

# --- SIDEBAR: PARAMETER PASARAN GLOBAL ---
st.sidebar.header("⚙️ Parameter Pasaran Global")

# Input Harga SMR 20 dan Insentif
harga_smr20 = st.sidebar.slider("Harga SMR 20 (sen/kg)", 500, 1200, 790)
insentif_risda = st.sidebar.slider("Insentif RISDA (sen/kg)", 0, 200, 100)
diskaun_kilang = st.sidebar.slider("Kos Pemprosesan/Diskaun (sen/kg)", 50, 200, 130)

# Parameter Input Kos Operasi + GC secara global
kos_opex_gc = st.sidebar.slider("Kos Operasi + GC (RM/Ha/Tahun)", 5000, 12000, 7000)

# Pengiraan Harga Bersih SMR 20 (RM/kg)
harga_bersih_rm = (harga_smr20 + insentif_risda - diskaun_kilang) / 100

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Hasil Unjuran")
st.sidebar.metric(label="Harga Bersih SMR 20", value=f"RM {harga_bersih_rm:.2f}/kg")

if harga_bersih_rm < 6.00:
    st.sidebar.error("⚠️ KLAUSA PENURUNAN SEWA: Harga bersih bawah RM6.00/kg. Disyorkan potongan sewa 20%.")

# --- FUNGSI DIALAMI UNTUK NPV, IRR, ROI ---
def kira_metrik_kewangan(untung_tahunan, kadar_sewa, keluasan, tempoh_tahun=6):
    modal_terikat = kadar_sewa * keluasan
    if modal_terikat <= 0 or untung_tahunan <= 0:
        return modal_terikat, 0.0, 0.0, 0.0
    
    # Formula IRR mengikut draf dokumen: (Untung Operasi / Modal Terikat) * 100
    irr = (untung_tahunan / modal_terikat) * 100
    # ROI = IRR * Tempoh Projek (6 Tahun)
    roi = irr * tempoh_tahun
    
    # Aliran Tunai NPV Jangka Pendek (6 Tahun) dengan kos modal 10%
    aliran_tunai = [-modal_terikat] + [untung_tahunan] * tempoh_tahun
    npv = sum([cf / (1.10**t) for t, cf in enumerate(aliran_tunai)])
    
    return modal_terikat, npv, irr, roi

# Tabs Mengikut Ladang
tab1, tab2, tab3 = st.tabs(["🌳 Anjakan Wawasan", "🍂 Tropika Sanjung", "🌱 Sri Pelita Bumi"])

# --- TAB 1: ANJAKAN WAWASAN ---
with tab1:
    st.header("Ladang Anjakan Wawasan (2,300 Ha Matang)")
    col_in, col_eff = st.columns([1, 2])
    
    with col_in:
        st.subheader("📋 Input Operasi & Sewa")
        prod_aw = st.slider("Produktiviti (kg/Ha/Tahun)", 500, 2500, 1500, key="aw_p")
        sewa_aw = st.slider("Kadar Sewaan (RM/Ha/Tahun)", 1200, 3600, 2400, key="aw_s")
        
        pendapatan_aw = prod_aw * harga_bersih_rm * 2300
        kos_pengurusan_aw = (kos_opex_gc + sewa_aw) * 2300
        untung_aw = pendapatan_aw - kos_pengurusan_aw
        
        modal_aw, npv_aw, irr_aw, roi_aw = kira_metrik_kewangan(untung_aw, sewa_aw, 2300)
        
    with col_eff:
        st.subheader("💰 Penunjuk Prestasi Kewangan (KPI)")
        
        # Redesign kepada format Grid 2x2 untuk ruang yang lebih luas
        row1_c1, row1_c2 = st.columns(2)
        with row1_c1:
            st.metric("Untung Bersih/Tahun", f"RM {untung_aw:,.0f}")
        with row1_c2:
            st.metric("NPV (@10%)", f"RM {npv_aw:,.0f}")
            
        st.markdown("---") # Garis pemisah antara baris metric
        
        row2_c1, row2_c2 = st.columns(2)
        with row2_c1:
            st.metric("IRR (%)", f"{irr_aw:.2f}%")
        with row2_c2:
            st.metric("ROI (%)", f"{roi_aw:.2f}%")
            
        st.markdown("---")
        
        if untung_aw < 0:
            st.error("🚨 AMARAN: Aliran tunai negatif! Sila tingkatkan produktiviti atau runding semula kadar sewaan.")
        elif irr_aw < 46.67:
            st.warning("⚠️ ZON RISIKO: Pulangan kewangan berada di bawah tahap unjuran optimum.")
        else:
            st.success("✅ PROJEK VIABLE: Kadar pulangan pelaburan berada dalam zon selamat.")

# --- TAB 2: TROPIKA SANJUNG ---
with tab2:
    st.header("Ladang Tropika Sanjung (257 Ha Matang)")
    col_in_ts, col_eff_ts = st.columns([1, 2])
    
    with col_in_ts:
        st.subheader("📋 Input Operasi & Sewa")
        prod_ts = st.slider("Produktiviti (kg/Ha/Tahun)", 400, 2000, 700, key="ts_p")
        sewa_ts = st.slider("Kadar Sewaan (RM/Ha/Tahun)", 1000, 2400, 1200, key="ts_s")
        
        pendapatan_ts = prod_ts * harga_bersih_rm * 257
        kos_pengurusan_ts = (kos_opex_gc + sewa_ts) * 257
        untung_ts = pendapatan_ts - kos_pengurusan_ts
        
        modal_ts, npv_ts, irr_ts, roi_ts = kira_metrik_kewangan(untung_ts, sewa_ts, 257)
        
    with col_eff_ts:
        st.subheader("💰 Penunjuk Prestasi Kewangan (KPI)")
        
        # Redesign Grid 2x2
        row1_ts1, row1_ts2 = st.columns(2)
        with row1_ts1:
            st.metric("Untung Bersih/Tahun", f"RM {untung_ts:,.0f}")
        with row1_ts2:
            st.metric("NPV (@10%)", f"RM {npv_ts:,.0f}")
            
        st.markdown("---")
        
        row2_ts1, row2_ts2 = st.columns(2)
        with row2_ts1:
            st.metric("IRR (%)", f"{irr_ts:.2f}%")
        with row2_ts2:
            st.metric("ROI (%)", f"{roi_ts:.2f}%")
            
        st.markdown("---")
        
        if prod_ts < 1100:
            st.error("🚨 KRITIKAL: Rekod produktiviti semasa rendah (700gg/Ha). Sukar menjana keuntungan jika isu buruh tidak diselesaikan untuk mencapai target min 1,100 kg/Ha.")
        elif untung_ts > 0:
            st.success("✅ Untung bersih dicapai melalui peningkatan produktiviti.")

# --- TAB 3: SRI PELITA BUMI ---
with tab3:
    st.header("Ladang Sri Pelita Bumi (344 Ha Matang)")
    col_in_sp, col_eff_sp = st.columns([1, 2])
    
    with col_in_sp:
        st.subheader("📋 Input Operasi & Sewa")
        prod_sp = st.slider("Produktiviti (kg/Ha/Tahun)", 500, 2000, 1113, key="sp_p")
        sewa_sp = st.slider("Kadar Sewaan (RM/Ha/Tahun)", 1200, 3000, 1800, key="sp_s")
        
        pendapatan_sp = prod_sp * harga_bersih_rm * 344
        kos_pengurusan_sp = (kos_opex_gc + sewa_sp) * 344
        untung_sp = pendapatan_sp - kos_pengurusan_sp
        
        modal_sp, npv_sp, irr_sp, roi_sp = kira_metrik_kewangan(untung_sp, sewa_sp, 344)
        
    with col_eff_sp:
        st.subheader("💰 Penunjuk Prestasi Kewangan (KPI)")
        
        # Redesign Grid 2x2
        row1_sp1, row1_sp2 = st.columns(2)
        with row1_sp1:
            st.metric("Untung Bersih/Tahun", f"RM {untung_sp:,.0f}")
        with row1_sp2:
            st.metric("NPV (@10%)", f"RM {npv_sp:,.0f}")
            
        st.markdown("---")
        
        row2_sp1, row2_sp2 = st.columns(2)
        with row2_c1:
            st.metric("IRR (%)", f"{irr_sp:.2f}%")
        with row2_c2:
            st.metric("ROI (%)", f"{roi_sp:.2f}%")
            
        st.markdown("---")
        
        if sewa_sp > 2400:
            st.error("🚨 AMARAN SILING: Kadar sewaan melebihi had selamat RM2,400/Ha (Had 55% keuntungan hasil). Margin agensi berisiko terhapus jika harga komoditi jatuh.")
