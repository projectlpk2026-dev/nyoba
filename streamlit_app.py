import re
import streamlit as st
import pandas as pd
from datetime import datetime

unsur = {
    "H": {"nama": "Hidrogen", "nomor_atom": 1, "massa_atom": 1.008},
    "C": {"nama": "Karbon", "nomor_atom": 6, "massa_atom": 12.011},
    "N": {"nama": "Nitrogen", "nomor_atom": 7, "massa_atom": 14.007},
    "O": {"nama": "Oksigen", "nomor_atom": 8, "massa_atom": 15.999},
    "Na": {"nama": "Natrium", "nomor_atom": 11, "massa_atom": 22.990},
    "Mg": {"nama": "Magnesium", "nomor_atom": 12, "massa_atom": 24.305},
    "Al": {"nama": "Aluminium", "nomor_atom": 13, "massa_atom": 26.982},
    "S": {"nama": "Sulfur", "nomor_atom": 16, "massa_atom": 32.06},
    "Cl": {"nama": "Klorin", "nomor_atom": 17, "massa_atom": 35.45},
    "K": {"nama": "Kalium", "nomor_atom": 19, "massa_atom": 39.098},
    "Ca": {"nama": "Kalsium", "nomor_atom": 20, "massa_atom": 40.078},
    "Mn": {"nama": "Mangan", "nomor_atom": 25, "massa_atom": 54.938},
    "Fe": {"nama": "Besi", "nomor_atom": 26, "massa_atom": 55.845},
}

contoh_rumus = {
    "Air": "H2O",
    "Karbon dioksida": "CO2",
    "Garam dapur": "NaCl",
    "Glukosa": "C6H12O6",
    "Kalsium hidroksida": "Ca(OH)2",
    "Aluminium sulfat": "Al2(SO4)3",
    "FAS": "Fe(NH4)2(SO4)2(H2O)6",
    "Asam sulfat": "H2SO4",
    "Kalium permanganat": "KMnO4",
    "Kalsium karbonat": "CaCO3",
}

st.set_page_config(
    page_title="Kalkulator BM/Mr Kimia",
    page_icon="⚗️",
    layout="wide"
)

st.markdown("""
<style>
.hero {
    padding: 28px;
    border-radius: 24px;
    background: linear-gradient(135deg, #152e67, #2563eb, #38bdf8);
    color: white;
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 40px;
}
.card {
    padding: 20px;
    border-radius: 18px;
    background: white;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}
.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #152e67;
}
.chat-user {
    background: #dbeafe;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}
.chat-bot {
    background: #f1f5f9;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


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
            raise ValueError("Format rumus kimia tidak valid.")

    if len(stack) != 1:
        raise ValueError("Tanda kurung tidak sesuai.")

    return stack[0]


def hitung_bm_mr(rumus):
    rumus = rumus.strip().replace(" ", "")

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
        item["Persentase Massa (%)"] = round(
            item["Subtotal Massa"] / total * 100, 2
        )

    return round(total, 3), detail, None


def buat_pembahasan(rumus, total, detail):
    unsur_terlibat = ", ".join(
        [f"{d['Nama Unsur']} ({d['Simbol Unsur']})" for d in detail]
    )

    rincian = "; ".join(
        [
            f"{d['Simbol Unsur']} sebanyak {d['Jumlah Atom']} atom "
            f"dengan subtotal {d['Subtotal Massa']} g/mol"
            for d in detail
        ]
    )

    dominan = max(detail, key=lambda x: x["Subtotal Massa"])

    return (
        f"Berdasarkan hasil perhitungan, senyawa {rumus} tersusun atas unsur "
        f"{unsur_terlibat}. Perhitungan BM/Mr dilakukan dengan mengalikan "
        f"massa atom relatif setiap unsur dengan jumlah atomnya, kemudian "
        f"seluruh subtotal massa dijumlahkan. Rinciannya adalah {rincian}. "
        f"Dari hasil tersebut diperoleh BM/Mr {rumus} sebesar {total} g/mol. "
        f"Unsur dengan kontribusi massa terbesar adalah {dominan['Nama Unsur']} "
        f"({dominan['Simbol Unsur']}) sebesar {dominan['Persentase Massa (%)']}%."
    )


def chatbot_jawab(pertanyaan):
    teks = pertanyaan.lower()

    if pertanyaan.strip() == "":
        return "Tulis pertanyaan dulu. Chatbot ini belum bisa membaca pikiran."

    if "apa itu bm" in teks or "apa itu mr" in teks:
        return (
            "BM atau Mr adalah jumlah massa atom relatif dari seluruh unsur "
            "penyusun suatu senyawa."
        )

    if "cara" in teks and "hitung" in teks:
        return (
            "Cara menghitung BM/Mr adalah: pisahkan unsur, tentukan jumlah atom, "
            "kalikan jumlah atom dengan massa atom, lalu jumlahkan semuanya."
        )

    if "fas" in teks:
        total, detail, error = hitung_bm_mr("Fe(NH4)2(SO4)2(H2O)6")
        return f"BM/Mr FAS Fe(NH4)2(SO4)2·6H2O adalah {total} g/mol."

    pola = re.search(r"([A-Z][A-Za-z0-9()]+)", pertanyaan)
    if pola:
        rumus = pola.group(1)
        total, detail, error = hitung_bm_mr(rumus)

        if error:
            return error

        return f"BM/Mr {rumus} = {total} g/mol."

    return (
        "Saya bisa membantu menghitung BM/Mr. Contoh pertanyaan: "
        "'hitung Mr H2SO4' atau 'berapa BM FAS?'."
    )


if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "chat" not in st.session_state:
    st.session_state.chat = []


st.markdown("""
<div class="hero">
    <h1>⚗️ Kalkulator BM / Mr Kimia</h1>
    <p>Aplikasi interaktif untuk menghitung BM/Mr, persentase massa unsur, pembahasan otomatis, riwayat pencarian, dan chatbot mini.</p>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("Menu")
    menu = st.radio(
        "Pilih Fitur",
        [
            "Kalkulator BM/Mr",
            "Riwayat Pencarian",
            "Chatbot Mini",
            "Database Unsur"
        ]
    )

    st.subheader("Contoh Rumus")
    pilihan = st.selectbox("Pilih senyawa", list(contoh_rumus.keys()))
    st.code(contoh_rumus[pilihan])


if menu == "Kalkulator BM/Mr":
    st.subheader("Input Rumus Kimia")

    col1, col2 = st.columns([2, 1])

    with col1:
        rumus = st.text_input(
            "Masukkan rumus kimia",
            value=contoh_rumus[pilihan],
            placeholder="Contoh: H2O, CO2, Ca(OH)2"
        )

    with col2:
        st.markdown("### Rumus Dasar")
        st.info("BM/Mr = Σ massa atom × jumlah atom")

    if st.button("Hitung BM/Mr", use_container_width=True):
        total, detail, error = hitung_bm_mr(rumus)

        if error:
            st.error(error)
        else:
            rumus_bersih = rumus.strip().replace(" ", "")
            df = pd.DataFrame(detail)

            st.session_state.riwayat.insert(0, {
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Rumus": rumus_bersih,
                "BM/Mr": total
            })

            st.success("Perhitungan berhasil.")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(
                    f"<div class='card'><p>Rumus Kimia</p><div class='metric-value'>{rumus_bersih}</div></div>",
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"<div class='card'><p>Total BM/Mr</p><div class='metric-value'>{total}</div></div>",
                    unsafe_allow_html=True
                )

            with c3:
                st.markdown(
                    f"<div class='card'><p>Jumlah Unsur</p><div class='metric-value'>{len(detail)}</div></div>",
                    unsafe_allow_html=True
                )

            st.subheader("Tabel Hasil Perhitungan")
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.subheader("Grafik Persentase Massa Unsur")
            st.bar_chart(df.set_index("Simbol Unsur")[["Persentase Massa (%)"]])

            st.subheader("Pembahasan Otomatis")
            st.info(buat_pembahasan(rumus_bersih, total, detail))

            st.download_button(
                "Download Hasil CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"hasil_bm_mr_{rumus_bersih}.csv",
                mime="text/csv",
                use_container_width=True
            )


elif menu == "Riwayat Pencarian":
    st.subheader("Riwayat Pencarian")

    if len(st.session_state.riwayat) == 0:
        st.warning("Belum ada riwayat pencarian.")
    else:
        df_riwayat = pd.DataFrame(st.session_state.riwayat)
        st.dataframe(df_riwayat, use_container_width=True, hide_index=True)

        if st.button("Hapus Riwayat"):
            st.session_state.riwayat = []
            st.rerun()


elif menu == "Chatbot Mini":
    st.subheader("Chatbot Mini BM/Mr")

    pertanyaan = st.text_input("Tulis pertanyaan")

    if st.button("Kirim"):
        jawaban = chatbot_jawab(pertanyaan)
        st.session_state.chat.append({
            "user": pertanyaan,
            "bot": jawaban
        })

    for chat in reversed(st.session_state.chat):
        st.markdown(
            f"<div class='chat-user'><b>Anda:</b> {chat['user']}</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<div class='chat-bot'><b>Bot:</b> {chat['bot']}</div>",
            unsafe_allow_html=True
        )


elif menu == "Database Unsur":
    st.subheader("Database Unsur")

    keyword = st.text_input("Cari unsur")

    df_unsur = pd.DataFrame([
        {
            "Simbol": simbol,
            "Nama Unsur": data["nama"],
            "Nomor Atom": data["nomor_atom"],
            "Massa Atom": data["massa_atom"]
        }
        for simbol, data in unsur.items()
    ])

    if keyword:
        keyword = keyword.lower()
        df_unsur = df_unsur[
            df_unsur["Simbol"].str.lower().str.contains(keyword)
            | df_unsur["Nama Unsur"].str.lower().str.contains(keyword)
        ]

    st.dataframe(df_unsur, use_container_width=True, hide_index=True)

st.caption("Aplikasi Kalkulator BM/Mr Kimia berbasis Streamlit.")
