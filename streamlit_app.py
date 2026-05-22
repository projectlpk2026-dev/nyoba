import re
import streamlit as st
import pandas as pd
from datetime import datetime

# =========================================================
# DATABASE UNSUR
# =========================================================

unsur = {
    "H": {"nama": "Hidrogen", "nomor_atom": 1, "massa_atom": 1.008},
    "He": {"nama": "Helium", "nomor_atom": 2, "massa_atom": 4.0026},
    "Li": {"nama": "Litium", "nomor_atom": 3, "massa_atom": 6.94},
    "Be": {"nama": "Berilium", "nomor_atom": 4, "massa_atom": 9.0122},
    "B": {"nama": "Boron", "nomor_atom": 5, "massa_atom": 10.81},
    "C": {"nama": "Karbon", "nomor_atom": 6, "massa_atom": 12.011},
    "N": {"nama": "Nitrogen", "nomor_atom": 7, "massa_atom": 14.007},
    "O": {"nama": "Oksigen", "nomor_atom": 8, "massa_atom": 15.999},
    "F": {"nama": "Fluorin", "nomor_atom": 9, "massa_atom": 18.998},
    "Ne": {"nama": "Neon", "nomor_atom": 10, "massa_atom": 20.180},
    "Na": {"nama": "Natrium", "nomor_atom": 11, "massa_atom": 22.990},
    "Mg": {"nama": "Magnesium", "nomor_atom": 12, "massa_atom": 24.305},
    "Al": {"nama": "Aluminium", "nomor_atom": 13, "massa_atom": 26.982},
    "Si": {"nama": "Silikon", "nomor_atom": 14, "massa_atom": 28.085},
    "P": {"nama": "Fosfor", "nomor_atom": 15, "massa_atom": 30.974},
    "S": {"nama": "Sulfur", "nomor_atom": 16, "massa_atom": 32.06},
    "Cl": {"nama": "Klorin", "nomor_atom": 17, "massa_atom": 35.45},
    "Ar": {"nama": "Argon", "nomor_atom": 18, "massa_atom": 39.948},
    "K": {"nama": "Kalium", "nomor_atom": 19, "massa_atom": 39.098},
    "Ca": {"nama": "Kalsium", "nomor_atom": 20, "massa_atom": 40.078},
    "Sc": {"nama": "Skandium", "nomor_atom": 21, "massa_atom": 44.956},
    "Ti": {"nama": "Titanium", "nomor_atom": 22, "massa_atom": 47.867},
    "V": {"nama": "Vanadium", "nomor_atom": 23, "massa_atom": 50.942},
    "Cr": {"nama": "Kromium", "nomor_atom": 24, "massa_atom": 51.996},
    "Mn": {"nama": "Mangan", "nomor_atom": 25, "massa_atom": 54.938},
    "Fe": {"nama": "Besi", "nomor_atom": 26, "massa_atom": 55.845},
    "Co": {"nama": "Kobalt", "nomor_atom": 27, "massa_atom": 58.933},
    "Ni": {"nama": "Nikel", "nomor_atom": 28, "massa_atom": 58.693},
    "Cu": {"nama": "Tembaga", "nomor_atom": 29, "massa_atom": 63.546},
    "Zn": {"nama": "Seng", "nomor_atom": 30, "massa_atom": 65.38},
    "Ga": {"nama": "Galium", "nomor_atom": 31, "massa_atom": 69.723},
    "Ge": {"nama": "Germanium", "nomor_atom": 32, "massa_atom": 72.630},
    "As": {"nama": "Arsen", "nomor_atom": 33, "massa_atom": 74.922},
    "Se": {"nama": "Selenium", "nomor_atom": 34, "massa_atom": 78.971},
    "Br": {"nama": "Bromin", "nomor_atom": 35, "massa_atom": 79.904},
    "Kr": {"nama": "Kripton", "nomor_atom": 36, "massa_atom": 83.798},
    "Rb": {"nama": "Rubidium", "nomor_atom": 37, "massa_atom": 85.468},
    "Sr": {"nama": "Stronsium", "nomor_atom": 38, "massa_atom": 87.62},
    "Y": {"nama": "Itrium", "nomor_atom": 39, "massa_atom": 88.906},
    "Zr": {"nama": "Zirkonium", "nomor_atom": 40, "massa_atom": 91.224},
    "Nb": {"nama": "Niobium", "nomor_atom": 41, "massa_atom": 92.906},
    "Mo": {"nama": "Molibdenum", "nomor_atom": 42, "massa_atom": 95.95},
    "Tc": {"nama": "Teknesium", "nomor_atom": 43, "massa_atom": 98},
    "Ru": {"nama": "Rutenium", "nomor_atom": 44, "massa_atom": 101.07},
    "Rh": {"nama": "Rodium", "nomor_atom": 45, "massa_atom": 102.906},
    "Pd": {"nama": "Paladium", "nomor_atom": 46, "massa_atom": 106.42},
    "Ag": {"nama": "Perak", "nomor_atom": 47, "massa_atom": 107.868},
    "Cd": {"nama": "Kadmium", "nomor_atom": 48, "massa_atom": 112.414},
    "In": {"nama": "Indium", "nomor_atom": 49, "massa_atom": 114.818},
    "Sn": {"nama": "Timah", "nomor_atom": 50, "massa_atom": 118.710},
    "Sb": {"nama": "Antimon", "nomor_atom": 51, "massa_atom": 121.760},
    "Te": {"nama": "Telurium", "nomor_atom": 52, "massa_atom": 127.60},
    "I": {"nama": "Iodin", "nomor_atom": 53, "massa_atom": 126.904},
    "Xe": {"nama": "Xenon", "nomor_atom": 54, "massa_atom": 131.293},
    "Cs": {"nama": "Sesium", "nomor_atom": 55, "massa_atom": 132.905},
    "Ba": {"nama": "Barium", "nomor_atom": 56, "massa_atom": 137.327},
    "La": {"nama": "Lantanum", "nomor_atom": 57, "massa_atom": 138.905},
    "Ce": {"nama": "Serium", "nomor_atom": 58, "massa_atom": 140.116},
    "Pr": {"nama": "Praseodimium", "nomor_atom": 59, "massa_atom": 140.908},
    "Nd": {"nama": "Neodimium", "nomor_atom": 60, "massa_atom": 144.242},
    "Pm": {"nama": "Prometium", "nomor_atom": 61, "massa_atom": 145},
    "Sm": {"nama": "Samarium", "nomor_atom": 62, "massa_atom": 150.36},
    "Eu": {"nama": "Europium", "nomor_atom": 63, "massa_atom": 151.964},
    "Gd": {"nama": "Gadolinium", "nomor_atom": 64, "massa_atom": 157.25},
    "Tb": {"nama": "Terbium", "nomor_atom": 65, "massa_atom": 158.925},
    "Dy": {"nama": "Disprosium", "nomor_atom": 66, "massa_atom": 162.500},
    "Ho": {"nama": "Holmium", "nomor_atom": 67, "massa_atom": 164.930},
    "Er": {"nama": "Erbium", "nomor_atom": 68, "massa_atom": 167.259},
    "Tm": {"nama": "Tulium", "nomor_atom": 69, "massa_atom": 168.934},
    "Yb": {"nama": "Iterbium", "nomor_atom": 70, "massa_atom": 173.045},
    "Lu": {"nama": "Lutesium", "nomor_atom": 71, "massa_atom": 174.967},
    "Hf": {"nama": "Hafnium", "nomor_atom": 72, "massa_atom": 178.49},
    "Ta": {"nama": "Tantalum", "nomor_atom": 73, "massa_atom": 180.948},
    "W": {"nama": "Wolfram", "nomor_atom": 74, "massa_atom": 183.84},
    "Re": {"nama": "Renium", "nomor_atom": 75, "massa_atom": 186.207},
    "Os": {"nama": "Osmium", "nomor_atom": 76, "massa_atom": 190.23},
    "Ir": {"nama": "Iridium", "nomor_atom": 77, "massa_atom": 192.217},
    "Pt": {"nama": "Platina", "nomor_atom": 78, "massa_atom": 195.084},
    "Au": {"nama": "Emas", "nomor_atom": 79, "massa_atom": 196.967},
    "Hg": {"nama": "Merkuri", "nomor_atom": 80, "massa_atom": 200.592},
    "Tl": {"nama": "Talium", "nomor_atom": 81, "massa_atom": 204.38},
    "Pb": {"nama": "Timbal", "nomor_atom": 82, "massa_atom": 207.2},
    "Bi": {"nama": "Bismut", "nomor_atom": 83, "massa_atom": 208.980},
    "Po": {"nama": "Polonium", "nomor_atom": 84, "massa_atom": 209},
    "At": {"nama": "Astatin", "nomor_atom": 85, "massa_atom": 210},
    "Rn": {"nama": "Radon", "nomor_atom": 86, "massa_atom": 222},
    "Fr": {"nama": "Fransium", "nomor_atom": 87, "massa_atom": 223},
    "Ra": {"nama": "Radium", "nomor_atom": 88, "massa_atom": 226},
    "Ac": {"nama": "Aktinium", "nomor_atom": 89, "massa_atom": 227},
    "Th": {"nama": "Torium", "nomor_atom": 90, "massa_atom": 232.038},
    "Pa": {"nama": "Protaktinium", "nomor_atom": 91, "massa_atom": 231.036},
    "U": {"nama": "Uranium", "nomor_atom": 92, "massa_atom": 238.029},
    "Np": {"nama": "Neptunium", "nomor_atom": 93, "massa_atom": 237},
    "Pu": {"nama": "Plutonium", "nomor_atom": 94, "massa_atom": 244},
    "Am": {"nama": "Amerisium", "nomor_atom": 95, "massa_atom": 243},
    "Cm": {"nama": "Kurium", "nomor_atom": 96, "massa_atom": 247},
    "Bk": {"nama": "Berkelium", "nomor_atom": 97, "massa_atom": 247},
    "Cf": {"nama": "Kalifornium", "nomor_atom": 98, "massa_atom": 251},
    "Es": {"nama": "Einsteinium", "nomor_atom": 99, "massa_atom": 252},
    "Fm": {"nama": "Fermium", "nomor_atom": 100, "massa_atom": 257},
    "Md": {"nama": "Mendelevium", "nomor_atom": 101, "massa_atom": 258},
    "No": {"nama": "Nobelium", "nomor_atom": 102, "massa_atom": 259},
    "Lr": {"nama": "Lawrensium", "nomor_atom": 103, "massa_atom": 266},
    "Rf": {"nama": "Rutherfordium", "nomor_atom": 104, "massa_atom": 267},
    "Db": {"nama": "Dubnium", "nomor_atom": 105, "massa_atom": 268},
    "Sg": {"nama": "Seaborgium", "nomor_atom": 106, "massa_atom": 269},
    "Bh": {"nama": "Bohrium", "nomor_atom": 107, "massa_atom": 270},
    "Hs": {"nama": "Hassium", "nomor_atom": 108, "massa_atom": 277},
    "Mt": {"nama": "Meitnerium", "nomor_atom": 109, "massa_atom": 278},
    "Ds": {"nama": "Darmstadtium", "nomor_atom": 110, "massa_atom": 281},
    "Rg": {"nama": "Roentgenium", "nomor_atom": 111, "massa_atom": 282},
    "Cn": {"nama": "Kopernisium", "nomor_atom": 112, "massa_atom": 285},
    "Nh": {"nama": "Nihonium", "nomor_atom": 113, "massa_atom": 286},
    "Fl": {"nama": "Flerovium", "nomor_atom": 114, "massa_atom": 289},
    "Mc": {"nama": "Moskovium", "nomor_atom": 115, "massa_atom": 290},
    "Lv": {"nama": "Livermorium", "nomor_atom": 116, "massa_atom": 293},
    "Ts": {"nama": "Tenesin", "nomor_atom": 117, "massa_atom": 294},
    "Og": {"nama": "Oganeson", "nomor_atom": 118, "massa_atom": 294}
}

CONTOH_RUMUS = {
    "Air": "H2O",
    "Karbon dioksida": "CO2",
    "Garam dapur": "NaCl",
    "Glukosa": "C6H12O6",
    "Kalsium hidroksida": "Ca(OH)2",
    "Aluminium sulfat": "Al2(SO4)3",
    "FAS": "Fe(NH4)2(SO4)2(H2O)6",
    "Asam sulfat": "H2SO4",
    "Kalium permanganat": "KMnO4",
    "Kalsium karbonat": "CaCO3"
}

# =========================================================
# STYLE CSS
# =========================================================

st.set_page_config(
    page_title="Kalkulator BM/MR Kimia",
    page_icon="⚗️",
    layout="wide"
)

st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .hero {
        padding: 28px;
        border-radius: 24px;
        background: linear-gradient(135deg, #152e67 0%, #2563eb 65%, #38bdf8 100%);
        color: white;
        box-shadow: 0 12px 35px rgba(21, 46, 103, 0.25);
        margin-bottom: 24px;
    }
    .hero h1 {
        font-size: 42px;
        margin-bottom: 4px;
    }
    .hero p {
        font-size: 17px;
        opacity: 0.95;
    }
    .metric-card {
        padding: 22px;
        border-radius: 20px;
        background: white;
        box-shadow: 0 8px 28px rgba(15, 23, 42, 0.08);
        border: 1px solid #e5e7eb;
    }
    .metric-title {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 6px;
    }
    .metric-value {
        color: #152e67;
        font-size: 30px;
        font-weight: 800;
    }
    .formula-box {
        padding: 18px;
        border-radius: 18px;
        background: #eff6ff;
        border-left: 6px solid #2563eb;
        color: #1e3a8a;
        font-weight: 600;
        font-size: 18px;
    }
    .chat-user {
        padding: 12px 14px;
        background: #dbeafe;
        border-radius: 14px;
        margin-bottom: 8px;
    }
    .chat-bot {
        padding: 12px 14px;
        background: #f1f5f9;
        border-radius: 14px;
        margin-bottom: 12px;
    }
    .small-note {
        color: #64748b;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNGSI PARSING DAN HITUNG
# =========================================================

def bersihkan_rumus(rumus):
    return rumus.strip().replace(" ", "")

def parse_rumus(rumus):
    stack = [{}]
    i = 0

    while i < len(rumus):
        karakter = rumus[i]

        if karakter == "(":
            stack.append({})
            i += 1

        elif karakter == ")":
            if len(stack) == 1:
                raise ValueError("Tanda kurung tidak sesuai.")
            grup = stack.pop()
            i += 1

            angka = ""
            while i < len(rumus) and rumus[i].isdigit():
                angka += rumus[i]
                i += 1

            pengali = int(angka) if angka else 1

            for simbol, jumlah in grup.items():
                stack[-1][simbol] = stack[-1].get(simbol, 0) + jumlah * pengali

        elif karakter.isupper():
            simbol = karakter
            i += 1

            if i < len(rumus) and rumus[i].islower():
                simbol += rumus[i]
                i += 1

            angka = ""
            while i < len(rumus) and rumus[i].isdigit():
                angka += rumus[i]
                i += 1

            jumlah = int(angka) if angka else 1
            stack[-1][simbol] = stack[-1].get(simbol, 0) + jumlah

        else:
            raise ValueError("Format rumus kimia tidak valid. Gunakan huruf besar-kecil yang benar, contoh: NaCl, bukan nacl.")

    if len(stack) != 1:
        raise ValueError("Tanda kurung tidak sesuai.")

    return stack[0]

def hitung_bobot_molekul(rumus):
    rumus = bersihkan_rumus(rumus)

    if rumus == "":
        return None, None, "Rumus kimia tidak boleh kosong."

    try:
        hasil_parse = parse_rumus(rumus)
    except ValueError as e:
        return None, None, str(e)

    total = 0
    detail = []

    for simbol, jumlah_atom in hasil_parse.items():
        if simbol not in unsur:
            return None, None, f"Unsur '{simbol}' tidak ditemukan dalam database."

        data = unsur[simbol]
        massa_atom = data["massa_atom"]
        subtotal = massa_atom * jumlah_atom
        total += subtotal

        detail.append({
            "Simbol Unsur": simbol,
            "Nama Unsur": data["nama"],
            "Nomor Atom": data["nomor_atom"],
            "Jumlah Atom": jumlah_atom,
            "Massa Atom": massa_atom,
            "Subtotal Massa": round(subtotal, 3),
            "Persentase Massa (%)": 0
        })

    for item in detail:
        item["Persentase Massa (%)"] = round((item["Subtotal Massa"] / total) * 100, 2)

    return round(total, 3), detail, None

def buat_pembahasan_otomatis(rumus, total, detail):
    unsur_terlibat = ", ".join([f"{d['Nama Unsur']} ({d['Simbol Unsur']})" for d in detail])
    rincian = "; ".join([
        f"{d['Simbol Unsur']} sebanyak {d['Jumlah Atom']} atom dengan subtotal massa {d['Subtotal Massa']} g/mol"
        for d in detail
    ])

    dominan = max(detail, key=lambda x: x["Subtotal Massa"])

    return (
        f"Berdasarkan hasil perhitungan, senyawa dengan rumus kimia {rumus} tersusun atas unsur {unsur_terlibat}. "
        f"Perhitungan bobot molekul dilakukan dengan mengalikan massa atom relatif setiap unsur dengan jumlah atomnya, "
        f"kemudian seluruh subtotal massa dijumlahkan. Rinciannya adalah {rincian}. "
        f"Dari hasil tersebut diperoleh nilai BM/Mr {rumus} sebesar {total} g/mol. "
        f"Unsur yang memberikan kontribusi massa terbesar adalah {dominan['Nama Unsur']} ({dominan['Simbol Unsur']}) "
        f"dengan persentase massa sekitar {dominan['Persentase Massa (%)']}%. "
        f"Nilai ini menunjukkan massa satu mol senyawa {rumus} dalam satuan gram per mol dan dapat digunakan untuk "
        f"perhitungan stoikiometri, pembuatan larutan, maupun analisis kuantitatif."
    )

def jawab_chatbot(pertanyaan):
    teks = pertanyaan.lower().strip()

    if teks == "":
        return "Tulis pertanyaan dulu. Chatbot mini ini belum bisa membaca pikiran, untungnya."

    if "bm" in teks or "mr" in teks or "bobot molekul" in teks:
        rumus_match = re.findall(r"[A-Z][a-z]?\d*|\(|\)\d*", pertanyaan)
        if rumus_match:
            kandidat = "".join(rumus_match)
            total, detail, error = hitung_bobot_molekul(kandidat)
            if error:
                return error
            return f"BM/Mr {kandidat} = {total} g/mol."
        return "BM atau Mr adalah jumlah massa atom relatif semua unsur dalam suatu senyawa."

    if "cara" in teks and ("hitung" in teks or "menghitung" in teks):
        return (
            "Cara menghitung BM/Mr: pisahkan unsur dalam rumus kimia, tentukan jumlah atom tiap unsur, "
            "kalikan jumlah atom dengan massa atom relatifnya, lalu jumlahkan semua hasilnya."
        )

    if "fas" in teks:
        total, detail, error = hitung_bobot_molekul("Fe(NH4)2(SO4)2(H2O)6")
        return f"Rumus FAS yang umum digunakan adalah Fe(NH4)2(SO4)2·6H2O. BM/Mr-nya sekitar {total} g/mol."

    if "contoh" in teks:
        return "Contoh rumus yang bisa dihitung: H2O, CO2, NaCl, C6H12O6, Ca(OH)2, Al2(SO4)3, KMnO4, dan FAS."

    return (
        "Saya bisa membantu menjelaskan BM/Mr, cara hitung, contoh rumus, atau menghitung langsung rumus kimia. "
        "Contoh pertanyaan: 'hitung Mr H2SO4' atau 'apa itu BM?'."
    )

# =========================================================
# SESSION STATE
# =========================================================

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <h1>⚗️ Kalkulator BM / Mr Kimia</h1>
    <p>Aplikasi interaktif untuk menghitung bobot molekul, massa molekul relatif, persentase massa unsur, pembahasan otomatis, riwayat pencarian, dan chatbot mini.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.header("⚙️ Menu Aplikasi")
    menu = st.radio(
        "Pilih fitur",
        ["Kalkulator BM/Mr", "Riwayat Pencarian", "Chatbot Mini", "Database Unsur"]
    )

    st.divider()
    st.subheader("Contoh Rumus")
    pilihan_contoh = st.selectbox("Pilih contoh senyawa", list(CONTOH_RUMUS.keys()))
    st.code(CONTOH_RUMUS[pilihan_contoh])

    st.caption("Catatan: penulisan rumus harus benar, misalnya NaCl, bukan nacl.")

# =========================================================
# MENU KALKULATOR
# =========================================================

if menu == "Kalkulator BM/Mr":
    col_input, col_info = st.columns([1.2, 0.8])

    with col_input:
        st.subheader("🧪 Input Rumus Kimia")
        mode = st.radio("Jenis perhitungan", ["BM / Mr Senyawa", "Massa per Unsur"], horizontal=True)

        rumus_default = CONTOH_RUMUS[pilihan_contoh]
        rumus = st.text_input(
            "Masukkan rumus kimia",
            value=rumus_default,
            placeholder="Contoh: H2O, CO2, NaCl, Ca(OH)2, Al2(SO4)3"
        )

        tombol = st.button("🔍 Hitung Sekarang", use_container_width=True)

    with col_info:
        st.subheader("📌 Petunjuk Singkat")
        st.markdown("""
        <div class="formula-box">
            BM/Mr = Σ (massa atom × jumlah atom)
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <p class="small-note">
        Gunakan tanda kurung untuk gugus senyawa, misalnya Ca(OH)2 atau Al2(SO4)3.
        Program ini juga bisa membaca rumus FAS: Fe(NH4)2(SO4)2(H2O)6.
        </p>
        """, unsafe_allow_html=True)

    if tombol:
        total, detail, error = hitung_bobot_molekul(rumus)

        if error:
            st.error(error)
        else:
            df = pd.DataFrame(detail)
            rumus_bersih = bersihkan_rumus(rumus)

            st.session_state.riwayat.insert(0, {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Rumus": rumus_bersih,
                "BM/Mr": total
            })

            st.success("Perhitungan berhasil.")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Rumus Kimia</div>
                    <div class="metric-value">{rumus_bersih}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total BM/Mr</div>
                    <div class="metric-value">{total}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Jumlah Jenis Unsur</div>
                    <div class="metric-value">{len(detail)}</div>
                </div>
                """, unsafe_allow_html=True)
