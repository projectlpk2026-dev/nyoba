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
    "F": {"nama": "Fluorin", "nomor_atom": 9, "massa_atom": 18.9984032},
    "Ne": {"nama": "Neon", "nomor_atom": 10, "massa_atom": 20.1797},

    "Na": {"nama": "Natrium", "nomor_atom": 11, "massa_atom": 22.98976928},
    "Mg": {"nama": "Magnesium", "nomor_atom": 12, "massa_atom": 24.3050},
    "Al": {"nama": "Aluminium", "nomor_atom": 13, "massa_atom": 26.9815386},
    "Si": {"nama": "Silikon", "nomor_atom": 14, "massa_atom": 28.0855},
    "P": {"nama": "Fosfor", "nomor_atom": 15, "massa_atom": 30.973762},
    "S": {"nama": "Sulfur", "nomor_atom": 16, "massa_atom": 32.065},
    "Cl": {"nama": "Klorin", "nomor_atom": 17, "massa_atom": 35.453},
    "Ar": {"nama": "Argon", "nomor_atom": 18, "massa_atom": 39.948},
    "K": {"nama": "Kalium", "nomor_atom": 19, "massa_atom": 39.0983},
    "Ca": {"nama": "Kalsium", "nomor_atom": 20, "massa_atom": 40.078},

    "Sc": {"nama": "Skandium", "nomor_atom": 21, "massa_atom": 44.9559126},
    "Ti": {"nama": "Titanium", "nomor_atom": 22, "massa_atom": 47.867},
    "V": {"nama": "Vanadium", "nomor_atom": 23, "massa_atom": 50.9415},
    "Cr": {"nama": "Kromium", "nomor_atom": 24, "massa_atom": 51.9961},
    "Mn": {"nama": "Mangan", "nomor_atom": 25, "massa_atom": 54.938045},
    "Fe": {"nama": "Besi", "nomor_atom": 26, "massa_atom": 55.845},
    "Co": {"nama": "Kobalt", "nomor_atom": 27, "massa_atom": 58.933195},
    "Ni": {"nama": "Nikel", "nomor_atom": 28, "massa_atom": 58.6934},
    "Cu": {"nama": "Tembaga", "nomor_atom": 29, "massa_atom": 63.546},
    "Zn": {"nama": "Seng", "nomor_atom": 30, "massa_atom": 65.38},

    "Ga": {"nama": "Galium", "nomor_atom": 31, "massa_atom": 69.723},
    "Ge": {"nama": "Germanium", "nomor_atom": 32, "massa_atom": 72.64},
    "As": {"nama": "Arsen", "nomor_atom": 33, "massa_atom": 74.921},
    "Se": {"nama": "Selenium", "nomor_atom": 34, "massa_atom": 78.96},
    "Br": {"nama": "Bromin", "nomor_atom": 35, "massa_atom": 79.904},
    "Kr": {"nama": "Kripton", "nomor_atom": 36, "massa_atom": 83.798},
    "Rb": {"nama": "Rubidium", "nomor_atom": 37, "massa_atom": 85.4678},
    "Sr": {"nama": "Stronsium", "nomor_atom": 38, "massa_atom": 87.62},
    "Y": {"nama": "Itrium", "nomor_atom": 39, "massa_atom": 88.90585},
    "Zr": {"nama": "Zirkonium", "nomor_atom": 40, "massa_atom": 91.224},

    "Nb": {"nama": "Niobium", "nomor_atom": 41, "massa_atom": 92.90638},
    "Mo": {"nama": "Molibdenum", "nomor_atom": 42, "massa_atom": 95.96},
    "Tc": {"nama": "Teknesium", "nomor_atom": 43, "massa_atom": 98},
    "Ru": {"nama": "Rutenium", "nomor_atom": 44, "massa_atom": 101.07},
    "Rh": {"nama": "Rodium", "nomor_atom": 45, "massa_atom": 102.90550},
    "Pd": {"nama": "Paladium", "nomor_atom": 46, "massa_atom": 106.42},
    "Ag": {"nama": "Perak", "nomor_atom": 47, "massa_atom": 107.8682},
    "Cd": {"nama": "Kadmium", "nomor_atom": 48, "massa_atom": 112.41},
    "In": {"nama": "Indium", "nomor_atom": 49, "massa_atom": 114.818},
    "Sn": {"nama": "Timah", "nomor_atom": 50, "massa_atom": 118.710},

    "Sb": {"nama": "Antimon", "nomor_atom": 51, "massa_atom": 121.760},
    "Te": {"nama": "Telurium", "nomor_atom": 52, "massa_atom": 127.60},
    "I": {"nama": "Iodin", "nomor_atom": 53, "massa_atom": 126.90447},
    "Xe": {"nama": "Xenon", "nomor_atom": 54, "massa_atom": 131.293},
    "Cs": {"nama": "Sesium", "nomor_atom": 55, "massa_atom": 132.9054519},
    "Ba": {"nama": "Barium", "nomor_atom": 56, "massa_atom": 137.327},
    "La": {"nama": "Lantanum", "nomor_atom": 57, "massa_atom": 138.90547},
    "Ce": {"nama": "Cerium", "nomor_atom": 58, "massa_atom": 140.116},
    "Pr": {"nama": "Praseodimium", "nomor_atom": 59, "massa_atom": 140.90765},
    "Nd": {"nama": "Neodimium", "nomor_atom": 60, "massa_atom": 144.242},

    "Pm": {"nama": "Prometium", "nomor_atom": 61, "massa_atom": 145},
    "Sm": {"nama": "Samarium", "nomor_atom": 62, "massa_atom": 150.36},
    "Eu": {"nama": "Europium", "nomor_atom": 63, "massa_atom": 151.964},
    "Gd": {"nama": "Gadolinium", "nomor_atom": 64, "massa_atom": 157.25},
    "Tb": {"nama": "Terbium", "nomor_atom": 65, "massa_atom": 158.92535},
    "Dy": {"nama": "Disprosium", "nomor_atom": 66, "massa_atom": 162.500},
    "Ho": {"nama": "Holmium", "nomor_atom": 67, "massa_atom": 164.93032},
    "Er": {"nama": "Erbium", "nomor_atom": 68, "massa_atom": 167.259},
    "Tm": {"nama": "Tulium", "nomor_atom": 69, "massa_atom": 168.93421},
    "Yb": {"nama": "Iterbium", "nomor_atom": 70, "massa_atom": 173.054},

    "Lu": {"nama": "Lutesium", "nomor_atom": 71, "massa_atom": 174.9668},
    "Hf": {"nama": "Hafnium", "nomor_atom": 72, "massa_atom": 178.49},
    "Ta": {"nama": "Tantalum", "nomor_atom": 73, "massa_atom": 180.94788},
    "W": {"nama": "Tungsten", "nomor_atom": 74, "massa_atom": 183.84},
    "Re": {"nama": "Renium", "nomor_atom": 75, "massa_atom": 186.207},
    "Os": {"nama": "Osmium", "nomor_atom": 76, "massa_atom": 190.23},
    "Ir": {"nama": "Iridium", "nomor_atom": 77, "massa_atom": 192.217},
    "Pt": {"nama": "Platina", "nomor_atom": 78, "massa_atom": 195.084},
    "Au": {"nama": "Emas", "nomor_atom": 79, "massa_atom": 196.966569},
    "Hg": {"nama": "Merkuri", "nomor_atom": 80, "massa_atom": 200.59}
}

# =========================
# FUNGSI HITUNG BM
# =========================

def hitung_bobot_molekul(rumus):
    pola = r'([A-Z][a-z]?)(\d*)'
    hasil = re.findall(pola, rumus)
    total = 0
    detail = []
    for simbol, jumlah in hasil:
        if simbol not in unsur:
            return None, None, f"Unsur {simbol} tidak ditemukan!"
        jumlah = int(jumlah) if jumlah != "" else 1
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
    return total, detail, None
