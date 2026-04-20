"""
Tugas 1 - Step 3b: Simulasi Random Search
Kasus: Perencanaan Nutrisi Pasca-Operasi
Mata Kuliah: Algoritma Evolusi dan Kecerdasan Kelompok (CIF62342)

Metode Random Search mengambil 40 sampel acak dari ruang solusi,
mengevaluasi kelayakan dan biaya setiap sampel, lalu mencatat
solusi terbaik yang ditemukan selama proses pencarian.
"""

import random
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
JUMLAH_ITERASI = 40     # jumlah sampel acak yang diambil

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


def bangkit_kandidat():
    """
    Membangkitkan satu kandidat solusi acak (x1, x2, x3).

    Cara:
      1. Pilih x1 secara acak dari [0, 12]
      2. Pilih x2 secara acak dari [0, 12 - x1]
      3. Hitung x3 = 12 - x1 - x2  (menjamin total = 12)

    Dengan cara ini, kendala 'tepat 12 sajian' selalu terpenuhi
    pada setiap kandidat tanpa perlu filter tambahan.
    """
    x1 = random.randint(0, TOTAL_SAJIAN)
    x2 = random.randint(0, TOTAL_SAJIAN - x1)
    x3 = TOTAL_SAJIAN - x1 - x2
    return x1, x2, x3

# =====================================================================
# ALGORITMA RANDOM SEARCH
# =====================================================================

def random_search(seed=42):
    """
    Pencarian acak dengan 40 iterasi dari ruang solusi.

    Cara kerja:
      - Tetapkan seed agar hasil reproducible
      - Setiap iterasi: bangkitkan kandidat acak, evaluasi, catat hasilnya
      - Simpan kandidat layak dengan biaya terkecil sebagai solusi terbaik
      - Tidak menjamin optimal karena hanya menjelajahi sebagian ruang solusi

    Parameter:
      seed : angka awal generator acak (default 42)
    """

    # Tetapkan seed untuk memastikan hasil yang sama setiap kali dijalankan
    random.seed(seed)

    best_sol   = None           # solusi terbaik yang ditemukan
    best_biaya = float('inf')   # biaya terkecil sejauh ini
    cnt_layak  = 0              # jumlah sampel yang lolos semua kendala
    cnt_tidak  = 0              # jumlah sampel yang gagal minimal satu kendala
    log        = []             # simpan semua baris log, dicetak SETELAH timer berhenti

    # ── MULAI TIMER — hanya mengukur komputasi, bukan I/O print ──
    start = time.perf_counter()

    for i in range(1, JUMLAH_ITERASI + 1):

        # Bangkitkan satu kandidat solusi secara acak
        x1, x2, x3 = bangkit_kandidat()

        # Hitung nilai nutrisi dan biaya kandidat ini
        kalori, protein, natrium, biaya = hitung_nutrisi(x1, x2, x3)

        # Evaluasi kelayakan berdasarkan semua kendala klinis
        layak = cek_layak(kalori, protein, natrium)

        if layak:
            cnt_layak += 1
            status = "LAYAK  <--"

            # Perbarui solusi terbaik jika biaya lebih rendah
            if biaya < best_biaya:
                best_biaya = biaya
                best_sol   = (x1, x2, x3)
        else:
            cnt_tidak += 1
            status = "tidak layak"

        # Simpan ke log (belum dicetak agar tidak masuk hitungan waktu)
        log.append((i, x1, x2, x3, kalori, protein, natrium, biaya, status))

    # ── STOP TIMER ──
    durasi = time.perf_counter() - start

    # Cetak log setelah timer berhenti
    print(f"\n  Log {JUMLAH_ITERASI} Iterasi Random Search:")
    print(f"  {'Iter':>4}  {'x1':>3}  {'x2':>3}  {'x3':>3}  "
          f"{'Kalori':>7}  {'Protein':>7}  {'Natrium':>7}  "
          f"{'Biaya':>12}  Status")
    print("  " + "-" * 74)
    for (i_, x1_, x2_, x3_, kal_, prot_, nat_, biaya_, status_) in log:
        print(f"  {i_:>4}  {x1_:>3}  {x2_:>3}  {x3_:>3}  "
              f"{kal_:>7}  {prot_:>7}  {nat_:>7}  "
              f"Rp{biaya_:>10,}  {status_}")

    return best_sol, cnt_layak, cnt_tidak, durasi

# =====================================================================
# TAMPILKAN HASIL
# =====================================================================

def tampilkan_hasil(best_sol, cnt_layak, cnt_tidak, durasi):
    """Menampilkan rangkuman hasil Random Search ke layar."""

    print("\n" + "=" * 60)
    print("  HASIL RANDOM SEARCH")
    print("=" * 60)

    if best_sol:
        x1, x2, x3 = best_sol
        kalori, protein, natrium, biaya = hitung_nutrisi(x1, x2, x3)

        print(f"  Solusi terbaik  : A={x1} sajian, B={x2} sajian, C={x3} sajian")
        print(f"  Total biaya     : Rp {biaya:,.0f}")
        print(f"  Kalori          : {kalori} kkal  (minimal {MIN_KALORI})")
        print(f"  Protein         : {protein} g     (minimal {MIN_PROTEIN})")
        print(f"  Natrium         : {natrium} mg    (maksimal {MAX_NATRIUM})")
    else:
        print("  Solusi terbaik  : TIDAK DITEMUKAN")
        print("  (Tidak ada sampel acak yang memenuhi semua kendala)")

    print()
    print(f"  Total sampel dievaluasi  : {cnt_layak + cnt_tidak}")
    print(f"  Sampel LAYAK             : {cnt_layak}")
    print(f"  Sampel TIDAK LAYAK       : {cnt_tidak}")
    print(f"  Waktu eksekusi           : {durasi:.6f} detik")
    print()

    # Catatan probabilistik
    total_ruang = 91  # total kombinasi dalam ruang solusi (C(14,2))
    persen_jelajah = (cnt_layak + cnt_tidak) / total_ruang * 100
    print(f"  Catatan:")
    print(f"  - Random Search menjelajahi {cnt_layak+cnt_tidak} dari {total_ruang} "
          f"titik ({persen_jelajah:.1f}% ruang solusi)")
    print(f"  - Hasil bisa berbeda jika seed diubah")
    print(f"  - Tidak menjamin menemukan solusi OPTIMAL GLOBAL")

    print("=" * 60)

# =====================================================================
# MAIN
# =====================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  RANDOM SEARCH — PERENCANAAN NUTRISI PASCA-OPERASI")
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
    print(f"    Total sajian/hari  : tepat {TOTAL_SAJIAN}")
    print(f"    Kalori minimal     : >= {MIN_KALORI} kkal")
    print(f"    Protein minimal    : >= {MIN_PROTEIN} g")
    print(f"    Natrium maksimal   : <= {MAX_NATRIUM} mg")
    print(f"    Jumlah iterasi     : {JUMLAH_ITERASI}")

    # Jalankan Random Search dengan seed default
    best_sol, cnt_layak, cnt_tidak, durasi = random_search(seed=42)

    # Tampilkan hasil lengkap
    tampilkan_hasil(best_sol, cnt_layak, cnt_tidak, durasi)

    # Demonstrasi pengaruh seed berbeda
    print()
    print("  Uji coba dengan seed berbeda (untuk menunjukkan sifat probabilistik):")
    print(f"  {'Seed':>6}  {'Layak':>6}  {'Tdk Layak':>10}  Solusi Terbaik")
    print("  " + "-" * 50)
    for s in [42, 7, 123, 999, 2024]:
        random.seed(s)
        b_sol = None
        b_biaya = float('inf')
        b_lay = 0
        b_tdk = 0
        for _ in range(JUMLAH_ITERASI):
            x1, x2, x3 = bangkit_kandidat()
            kal, prot, nat, biaya = hitung_nutrisi(x1, x2, x3)
            if cek_layak(kal, prot, nat):
                b_lay += 1
                if biaya < b_biaya:
                    b_biaya = biaya
                    b_sol = (x1, x2, x3)
            else:
                b_tdk += 1
        sol_str = (f"A={b_sol[0]},B={b_sol[1]},C={b_sol[2]} Rp{b_biaya:,}"
                   if b_sol else "tidak ditemukan")
        print(f"  {s:>6}  {b_lay:>6}  {b_tdk:>10}  {sol_str}")
