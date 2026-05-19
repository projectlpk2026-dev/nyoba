import streamlit as st
import math

# =====================================================
# DATABASE ALAT LAB
# =====================================================

alat_lab = [

    "Alu",
    "Batang Pengaduk",
    "Beaker Glass",
    "Botol Reagen",
    "Botol Timbang",
    "Botol Semprot",
    "Buret",
    "Bunsen",
    "Cawan Petri",
    "Corong Kaca",
    "Cawan Porselen",
    "Corong Pisah",
    "Desikator",
    "Erlenmeyer",
    "Gelas Ukur",
    "Gegep Besi",
    "Gegep Kayu",
    "Hot Plate",
    "Inkubator",
    "Jarum Ose",
    "Kaca Arloji",
    "Kaki Tiga",
    "Kasa Asbes",
    "Kertas Saring",
    "Klem Buret",
    "Kuvet",
    "Labu Alas Bulat",
    "Labu Takar",
    "Laminar Air Flow",
    "Mikropipet",
    "Mortar",
    "Mekker",
    "Neraca Analitik",
    "Oven",
    "pH meter",
    "Pipet Volume",
    "Pipet Tetes",
    "Pipet Mohr",
    "Piknometer",
    "Polismen",
    "Rak Tabung Reaksi",
    "Sentrifus",
    "Segitiga Porselen",
    "Spatula",
    "Spektrofotometer",
    "Statif",
    "Spirtus",
    "Soxhlet",
    "Tabung Reaksi",
    "Tanur",
    "Tutup Kaca",
    "Termometer",
    "Vortex",
    "Water bath"
]

# =====================================================
# HEADER
# =====================================================

st.title("🧪 APLIKASI LABORATORIUM KIMIA")

menu = st.sidebar.selectbox(
    "MENU UTAMA",
    [
        "Cek Stok Alat Laboratorium",
        "Kalkulator Molaritas",
        "Kalkulator Pengenceran",
        "Kalkulator Kadar",
        "Kalkulator pH"
    ]
)

# =====================================================
# MENU CEK ALAT
# =====================================================

if menu == "Cek Stok Alat Laboratorium":

    st.header("CEK STOK ALAT LABORATORIUM")

    cari = st.text_input("Cari alat apa?")

    if st.button("Cek Alat"):

        if cari.title() in alat_lab:
            st.success(f"Alat '{cari}' TERSEDIA di laboratorium")

        else:
            st.error(f"Alat '{cari}' TIDAK DITEMUKAN")

    if st.checkbox("Tampilkan Semua Alat"):
        for alat in alat_lab:
            st.write("-", alat)

# =====================================================
# MENU MOLARITAS
# =====================================================

elif menu == "Kalkulator Molaritas":

    st.header("KALKULATOR MOLARITAS")

    mol = st.number_input("Masukkan jumlah mol (mol):", min_value=0.0)
    volume = st.number_input("Masukkan volume larutan (L):", min_value=0.0001)

    if st.button("Hitung Molaritas"):

        hasil = mol / volume

        st.success(f"Molaritas = {round(hasil, 3)} M")

# =====================================================
# MENU PENGENCERAN
# =====================================================

elif menu == "Kalkulator Pengenceran":

    st.header("KALKULATOR PENGENCERAN")

    M1 = st.number_input("Masukkan M1 (M):", min_value=0.0)
    V1 = st.number_input("Masukkan V1 (mL):", min_value=0.0)
    M2 = st.number_input("Masukkan M2 (M):", min_value=0.0001)

    if st.button("Hitung Pengenceran"):

        V2 = (M1 * V1) / M2

        st.success(f"V2 = {round(V2, 2)} mL")

# =====================================================
# MENU KADAR
# =====================================================

elif menu == "Kalkulator Kadar":

    pilihan = st.selectbox(
        "Pilih Jenis Kadar",
        [
            "Kadar Asam Asetat",
            "NaOH dan Na2CO3 (Warder)",
            "Kadar Besi(Fe)",
            "Kadar Klorida(Cl) Iodometri",
            "Kadar Klorida(Cl) Argentometri",
            "Kesadahan Air"
        ]
    )

    # =====================================================
    # KADAR ASAM ASETAT
    # =====================================================

    if pilihan == "Kadar Asam Asetat":

        V = st.number_input("Volume titrasi/V(mL)")
        N = st.number_input("Normalitas/N(mgrek/mL)")
        FP = st.number_input("Faktor pengenceran")
        V_sampel = st.number_input("Volume sampel (mL)")

        if st.button("Hitung"):

            hasil = ((V * N * 60) * (10**-3) * FP * 100) / V_sampel

            st.success(f"Kadar CH3COOH = {round(hasil,2)} %")

    # =====================================================
    # WARDER
    # =====================================================

    elif pilihan == "NaOH dan Na2CO3 (Warder)":

        a = st.number_input("Volume titrasi 1/a(mL)")
        b = st.number_input("Volume titrasi 2/b(mL)")
        N = st.number_input("Normalitas/N(mgrek/mL)")
        V_sampel = st.number_input("Volume sampel (mL)")

        if st.button("Hitung"):

            BE_NaOH = 40
            BE_Na2CO3 = 53

            Na2CO3 = ((2 * (b-a)* N * BE_Na2CO3) * (10**-3) * 100) / V_sampel
            NaOH = ((2*a - b)* N * BE_NaOH) * (10**-3) * 100 / V_sampel

            st.success(f"Kadar NaOH = {round(NaOH,2)} %")
            st.success(f"Kadar Na2CO3 = {round(Na2CO3,2)} %")

    # =====================================================
    # BESI
    # =====================================================

    elif pilihan == "Kadar Besi(Fe)":

        V = st.number_input("Volume titrasi/V(mL)")
        N = st.number_input("Normalitas/N(mgrek/mL)")
        V_sampel = st.number_input("Volume sampel (mL)")

        if st.button("Hitung"):

            hasil = ((V * N * 56) * (10**-3) * 100) / V_sampel

            st.success(f"Kadar Fe = {round(hasil,2)} %")

    # =====================================================
    # IODOMETRI
    # =====================================================

    elif pilihan == "Kadar Klorida(Cl) Iodometri":

        V = st.number_input("Volume titrasi/V(mL)")
        N = st.number_input("Normalitas/N(mgrek/mL)")
        V_sampel = st.number_input("Volume sampel (mL)")

        if st.button("Hitung"):

            hasil = ((V * N * 17.75) * (10**-3) * 100/5 * 100) / V_sampel

            st.success(f"Kadar Cl = {round(hasil,2)} %")

    # =====================================================
    # ARGENTOMETRI
    # =====================================================

    elif pilihan == "Kadar Klorida(Cl) Argentometri":

        V = st.number_input("Volume titrasi/V(mL)")
        N = st.number_input("Normalitas/N(mgrek/mL)")
        V_sampel = st.number_input("Volume sampel (mL)")

        if st.button("Hitung"):

            hasil = ((V * N * 35.5) * (10**-3) * 100) / V_sampel

            st.success(f"Kadar Cl = {round(hasil,2)} %")

    # =====================================================
    # KESADAHAN
    # =====================================================

    elif pilihan == "Kesadahan Air":

        V = st.number_input("Volume titrasi/V(mL)")
        M = st.number_input("Molaritas/M(mmol/mL)")
        V_sampel = st.number_input("Volume sampel (L)")

        if st.button("Hitung"):

            hasil = ((V * M * 100)) / V_sampel

            st.success(f"Kadar CaCO3 = {round(hasil,2)} %")

# =====================================================
# MENU pH
# =====================================================

elif menu == "Kalkulator pH":

    st.header("KALKULATOR pH")

    h = st.number_input("Masukkan konsentrasi H+ (mol/L):", min_value=0.0000001)

    if st.button("Hitung pH"):

        hasil = -math.log10(h)

        st.success(f"pH = {round(hasil,2)}")
