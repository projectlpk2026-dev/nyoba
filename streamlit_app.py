import re

# =========================
# DATABASE UNSUR
# =========================

unsur = {
    "H": {"nama": "Hidrogen", "nomor_atom": 1, "massa_atom": 1.00794},
    "He": {"nama": "Helium", "nomor_atom": 2, "massa_atom": 4.002602},
    "Li": {"nama": "Litium", "nomor_atom": 3, "massa_atom": 6.941},
    "Be": {"nama": "Berilium", "nomor_atom": 4, "massa_atom": 9.012182},
    "B": {"nama": "Boron", "nomor_atom": 5, "massa_atom": 10.811},
    "C": {"nama": "Karbon", "nomor_atom": 6, "massa_atom": 12.0107},
    "N": {"nama": "Nitrogen", "nomor_atom": 7, "massa_atom": 14.0067},
    "O": {"nama": "Oksigen", "nomor_atom": 8, "massa_atom": 15.9994},
    "Na": {"nama": "Natrium", "nomor_atom": 11, "massa_atom": 22.98976928},
    "Mg": {"nama": "Magnesium", "nomor_atom": 12, "massa_atom": 24.3050},
    "Al": {"nama": "Aluminium", "nomor_atom": 13, "massa_atom": 26.9815386},
    "Si": {"nama": "Silikon", "nomor_atom": 14, "massa_atom": 28.0855},
    "P": {"nama": "Fosfor", "nomor_atom": 15, "massa_atom": 30.973762},
    "S": {"nama": "Sulfur", "nomor_atom": 16, "massa_atom": 32.065},
    "Cl": {"nama": "Klorin", "nomor_atom": 17, "massa_atom": 35.453},
    "K": {"nama": "Kalium", "nomor_atom": 19, "massa_atom": 39.0983},
    "Ca": {"nama": "Kalsium", "nomor_atom": 20, "massa_atom": 40.078},
    "Fe": {"nama": "Besi", "nomor_atom": 26, "massa_atom": 55.845},
    "Cu": {"nama": "Tembaga", "nomor_atom": 29, "massa_atom": 63.546},
    "Zn": {"nama": "Seng", "nomor_atom": 30, "massa_atom": 65.38},
    "Ag": {"nama": "Perak", "nomor_atom": 47, "massa_atom": 107.8682},
    "I": {"nama": "Iodin", "nomor_atom": 53, "massa_atom": 126.90447},
    "Ba": {"nama": "Barium", "nomor_atom": 56, "massa_atom": 137.327},
    "Au": {"nama": "Emas", "nomor_atom": 79, "massa_atom": 196.966569},
    "Hg": {"nama": "Merkuri", "nomor_atom": 80, "massa_atom": 200.59}
}

# =========================
# FUNGSI PARSING RUMUS
# =========================

def parse_rumus(rumus):
    stack = [{}]
    i = 0

    while i < len(rumus):
        char = rumus[i]

        if char == "(":
            stack.append({})
            i += 1

        elif char == ")":
            i += 1
            angka = ""

            while i < len(rumus) and rumus[i].isdigit():
                angka += rumus[i]
                i += 1

            pengali = int(angka) if angka else 1
            grup = stack.pop()

            for simbol, jumlah in grup.items():
                stack[-1][simbol] = stack[-1].get(simbol, 0) + jumlah * pengali

        elif char.isupper():
            simbol = char
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
            raise ValueError("Format rumus kimia tidak valid!")

    if len(stack) != 1:
        raise ValueError("Tanda kurung tidak lengkap!")

    return stack[0]


# =========================
# FUNGSI HITUNG BOBOT MOLEKUL
# =========================

def hitung_bobot_molekul(rumus):
    if not rumus or rumus.strip() == "":
        return None, None, "Rumus kimia tidak boleh kosong!"

    rumus = rumus.strip()

    try:
        komposisi = parse_rumus(rumus)
    except ValueError as e:
        return None, None, str(e)

    total = 0
    detail = []

    for simbol, jumlah in komposisi.items():
        if simbol not in unsur:
            return None, None, f"Unsur {simbol} tidak ditemukan dalam database!"

        massa_atom = unsur[simbol]["massa_atom"]
        subtotal = massa_atom * jumlah
        total += subtotal

        detail.append({
            "Unsur": simbol,
            "Nama": unsur[simbol]["nama"],
            "Jumlah Atom": jumlah,
            "Massa Atom": massa_atom,
            "Subtotal": round(subtotal, 3)
        })

    return round(total, 3), detail, None


# =========================
# CONTOH PENGGUNAAN
# =========================

rumus = input("Masukkan rumus kimia: ")

total, detail, error = hitung_bobot_molekul(rumus)

if error:
    print("Error:", error)
else:
    print("\nDetail Perhitungan:")
    for data in detail:
        print(data)

    print(f"\nBobot Molekul (Mr) {rumus} = {total}")
