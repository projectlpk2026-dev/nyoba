import re
import sqlite3
from datetime import datetime

import pandas as pd
import streamlit as st

# ==============================================================================
# PROYEK: KALKULATOR BOBOT MOLEKUL / BM / Mr
# Tampilan UI Interaktif dengan Database SQLite, Riwayat, Detail Unsur, dan AI Mini
# ==============================================================================

st.set_page_config(
    page_title="Kalkulator Bobot Molekul",
    page_icon="⚗️",
    layout="wide"
)

DB_FILE = "molecular_weight_history.db"

# ==============================================================================
# DATABASE UNSUR LENGKAP 1-118
# ==============================================================================

DATA_UNSUR = """
H,Hidrogen,1,1.008
He,Helium,2,4.0026
Li,Litium,3,6.94
Be,Berilium,4,9.0122
B,Boron,5,10.81
C,Karbon,6,12.011
N,Nitrogen,7,14.007
O,Oksigen,8,15.999
F,Fluorin,9,18.998
Ne,Neon,10,20.180
Na,Natrium,11,22.990
Mg,Magnesium,12,24.305
Al,Aluminium,13,26.982
Si,Silikon,14,28.085
P,Fosfor,15,30.974
S,Sulfur,16,32.06
Cl,Klorin,17,35.45
Ar,Argon,18,39.948
K,Kalium,19,39.098
Ca,Kalsium,20,40.078
Sc,Skandium,21,44.956
Ti,Titanium,22,47.867
V,Vanadium,23,50.942
Cr,Kromium,24,51.996
Mn,Mangan,25,54.938
Fe,Besi,26,55.845
Co,Kobalt,27,58.933
Ni,Nikel,28,58.693
Cu,Tembaga,29,63.546
Zn,Seng,30,65.38
Ga,Galium,31,69.723
Ge,Germanium,32,72.630
As,Arsen,33,74.922
Se,Selenium,34,78.971
Br,Bromin,35,79.904
Kr,Kripton,36,83.798
Rb,Rubidium,37,85.468
Sr,Stronsium,38,87.62
Y,Itrium,39,88.906
Zr,Zirkonium,40,91.224
Nb,Niobium,41,92.906
Mo,Molibdenum,42,95.95
Tc,Teknesium,43,98
Ru,Rutenium,44,101.07
Rh,Rodium,45,102.906
Pd,Paladium,46,106.42
Ag,Perak,47,107.868
Cd,Kadmium,48,112.414
In,Indium,49,114.818
Sn,Timah,50,118.710
Sb,Antimon,51,121.760
Te,Telurium,52,127.60
I,Iodin,53,126.904
Xe,Xenon,54,131.293
Cs,Sesium,55,132.905
Ba,Barium,56,137.327
La,Lantanum,57,138.905
Ce,Serium,58,140.116
Pr,Praseodimium,59,140.908
Nd,Neodimium,60,144.242
Pm,Prometium,61,145
Sm,Samarium,62,150.36
Eu,Europium,63,151.964
Gd,Gadolinium,64,157.25
Tb,Terbium,65,158.925
Dy,Disprosium,66,162.500
Ho,Holmium,67,164.930
Er,Erbium,68,167.259
Tm,Tulium,69,168.934
Yb,Iterbium,70,173.045
Lu,Lutesium,71,174.967
Hf,Hafnium,72,178.49
Ta,Tantalum,73,180.948
W,Wolfram,74,183.84
Re,Renium,75,186.207
Os,Osmium,76,190.23
Ir,Iridium,77,192.217
Pt,Platina,78,195.084
Au,Emas,79,196.967
Hg,Merkuri,80,200.592
Tl,Talium,81,204.38
Pb,Timbal,82,207.2
Bi,Bismut,83,208.980
Po,Polonium,84,209
At,Astatin,85,210
Rn,Radon,86,222
Fr,Fransium,87,223
Ra,Radium,88,226
Ac,Aktinium,89,227
Th,Torium,90,232.038
Pa,Protaktinium,91,231.036
U,Uranium,92,238.029
Np,Neptunium,93,237
Pu,Plutonium,94,244
Am,Amerisium,95,243
Cm,Kurium,96,247
Bk,Berkelium,97,247
Cf,Kalifornium,98,251
Es,Einsteinium,99,252
Fm,Fermium,100,257
Md,Mendelevium,101,258
No,Nobelium,102,259
Lr,Lawrensium,103,266
Rf,Rutherfordium,104,267
Db,Dubnium,105,268
Sg,Seaborgium,106,269
Bh,Bohrium,107,270
Hs,Hassium,108,277
Mt,Meitnerium,109,278
Ds,Darmstadtium,110,281
Rg,Roentgenium,111,282
Cn,Kopernisium,112,285
Nh,Nihonium,113,286
Fl,Flerovium,114,289
Mc,Moskovium,115,290
Lv,Livermorium,116,293
Ts,Tenesin,117,294
Og,Oganeson,118,294
""".strip()

unsur = {}
for line in DATA_UNSUR.splitlines():
    simbol, nama, nomor_atom, massa_atom = line.split(",")
    unsur[simbol] = {
        "nama": nama,
        "nomor_atom": int(nomor_atom),
        "massa_atom": float(massa_atom)
    }

# ==============================================================================
# DATABASE SQLITE
# ==============================================================================

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history_bm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT,
            rumus TEXT,
            total_bm REAL,
            jumlah_unsur INTEGER,
            jumlah_atom INTEGER,
            detail TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_bm (
            topik TEXT PRIMARY KEY,
            penjelasan TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM knowledge_bm")
    if cursor.fetchone()[0] == 0:
        knowledge_awal = [
            ("mr", "Mr atau massa molekul relatif adalah jumlah massa atom relatif dari seluruh atom penyusun suatu senyawa."),
            ("bm", "BM atau bobot molekul sering dinyatakan dalam satuan g/mol dan digunakan untuk perhitungan mol, konsentrasi, serta pembuatan larutan."),
            ("hidrat", "Senyawa hidrat mengandung molekul air kristal. Contoh: CuSO4.5H2O atau CuSO4·5H2O."),
            ("kurung", "Tanda kurung digunakan untuk mengalikan gugus atom. Contoh: Ca(OH)2 berarti Ca sebanyak 1, O sebanyak 2, dan H sebanyak 2."),
            ("fas", "FAS atau ferro ammonium sulfate memiliki rumus umum Fe(NH4)2(SO4)2.6H2O.")
        ]
        cursor.executemany("INSERT OR IGNORE INTO knowledge_bm VALUES (?, ?)", knowledge_awal)

    conn.commit()
    conn.close()

def save_history(rumus, total_bm, detail_df):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    jumlah_unsur = len(detail_df)
    jumlah_atom = int(detail_df["Jumlah Atom"].sum())
    detail = detail_df.to_json(orient="records", force_ascii=False)

    cursor.execute("""
        INSERT INTO history_bm (waktu, rumus, total_bm, jumlah_unsur, jumlah_atom, detail)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        rumus,
        float(total_bm),
        jumlah_unsur,
        jumlah_atom,
        detail
    ))

    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(
        "SELECT waktu, rumus, total_bm, jumlah_unsur, jumlah_atom FROM history_bm ORDER BY id DESC",
        conn
    )
    conn.close()
    return df

def clear_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history_bm")
    conn.commit()
    conn.close()

def get_knowledge():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT topik, penjelasan FROM knowledge_bm")
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def save_knowledge(topik, penjelasan):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO knowledge_bm VALUES (?, ?)", (topik, penjelasan))
    conn.commit()
    conn.close()

init_db()

def safe_rerun():
    """Kompatibilitas untuk Streamlit versi lama dan baru."""
    if hasattr(st, "rerun"):
        safe_rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

def safe_toast(pesan):
    """Kompatibilitas untuk Streamlit versi lama yang belum punya st.toast."""
    if hasattr(st, "toast"):
        st.toast(pesan)
    else:
        st.success(pesan)

def tampilkan_jawaban_ai(teks):
    """Menampilkan jawaban AI tanpa error pada Streamlit versi lama."""
    if hasattr(st, "chat_message"):
        with st.chat_message("assistant"):
            st.write(teks)
    else:
        st.info(teks)


# ==============================================================================
# LOGIKA PARSING RUMUS KIMIA
# ==============================================================================

def normalize_formula(rumus):
    rumus = rumus.strip()
    rumus = rumus.replace(" ", "")
    rumus = rumus.replace("[", "(").replace("]", ")")
    rumus = rumus.replace("{", "(").replace("}", ")")
    rumus = rumus.replace("·", ".")
    return rumus

def parse_segment(segment):
    stack = [{}]
    i = 0

    while i < len(segment):
        karakter = segment[i]

        if karakter == "(":
            stack.append({})
            i += 1

        elif karakter == ")":
            if len(stack) == 1:
                raise ValueError("Tanda kurung tidak sesuai.")

            grup = stack.pop()
            i += 1

            angka = ""
            while i < len(segment) and segment[i].isdigit():
                angka += segment[i]
                i += 1

            pengali = int(angka) if angka else 1

            for simbol, jumlah in grup.items():
                stack[-1][simbol] = stack[-1].get(simbol, 0) + jumlah * pengali

        elif karakter.isupper():
            simbol = karakter
            i += 1

            if i < len(segment) and segment[i].islower():
                simbol += segment[i]
                i += 1

            angka = ""
            while i < len(segment) and segment[i].isdigit():
                angka += segment[i]
                i += 1

            jumlah = int(angka) if angka else 1
            stack[-1][simbol] = stack[-1].get(simbol, 0) + jumlah

        else:
            raise ValueError(f"Format rumus tidak valid pada karakter '{karakter}'.")

    if len(stack) != 1:
        raise ValueError("Tanda kurung tidak sesuai.")

    return stack[0]

def parse_formula(rumus):
    rumus = normalize_formula(rumus)

    if not rumus:
        raise ValueError("Rumus kimia tidak boleh kosong.")

    bagian = rumus.split(".")
    total_komposisi = {}

    for part in bagian:
        if not part:
            raise ValueError("Format hidrat tidak valid.")

        match = re.match(r"^(\d+)(.*)$", part)
        if match:
            koefisien = int(match.group(1))
            segment = match.group(2)
            if not segment:
                raise ValueError("Koefisien harus diikuti rumus kimia.")
        else:
            koefisien = 1
            segment = part

        komposisi = parse_segment(segment)

        for simbol, jumlah in komposisi.items():
            total_komposisi[simbol] = total_komposisi.get(simbol, 0) + jumlah * koefisien

    return total_komposisi

def hitung_bobot_molekul(rumus):
    try:
        komposisi = parse_formula(rumus)
    except ValueError as e:
        return None, None, str(e)

    detail = []
    total = 0

    for simbol, jumlah_atom in komposisi.items():
        if simbol not in unsur:
            return None, None, f"Unsur '{simbol}' tidak ditemukan dalam database unsur."

        nama_unsur = unsur[simbol]["nama"]
        nomor_atom = unsur[simbol]["nomor_atom"]
        massa_atom = unsur[simbol]["massa_atom"]
        subtotal = massa_atom * jumlah_atom
        total += subtotal

        detail.append({
            "Simbol Unsur": simbol,
            "Nama Unsur": nama_unsur,
            "Nomor Atom": nomor_atom,
            "Jumlah Atom": jumlah_atom,
            "Massa Atom (Ar)": massa_atom,
            "Subtotal Massa": round(subtotal, 4)
        })

    df = pd.DataFrame(detail)
    return round(total, 4), df, None

def generate_pembahasan(rumus, total, df):
    jumlah_unsur = len(df)
    jumlah_atom = int(df["Jumlah Atom"].sum())
    unsur_dominan = df.sort_values("Subtotal Massa", ascending=False).iloc[0]

    return (
        f"Berdasarkan hasil perhitungan, senyawa dengan rumus {rumus} memiliki bobot molekul sebesar "
        f"{total:.4f} g/mol. Senyawa ini tersusun atas {jumlah_unsur} jenis unsur dengan total {jumlah_atom} atom. "
        f"Kontribusi massa terbesar berasal dari unsur {unsur_dominan['Nama Unsur']} ({unsur_dominan['Simbol Unsur']}) "
        f"dengan subtotal massa {unsur_dominan['Subtotal Massa']:.4f} g/mol. Nilai bobot molekul ini dapat digunakan "
        f"untuk perhitungan mol, pembuatan larutan, stoikiometri reaksi, serta analisis kuantitatif di laboratorium kimia."
    )

def ai_chatbot_bm(pertanyaan):
    pertanyaan = pertanyaan.lower().strip()
    knowledge = get_knowledge()
    history = get_history()

    if pertanyaan in ["halo", "hai", "p", "test"]:
        return "Masukkan rumus kimia, nanti sistem hitung BM lengkap dengan detail unsur. Kimia memang suka bikin manusia menghitung ulang hal yang bisa dihitung mesin."

    if "rekap" in pertanyaan or "riwayat" in pertanyaan or "history" in pertanyaan:
        if history.empty:
            return "Belum ada riwayat perhitungan. Database masih kosong seperti niat belajar setelah libur panjang."
        return f"Total riwayat perhitungan yang tersimpan saat ini adalah {len(history)} data. BM tertinggi yang pernah dihitung adalah {history['total_bm'].max():.4f} g/mol."

    for kunci, isi in knowledge.items():
        if kunci in pertanyaan:
            return f"**{kunci.upper()}**: {isi}"

    return "Keyword belum ditemukan di memori. Tambahkan dulu di menu Manajemen Pengetahuan supaya sistem bisa menjawabnya."

# ==============================================================================
# CSS & ANIMASI BACKGROUND
# ==============================================================================

st.markdown("""
    <canvas id="chemCanvas" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1; pointer-events:none; opacity:0.12;"></canvas>
    <script>
    const canvas = document.getElementById('chemCanvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    const chars = '⚗️HCONFeNaCl0123456789';
    const alphabet = chars.split('');
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const drops = [];

    for (let x = 0; x < columns; x++) drops[x] = 1;

    function draw() {
        ctx.fillStyle = 'rgba(15, 23, 42, 0.06)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#22d3ee';
        ctx.font = fontSize + 'px monospace';

        for (let i = 0; i < drops.length; i++) {
            const text = alphabet[Math.floor(Math.random() * alphabet.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 40);
    </script>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #1e1e38, #0f172a 60%, #080c14);
        color: #f8fafc !important;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090d16 0%, #0f172a 100%) !important;
        border-right: 2px solid #1e293b;
    }

    .main-title {
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(45deg, #22d3ee, #a78bfa, #22d3ee);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 5px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .card-blue {
        background-color: rgba(14, 165, 233, 0.12);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid rgba(14, 165, 233, 0.35);
        border-left: 6px solid #0284c7;
        color: #e0f2fe;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }

    .card-purple {
        background-color: rgba(168, 85, 247, 0.12);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid rgba(168, 85, 247, 0.35);
        border-left: 6px solid #9333ea;
        color: #f3e8ff;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }

    .card-green {
        background-color: rgba(34, 197, 94, 0.12);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid rgba(34, 197, 94, 0.35);
        border-left: 6px solid #16a34a;
        color: #dcfce7;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }

    .card-blue:hover, .card-purple:hover, .card-green:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(34, 211, 238, 0.14);
    }

    .section-head {
        color: #38bdf8;
        font-weight: bold;
        border-bottom: 2px solid #1e293b;
        padding-bottom: 6px;
        margin-top: 18px;
    }

    label, p, span {
        color: #e2e8f0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR
# ==============================================================================

history_now = get_history()

with st.sidebar:
    st.markdown("<h2 style='color:#38bdf8; margin-bottom:0px; font-weight:900;'>⚗️ Molecule BM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-style:italic; color:#94a3b8; margin-top:0px;'>Kalkulator Bobot Molekul</p>", unsafe_allow_html=True)
    st.markdown("---")

    pilih_fitur = st.radio(
        "📌 Pilih Fitur:",
        [
            "Beranda",
            "Kalkulator BM / Mr",
            "Database Unsur",
            "Riwayat Perhitungan",
            "Inteligensia & Konsultasi AI"
        ]
    )

    st.markdown("---")
    st.markdown("<h4 style='color:#38bdf8;'>📊 Ringkasan Sistem</h4>", unsafe_allow_html=True)
    st.metric("Total Unsur Database", f"{len(unsur)} Unsur")
    st.metric("Riwayat Tersimpan", f"{len(history_now)} Data")

    if not history_now.empty:
        st.metric("BM Tertinggi", f"{history_now['total_bm'].max():.3f} g/mol")
    else:
        st.metric("BM Tertinggi", "0 g/mol")

# ==============================================================================
# HALAMAN BERANDA
# ==============================================================================

if pilih_fitur == "Beranda":
    st.markdown("<p class='main-title'>⚗️ Kalkulator Bobot Molekul / Mr</p>", unsafe_allow_html=True)
    st.caption("Dashboard komputasi kimia untuk menghitung BM, Mr, komposisi unsur, dan menyimpan riwayat perhitungan.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class='card-blue'>
                <h3 style='color:#38bdf8; margin-top:0px;'>🎯 Tujuan Aplikasi</h3>
                <p>Aplikasi ini dibuat untuk menghitung bobot molekul suatu senyawa berdasarkan rumus kimia. Sistem membaca simbol unsur, jumlah atom, tanda kurung, serta senyawa hidrat seperti CuSO4.5H2O.</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class='card-green'>
                <h3 style='color:#4ade80; margin-top:0px;'>📚 Manfaat Aplikasi</h3>
                <p>Aplikasi membantu proses perhitungan kimia analitik, pembuatan larutan, stoikiometri, dan validasi komposisi unsur tanpa menghitung manual berulang-ulang seperti ritual penderitaan akademik.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 class='section-head'>🧪 Contoh Rumus yang Didukung</h3>", unsafe_allow_html=True)
    contoh = pd.DataFrame({
        "Jenis Senyawa": ["Sederhana", "Dengan angka indeks", "Dengan tanda kurung", "Garam kompleks", "Hidrat"],
        "Contoh Rumus": ["H2O", "C6H12O6", "Ca(OH)2", "Al2(SO4)3", "Fe(NH4)2(SO4)2.6H2O"]
    })
    st.dataframe(contoh, use_container_width=True)

# ==============================================================================
# HALAMAN KALKULATOR
# ==============================================================================

elif pilih_fitur == "Kalkulator BM / Mr":
    st.markdown("<h1 style='color:#38bdf8;'>⚗️ Kalkulator Bobot Molekul</h1>", unsafe_allow_html=True)
    st.caption("Masukkan rumus kimia. Sistem akan memecah unsur, menghitung subtotal massa, lalu menjumlahkan BM.")
    st.markdown("---")

    col_input, col_output = st.columns([1.2, 1.3])

    with col_input:
        if "rumus_input" not in st.session_state:
            st.session_state["rumus_input"] = "Fe(NH4)2(SO4)2.6H2O"

        rumus = st.text_input(
            "🧪 Masukkan Rumus Kimia:",
            key="rumus_input",
            placeholder="Contoh: H2O, NaCl, Ca(OH)2, Al2(SO4)3, CuSO4.5H2O"
        )

        simpan = st.checkbox("Simpan hasil ke database riway
