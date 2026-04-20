"""
Tugas 1 - Step 3a: Simulasi Brute Force
Kasus: Perencanaan Nutrisi Pasca-Operasi
Mata Kuliah: Algoritma Evolusi dan Kecerdasan Kelompok (CIF62342)

Metode Brute Force mengevaluasi SEMUA kemungkinan kombinasi
(x1, x2, x3) secara ekshaustif untuk menemukan solusi optimal global.
"""

import time

# =====================================================================
# DATA SUPLEMEN
# =====================================================================

# Kalori tiap suplemen (kkal/sajian): A=120, B=150, C=80
KALORI  = [120, 150,  80]

# Protein tiap suplemen (g/sajian): A=20, B=5, C=8
PROTEIN = [ 20,   5,   8]

# Natrium tiap suplemen (mg/sajian): A=80, B=30, C=120
NATRIUM = [ 80,  30, 120]

# Biaya tiap suplemen (Rp/sajian): A=25000, B=15000, C=20000
BIAYA   = [25000, 15000, 20000]

# =====================================================================
# PARAMETER KENDALA
# =====================================================================

TOTAL_SAJIAN  = 12      # total sajian per hari harus tepat 12
MIN_KALORI    = 1800    # kebutuhan kalori minimal (kkal)
MIN_PROTEIN   = 70      # kebutuhan protein minimal (g)
MAX_NATRIUM   = 2000    # batas natrium maksimal (mg)

# =====================================================================
# FUNGSI BANTU
# =====================================================================

def hitung_nutrisi(x1, x2, x3):
    """Menghitung total kalori, protein, natrium, dan biaya dari kombinasi sajian."""
    kalori  = x1 * KALORI[0]  + x2 * KALORI[1]  + x3 * KALORI[2]
    protein = x1 * PROTEIN[0] + x2 * PROTEIN[1] + x3 * PROTEIN[2]
    natrium = x1 * NATRIUM[0] + x2 * NATRIUM[1] + x3 * NATRIUM[2]
    biaya   = x1 * BIAYA[0]   + x2 * BIAYA[1]   + x3 * BIAYA[2]
    return kalori, protein, natrium, biaya


def cek_layak(kalori, protein, natrium):
    """Mengembalikan True jika semua kendala klinis terpenuhi."""
    return (
        kalori  >= MIN_KALORI  and
        protein >= MIN_PROTEIN and
        natrium <= MAX_NATRIUM
    )

# =====================================================================
# ALGORITMA BRUTE FORCE
# =====================================================================

def brute_force():
    """
    Enumerasi semua kombinasi integer (x1, x2, x3) dengan x1+x2+x3=12.

    Cara kerja:
      - Loop x1 dari 0 sampai 12
      - Loop x2 dari 0 sampai (12 - x1)
      - x3 dihitung otomatis: x3 = 12 - x1 - x2
        (menjamin kendala total sajian selalu terpenuhi)
      - Setiap kombinasi dievaluasi kelayakannya
      - Simpan kombinasi dengan biaya terkecil sebagai solusi terbaik

    Total kombinasi yang dievaluasi: C(12+2, 2) = 91 titik
    Kompleksitas waktu: O(n^2), n = TOTAL_SAJIAN + 1
    """

    best_sol    = None          # solusi terbaik yang ditemukan
    best_biaya  = float('inf')  # biaya terkecil sejauh ini
    cnt_layak   = 0             # jumlah kombinasi yang lolos semua kendala
    cnt_tidak   = 0             # jumlah kombinasi yang gagal minimal satu kendala
    semua_layak = []            # daftar seluruh solusi layak untuk ditampilkan

    log = []   # simpan semua baris log, dicetak SETELAH timer berhenti
    no  = 0    # nomor urut semua kombinasi

    # ── MULAI TIMER — hanya mengukur komputasi, bukan I/O print ──
    start = time.perf_counter()

    # Iterasi semua pasangan (x1, x2); x3 ditentukan otomatis
    for x1 in range(TOTAL_SAJIAN + 1):
        for x2 in range(TOTAL_SAJIAN - x1 + 1):

            # Hitung x3 agar x1+x2+x3 = 12 selalu terpenuhi
            x3 = TOTAL_SAJIAN - x1 - x2
            no += 1

            # Hitung nilai nutrisi dan biaya kombinasi ini
            kalori, protein, natrium, biaya = hitung_nutrisi(x1, x2, x3)

            # Periksa apakah memenuhi semua kendala klinis
            if cek_layak(kalori, protein, natrium):
                cnt_layak += 1
                semua_layak.append((biaya, x1, x2, x3, kalori, protein, natrium))

                # Perbarui solusi terbaik jika biaya lebih rendah
                if biaya < best_biaya:
                    best_biaya = biaya
                    best_sol   = (x1, x2, x3)

                status = "LAYAK  <--"
            else:
                cnt_tidak += 1
                status = "tidak layak"

            # Simpan ke log (belum dicetak agar tidak masuk hitungan waktu)
            log.append((no, x1, x2, x3, kalori, protein, natrium, biaya, status))

    # ── STOP TIMER ──
    durasi = time.perf_counter() - start

    # Cetak log setelah timer berhenti
    print("\n  Log Evaluasi Brute Force (semua kombinasi):")
    print(f"  {'No':>4}  {'x1':>3}  {'x2':>3}  {'x3':>3}  "
          f"{'Kalori':>7}  {'Protein':>7}  {'Natrium':>7}  {'Biaya':>12}  Status")
    print("  " + "-" * 80)
    for (no_, x1_, x2_, x3_, kal_, prot_, nat_, biaya_, status_) in log:
        print(f"  {no_:>4}  {x1_:>3}  {x2_:>3}  {x3_:>3}  "
              f"{kal_:>7}  {prot_:>7}  {nat_:>7}  "
              f"Rp{biaya_:>10,}  {status_}")

    return best_sol, cnt_layak, cnt_tidak, durasi, semua_layak

# =====================================================================
# TAMPILKAN HASIL
# =====================================================================

def tampilkan_hasil(best_sol, cnt_layak, cnt_tidak, durasi, semua_layak):
    """Menampilkan rangkuman hasil Brute Force ke layar."""

    print("\n" + "=" * 60)
    print("  HASIL BRUTE FORCE")
    print("=" * 60)

    if best_sol:
        x1, x2, x3 = best_sol
        kalori, protein, natrium, biaya = hitung_nutrisi(x1, x2, x3)

        print(f"  Solusi optimal  : A={x1} sajian, B={x2} sajian, C={x3} sajian")
        print(f"  Total biaya     : Rp {biaya:,.0f}")
        print(f"  Kalori          : {kalori} kkal  (minimal {MIN_KALORI})")
        print(f"  Protein         : {protein} g     (minimal {MIN_PROTEIN})")
        print(f"  Natrium         : {natrium} mg    (maksimal {MAX_NATRIUM})")
    else:
        print("  Solusi terbaik  : TIDAK DITEMUKAN")
        print("  (Tidak ada kombinasi yang memenuhi semua kendala)")

    print()
    print(f"  Total kombinasi dievaluasi  : {cnt_layak + cnt_tidak}")
    print(f"  Kombinasi LAYAK             : {cnt_layak}")
    print(f"  Kombinasi TIDAK LAYAK       : {cnt_tidak}")
    print(f"  Waktu eksekusi              : {durasi:.6f} detik")

    # Tampilkan peringkat semua solusi layak diurutkan berdasarkan biaya
    if semua_layak:
        semua_layak_sorted = sorted(semua_layak)
        print()
        print(f"  Peringkat semua solusi layak (diurutkan biaya terendah):")
        print(f"  {'Rank':<5} {'x1':>3} {'x2':>3} {'x3':>3} "
              f"{'Kalori':>7} {'Protein':>7} {'Natrium':>7} {'Biaya':>12}")
        print("  " + "-" * 58)
        for i, (biaya, x1, x2, x3, kal, prot, nat) in enumerate(semua_layak_sorted, 1):
            mark = "  <-- OPTIMAL" if i == 1 else ""
            print(f"  {i:<5} {x1:>3} {x2:>3} {x3:>3} "
                  f"{kal:>7} {prot:>7} {nat:>7} Rp{biaya:>10,}{mark}")

    print("=" * 60)

# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  BRUTE FORCE — PERENCANAAN NUTRISI PASCA-OPERASI")
    print("  Algoritma Evolusi & Kecerdasan Kelompok (CIF62342)")
    print("=" * 60)

    # Tampilkan data suplemen
    print()
    print("  Data Suplemen:")
    print(f"  {'Suplemen':<22} {'Kalori':>7} {'Protein':>8} {'Natrium':>8} {'Biaya':>12}")
    print("  " + "-" * 60)
    nama = ["A (Whey Protein)", "B (Carbohydrate)", "C (Fiber & Vit)"]
    for i in range(3):
        print(f"  {nama[i]:<22} {KALORI[i]:>7} {PROTEIN[i]:>8} "
              f"{NATRIUM[i]:>8} Rp{BIAYA[i]:>9,}")

    # Tampilkan parameter kendala
    print()
    print("  Kendala:")
    print(f"    Total sajian/hari : tepat {TOTAL_SAJIAN}")
    print(f"    Kalori minimal    : >= {MIN_KALORI} kkal")
    print(f"    Protein minimal   : >= {MIN_PROTEIN} g")
    print(f"    Natrium maksimal  : <= {MAX_NATRIUM} mg")

    # Jalankan Brute Force
    best_sol, cnt_layak, cnt_tidak, durasi, semua_layak = brute_force()

    # Tampilkan hasil lengkap
    tampilkan_hasil(best_sol, cnt_layak, cnt_tidak, durasi, semua_layak)

    # Catatan infeasibilitas jika tidak ada solusi
    if not best_sol:
        print()
        print("  CATATAN INFEASIBILITAS:")
        print("  Kendala kalori >= 1800 dan protein >= 70 tidak dapat")
        print("  dipenuhi bersamaan dengan tepat 12 sajian integer.")
        print()
        print("  Bukti: Substitusi x3 = 12 - x1 - x2 ke kendala kalori:")
        print("    40x1 + 70x2 >= 840")
        print("  Nilai maksimum di x1=0, x2=12 menghasilkan 840 (pas batas),")
        print("  namun protein = 5*12 = 60 < 70  --> GAGAL protein.")
        print()
        print("  Solusi PALING MENDEKATI layak:")
        print("    x1=1, x2=11, x3=0 -> kalori=1770 (kurang 30), protein=75 OK")
        print("    x1=0, x2=12, x3=0 -> kalori=1800 OK, protein=60 (kurang 10)")
