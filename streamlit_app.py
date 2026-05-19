import streamlit as st
import re
import pandas as pd

# =========================
# DATABASE MASSA ATOM
# =========================
unsur = {
    "H": 1.008,
    "He": 4.0026,
    "Li": 6.94,
    "Be": 9.0122,
    "B": 10.81,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "F": 18.998,
    "Ne": 20.180,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.085,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "Ar": 39.948,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845,
    "Cu": 63.546,
    "Zn": 65.38,
    "Ag": 107.868,
    "I": 126.904,
    "Ba": 137.327,
    "Au": 196.967,
    "Hg": 200.592,
    "Pb": 207.2
}

# =========================
# FUNGSI HITUNG Mr
# =========================
def hitung_mr(rumus):
    pola = r'([A-Z][a-z]?)(\d*)'
    hasil = re.findall(pola, rumus)

    if not hasil:
        return None, "Format rumus kimia tidak valid."

    data = []
    total_mr = 0

    for simbol, jumlah in hasil:
        if simbol not in unsur:
            return None, f"Unsur '{simbol}' tidak ditemukan dalam database."

        jumlah_atom = int(jumlah) if jumlah else 1
        massa_atom = unsur[simbol]
        subtotal = massa_atom * jumlah_atom
        total_mr += subtotal

        data.append({
            "Simbol Unsur": simbol,
            "Jumlah Atom": jumlah_atom,
            "Massa Atom": massa_atom,
            "Subtotal Massa": subtotal
        })

    return data, total_mr


# =========================
# TAMPILAN WEB
# =========================
st.set_page_config(
    page_title="Kalkulator Bobot Molekul",
    page_icon="⚗️",
    layout="centered"
)

st.title("⚗️ Kalkulator Bobot Molekul")
st.write("Aplikasi ini digunakan untuk menghitung bobot molekul atau Mr suatu senyawa kimia.")

rumus = st.text_input(
    "Masukkan rumus kimia senyawa:",
    placeholder="Contoh: H2O, CO2, NaCl, C6H12O6"
)

if st.button("Hitung Mr"):
    if rumus.strip() == "":
        st.warning("Masukkan rumus kimia terlebih dahulu.")
    else:
        data, hasil = hitung_mr(rumus.strip())

        if data is None:
            st.error(hasil)
        else:
            df = pd.DataFrame(data)

            st.subheader("Hasil Perhitungan")
            st.dataframe(df, use_container_width=True)

            st.success(f"Bobot molekul (Mr) dari {rumus} adalah {hasil:.3f} g/mol")

            st.subheader("Rincian Perhitungan")
            for item in data:
                st.write(
                    f"{item['Simbol Unsur']} : "
                    f"{item['Massa Atom']} × {item['Jumlah Atom']} = "
                    f"{item['Subtotal Massa']:.3f}"
                )

            st.write(f"**Total Mr = {hasil:.3f} g/mol**")
