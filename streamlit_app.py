import streamlit as st
import re
import pandas as pd

# Database massa atom relatif
massa_atom = {
    "H": 1.008,
    "C": 12.011,
    "N": 14.007,
    "O": 15.999,
    "Na": 22.990,
    "Mg": 24.305,
    "Al": 26.982,
    "Si": 28.085,
    "P": 30.974,
    "S": 32.06,
    "Cl": 35.45,
    "K": 39.098,
    "Ca": 40.078,
    "Fe": 55.845,
    "Cu": 63.546,
    "Zn": 65.38,
    "Ag": 107.868,
    "I": 126.904,
    "Ba": 137.327,
    "Pb": 207.2
}

def hitung_mr(rumus):
    pola = r"([A-Z][a-z]?)(\d*)"
    hasil = re.findall(pola, rumus)

    if not hasil:
        return None, "Format rumus kimia tidak valid."

    data = []
    total_mr = 0

    for unsur, jumlah in hasil:
        jumlah_atom = int(jumlah) if jumlah else 1

        if unsur not in massa_atom:
            return None, f"Unsur '{unsur}' tidak ditemukan dalam database massa atom."

        massa = massa_atom[unsur]
        subtotal = massa * jumlah_atom
        total_mr += subtotal

        data.append({
            "Simbol Unsur": unsur,
            "Jumlah Atom": jumlah_atom,
            "Massa Atom": massa,
            "Subtotal Massa": subtotal
        })

    return data, total_mr


st.title("Kalkulator Bobot Molekul (Mr)")
st.write("Program ini digunakan untuk menghitung bobot molekul relatif suatu senyawa kimia berdasarkan rumus kimianya.")

rumus = st.text_input("Masukkan rumus kimia senyawa", placeholder="Contoh: H2O, CO2, NaCl, C6H12O6")

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

            st.success(f"Total bobot molekul (Mr) {rumus} = {hasil:.3f}")

st.subheader("Database Massa Atom")
st.write("Berikut beberapa unsur yang tersedia dalam database:")
st.dataframe(
    pd.DataFrame(
        list(massa_atom.items()),
        columns=["Simbol Unsur", "Massa Atom"]
    ),
    use_container_width=True
)
