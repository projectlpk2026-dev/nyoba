# =====================================================
# APLIKASI LABORATORIUM KIMIA
# =====================================================

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

def header():

    print("=" * 55)
    print("      APLIKASI LABORATORIUM KIMIA")
    print("=" * 55)

# =====================================================
# MENU CEK ALAT
# =====================================================

def cek_alat():

    print("\n=== CEK STOK ALAT LABORATORIUM ===")

    print("Ketik 'daftar' untuk melihat semua alat")
    print("Ketik 'keluar' untuk kembali ke menu")

    while True:

        cari = input("\nCari alat apa? ").strip().title()

        # keluar
        if cari.lower() == "keluar":
            break

        # tampil semua alat
        elif cari.lower() == "daftar":

            print("\nAlat yang tersedia:")

            for alat in alat_lab:
                print("-", alat)

        # pencarian alat
        elif cari in alat_lab:

            print(f"\nAlat '{cari}' TERSEDIA di laboratorium")

        else:

            print(f"\nAlat '{cari}' TIDAK DITEMUKAN")

# =====================================================
# MENU MOLARITAS
# =====================================================

def molaritas():

    print("\n=== KALKULATOR MOLARITAS ===")

    mol = float(input("Masukkan jumlah mol (mol): "))
    volume = float(input("Masukkan volume larutan (L): "))

    hasil = mol / volume

    print("\nMolaritas =", round(hasil, 3), "M")

# =====================================================
# MENU PENGENCERAN
# =====================================================

def pengenceran():

    print("\n=== KALKULATOR PENGENCERAN ===")

    M1 = float(input("Masukkan M1 (M): "))
    V1 = float(input("Masukkan V1 (mL): "))
    M2 = float(input("Masukkan M2 (M): "))

    V2 = (M1 * V1) / M2

    print("\nV2 =", round(V2, 2), "mL")

# =====================================================
# MENU KADAR
# =====================================================

def menu_kadar():
    while True:

        print("\n=== KALKULATOR KADAR ===")
        print("1. Kadar Asam Asetat")
        print("2. NaOH dan Na2CO3 (Warder)")
        print("3. Kadar Besi(Fe)")
        print("4. Kadar Klorida(Cl)Iodometri")
        print("5. Kadar Klorida(Cl)Argentometri")
        print("6. Kesadahan Air")
        print("7. Kembali")
        
        pilih = input("Pilih menu : ")
        if pilih == "1":
            kadar_asam_asetat()

        elif pilih == "2":
            kadar_warder()

        elif pilih == "3":
            kadar_besi()

        elif pilih == "4":
            kadar_klorida_iodometri()

        elif pilih == "5":
            kadar_klorida_argentometri()
            
        elif pilih == "6":
            kadar_kesadahan()

        elif pilih == "7":
            break

        else:
            print("Pilihan tidak valid")

def kadar_asam_asetat():
    print("\n=== KADAR ASAM ASETAT ===")
    V = float(input("Masukkan volume titrasi/V(mL):"))
    N = float(input("Masukkan normalitas/N(mgrek/mL):"))
    FP = float(input("Faktor pengenceran:"))
    V_sampel = float(input("Masukkan volume sampel (mL):"))
    hasil = ((V * N * 60) * (10**-3) * FP * 100) / V_sampel

    print("\nKadar CH3COOH =", round(hasil, 2), "%")

def kadar_warder():

    print("\n=== KADAR METODE WARDER ===")
    a = float(input("Masukkan volume titrasi 1/a(mL):"))
    b = float(input("Masukkan volume titrasi 2/b(mL):"))
    N = float(input("Masukkan normalitas/N(mgrek/mL):"))
    V_sampel = float(input("Masukkan volume sampel (mL):"))
    BE_NaOH = 40
    BE_Na2CO3 = 53
    
    Na2CO3 = ((2 * (b-a)* N * BE_Na2CO3) * (10**-3) * 100) / V_sampel
    NaOH = ((2*a - b)* N * BE_NaOH) * (10**-3) * 100 / V_sampel

    print("\nKadar NaOH =", round(Na2CO3, 2), "%")
    print("\nKadar Na2CO3 =", round(NaOH, 2), "%")

def kadar_besi():
    print("\n=== KADAR BESI (Fe) ===")
    V = float(input("Masukkan volume titrasi/V(mL):"))
    N = float(input("Masukkan normalitas/N(mgrek/mL):"))
    V_sampel = float(input("Masukkan volume sampel (mL):"))
    hasil = ((V * N * 56) * (10**-3) * 100) / V_sampel

    print("\nKadar Fe =", round(hasil, 2), "%")
    
def kadar_klorida_iodometri():
    print("\n=== KADAR KLORIDA (IODOMETRI)(Cl) ===")
    V = float(input("Masukkan volume titrasi/V(mL):"))
    N = float(input("Masukkan normalitas/N(mgrek/mL):"))
    V_sampel = float(input("Masukkan volume sampel (mL):"))
    hasil = ((V * N * 17.75) * (10**-3) * 100/5 * 100) / V_sampel

    print("\nKadar Cl =", round(hasil, 2), "%")

def kadar_klorida_argentometri():
    print("\n=== KADAR KLORIDA (ARGENTOMETRI)(Cl) ===")
    V = float(input("Masukkan volume titrasi/V(mL):"))
    N = float(input("Masukkan normalitas/N(mgrek/mL):"))
    V_sampel = float(input("Masukkan volume sampel (mL):"))
    hasil = ((V * N * 35.5) * (10**-3) * 100) / V_sampel

    print("\nKadar Cl =", round(hasil, 2), "%")


def kadar_kesadahan():
    print("\n=== KADAR KESADAHAN AIR ===")
    V = float(input("Masukkan volume titrasi/V(mL):"))
    M = float(input("Masukkan molaritas/M(mmol/mL):"))
    V_sampel = float(input("Masukkan volume sampel (L):"))
    hasil = ((V * M * 100)) /V_sampel

    print("\nKadar CaCO3 =", round(hasil, 2), "%")
    

# =====================================================
# MENU pH
# =====================================================

def ph():

    print("\n=== KALKULATOR pH ===")

    h = float(input("Masukkan konsentrasi H+ (mol/L): "))

    hasil = -math.log10(h)

    print("\npH =", round(hasil, 2))

# =====================================================
# PROGRAM UTAMA
# =====================================================

while True:

    header()

    print("""
MENU UTAMA

1. Cek Stok Alat Laboratorium
2. Kalkulator Molaritas
3. Kalkulator Pengenceran
4. Kalkulator Kadar
5. Kalkulator pH
6. Keluar
""")

    pilihan = input("Masukkan pilihan : ")

    # =================================================

    if pilihan == "1":
        cek_alat()

    elif pilihan == "2":
        molaritas()

    elif pilihan == "3":
        pengenceran()

    elif pilihan == "4":
        menu_kadar()

    elif pilihan == "5":
        ph()

    elif pilihan == "6":

        print("\nProgram selesai")
        break

    else:

        print("\nPilihan tidak valid")

    input("\nTekan ENTER untuk kembali ke menu...")
