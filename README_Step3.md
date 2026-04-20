# Step 3 — Simulasi Brute Force & Random Search

**Tugas 1 | Algoritma Evolusi dan Kecerdasan Kelompok (CIF62342)**
Kasus: Perencanaan Nutrisi Pasca-Operasi

---

## Daftar File

| File | Keterangan |
|---|---|
| `brute_force.py` | Implementasi metode Brute Force |
| `random_search.py` | Implementasi metode Random Search |

---

## Cara Menjalankan

```bash
# Jalankan Brute Force
python brute_force.py

# Jalankan Random Search
python random_search.py
```

Tidak memerlukan library eksternal. Hanya menggunakan modul bawaan Python: `random` dan `time`.

---

## Deskripsi Masalah

Seorang ahli gizi perlu menentukan jumlah sajian **(x₁, x₂, x₃)** dari tiga suplemen agar **total biaya harian minimum** tanpa melanggar batasan klinis.

| Suplemen | Kalori (kkal) | Protein (g) | Natrium (mg) | Biaya (Rp) |
|---|:---:|:---:|:---:|:---:|
| A — Whey Protein Isolate | 120 | 20 | 80 | 25.000 |
| B — Complex Carbohydrate | 150 | 5 | 30 | 15.000 |
| C — Fiber & Vitamin Blend | 80 | 8 | 120 | 20.000 |

**Fungsi Tujuan (Minimasi Biaya):**
```
Minimasi: Z = 25.000·x₁ + 15.000·x₂ + 20.000·x₃
```

**Kendala:**
```
x₁ + x₂ + x₃        = 12       (tepat 12 sajian/hari)
120x₁ + 150x₂ + 80x₃  ≥ 1.800  (kalori minimal)
 20x₁ +   5x₂ +  8x₃  ≥ 70     (protein minimal)
 80x₁ +  30x₂ + 120x₃ ≤ 2.000  (natrium maksimal)
x₁, x₂, x₃ ∈ ℤ⁺ ∪ {0}         (bilangan bulat non-negatif)
```

---

## Temuan Penting: Masalah Infeasible

> Dengan kendala asli, **tidak ada kombinasi integer** yang memenuhi seluruh kendala secara bersamaan. Kedua algoritma dengan benar melaporkan **0 solusi layak**.

**Bukti matematis:**

Substitusikan x₃ = 12 − x₁ − x₂ ke kendala kalori:
```
120x₁ + 150x₂ + 80(12−x₁−x₂) ≥ 1.800
40x₁ + 70x₂ ≥ 840   ... (*)
```

Nilai maksimum ruas kiri (*) dengan syarat x₁+x₂ ≤ 12 dicapai di **x₁=0, x₂=12**:
```
40(0) + 70(12) = 840   (tepat di batas, bukan lebih besar)
```

Namun titik ini menghasilkan protein = 5 × 12 = **60 g < 70 g** → GAGAL kendala protein.

Sebaliknya, jika protein ≥ 70 diprioritaskan, kalori tertinggi yang bisa dicapai adalah **1770 kkal** (x₁=1, x₂=11, x₃=0), masih kurang 30 kkal dari target 1800 kkal.

**Kesimpulan:** Kendala kalori ≥ 1800 dan protein ≥ 70 **saling bertentangan** pada ruang solusi integer dengan total 12 sajian. Temuan ini sendiri merupakan informasi klinis yang berharga — dokter/ahli gizi perlu meninjau ulang target nutrisi atau jumlah sajian.

---

## Cara Kerja: Brute Force (`brute_force.py`)

### Pseudocode

```
PROSEDUR BruteForce():
  best_sol   ← NULL
  best_biaya ← tak terhingga
  cnt_layak  ← 0
  cnt_tidak  ← 0

  UNTUK x1 DARI 0 SAMPAI 12:
    UNTUK x2 DARI 0 SAMPAI (12 − x1):
      x3 ← 12 − x1 − x2              // paksa total = 12
      (kalori, protein, natrium, biaya) ← hitung_nutrisi(x1, x2, x3)

      JIKA kalori≥1800 DAN protein≥70 DAN natrium≤2000:
        cnt_layak ← cnt_layak + 1
        JIKA biaya < best_biaya:
          best_biaya ← biaya
          best_sol   ← (x1, x2, x3)
      JIKA TIDAK:
        cnt_tidak ← cnt_tidak + 1

  KEMBALIKAN best_sol, cnt_layak, cnt_tidak
```

### Penjelasan Detail

**Pembangkitan ruang solusi:**
- Loop ganda (x₁, x₂) mencakup semua kemungkinan pasangan.
- x₃ dihitung otomatis sebagai `12 − x₁ − x₂` sehingga kendala total sajian **selalu terpenuhi** tanpa filter tambahan.
- Total kombinasi yang dievaluasi = C(12+2, 2) = **91 titik**.

**Evaluasi setiap titik:**
Setiap kombinasi diperiksa terhadap tiga kendala klinis. Jika lolos semua, dicatat sebagai solusi layak dan dibandingkan dengan solusi terbaik saat ini.

**Garansi optimal:**
Karena **semua 91 titik** dievaluasi, solusi yang ditemukan dijamin merupakan **optimal global** — tidak ada kombinasi yang lebih murah dan masih layak yang terlewat.

**Kompleksitas waktu:** O(n²), n = TOTAL_SAJIAN + 1 = 13

### Output yang Dicatat

| Informasi | Keterangan |
|---|---|
| Solusi terbaik (x₁, x₂, x₃) | Komposisi sajian dengan biaya minimum |
| Total biaya | Rp/hari |
| Kalori / Protein / Natrium | Verifikasi kelayakan klinis |
| Evaluasi layak | Jumlah kombinasi yang lolos semua kendala |
| Evaluasi tidak layak | Jumlah kombinasi yang gagal ≥ 1 kendala |
| Waktu eksekusi | Diukur dengan `time.perf_counter()` |
| Peringkat solusi layak | Semua solusi layak diurutkan dari biaya terendah |

---

## Cara Kerja: Random Search (`random_search.py`)

### Pseudocode

```
PROSEDUR RandomSearch(seed=42):
  TETAPKAN random seed ← seed     // reproducibility
  best_sol   ← NULL
  best_biaya ← tak terhingga
  cnt_layak  ← 0
  cnt_tidak  ← 0

  UNTUK i DARI 1 SAMPAI 40:
    x1 ← acak_bulat(0, 12)
    x2 ← acak_bulat(0, 12 − x1)
    x3 ← 12 − x1 − x2            // paksa total = 12
    (kalori, protein, natrium, biaya) ← hitung_nutrisi(x1, x2, x3)

    JIKA kalori≥1800 DAN protein≥70 DAN natrium≤2000:
      cnt_layak ← cnt_layak + 1
      JIKA biaya < best_biaya:
        best_biaya ← biaya
        best_sol   ← (x1, x2, x3)
    JIKA TIDAK:
      cnt_tidak ← cnt_tidak + 1
    CATAT log iterasi ke-i

  KEMBALIKAN best_sol, cnt_layak, cnt_tidak
```

### Penjelasan Detail

**Pembangkitan kandidat acak (`bangkit_kandidat()`):**
1. Pilih x₁ secara acak dari [0, 12]
2. Pilih x₂ secara acak dari [0, 12−x₁]
3. Hitung x₃ = 12 − x₁ − x₂

Cara ini menjamin kendala total sajian = 12 selalu terpenuhi pada setiap sampel, sehingga satu-satunya evaluasi yang diperlukan adalah tiga kendala klinis (kalori, protein, natrium).

**Reproducibility:**
`random.seed(42)` memastikan urutan bilangan acak yang sama setiap kali program dijalankan, sehingga hasil dapat diverifikasi dan direproduksi.

**Sifat probabilistik:**
Random Search **tidak menjamin** menemukan solusi optimal karena hanya menjelajahi sebagian ruang solusi (40 dari 91 titik = 44%). Solusi yang ditemukan bergantung pada seed yang digunakan.

**Demonstrasi multi-seed:**
Program juga menjalankan 5 seed berbeda (42, 7, 123, 999, 2024) untuk menunjukkan bahwa hasil bisa berbeda-beda, membuktikan sifat non-deterministik metode ini.

### Output yang Dicatat

| Informasi | Keterangan |
|---|---|
| Log per iterasi | x₁, x₂, x₃, kalori, protein, natrium, biaya, status layak/tidak |
| Solusi terbaik | Kombinasi dengan biaya minimum dari sampel yang layak |
| Evaluasi layak / tidak layak | Jumlah sampel yang lolos / gagal kendala |
| Waktu eksekusi | Diukur dengan `time.perf_counter()` |
| Persentase ruang terjelajahi | Berapa persen dari 91 titik yang dievaluasi |
| Uji multi-seed | Perbandingan hasil dengan 5 nilai seed berbeda |

---

## Perbandingan Kedua Metode

| Aspek | Brute Force | Random Search |
|---|:---:|:---:|
| **Garansi solusi optimal** | Ya (pasti) | Tidak (probabilistik) |
| **Total evaluasi** | 91 (selalu tetap) | 40 (sesuai iterasi) |
| **Waktu eksekusi rata-rata** | **0.000058 detik** | 0.000061 detik |
| **Waktu eksekusi median** | **0.000055 detik** | 0.000061 detik |
| **Hasil dipengaruhi seed** | Tidak | Ya |
| **Kompleksitas skalabilitas** | O(n²) — meledak | O(iterasi) — konstan |
| **Cocok untuk** | Dataset kecil, butuh kepastian | Dataset besar, butuh kecepatan |

### Perbandingan Waktu Eksekusi — 10 Percobaan

Pengukuran dilakukan dengan menjalankan `brute_force.py` dan `random_search.py` masing-masing 10 kali. Waktu yang diukur hanya bagian komputasi murni (print dilakukan di luar timer).

| Percobaan | Brute Force (detik) | Random Search (detik) | Lebih Cepat |
|:---:|:---:|:---:|:---:|
| 1  | 0.000089 | 0.000061 | RS |
| 2  | 0.000068 | 0.000063 | RS |
| 3  | 0.000067 | 0.000053 | RS |
| 4  | 0.000051 | 0.000061 | BF |
| 5  | 0.000044 | 0.000072 | BF |
| 6  | 0.000052 | 0.000057 | BF |
| 7  | 0.000058 | 0.000068 | BF |
| 8  | 0.000039 | 0.000055 | BF |
| 9  | 0.000063 | 0.000059 | RS |
| 10 | 0.000052 | 0.000065 | BF |
| **Rata-rata** | **0.000058** | **0.000061** | |
| **Median** | **0.000055** | **0.000061** | |
| **Min** | 0.000039 | 0.000053 | |
| **Maks** | 0.000089 | 0.000072 | |
| **Stdev** | 0.000014 | 0.000006 | |

**Kesimpulan dari 10 percobaan:** Brute Force lebih cepat di **6 dari 10 percobaan**, namun selisihnya sangat kecil (rata-rata hanya 0.000003 detik). Hasil tidak konsisten karena dipengaruhi kondisi CPU dan OS saat itu.

Yang menarik: **Random Search justru lebih stabil** (stdev 0.000006 vs 0.000014). Brute Force lebih fluktuatif karena loop ganda bersarang lebih sensitif terhadap cache CPU.

### Mengapa Selisihnya Sangat Kecil dan Tidak Konsisten?

Pada dataset sekecil ini (91 vs 40 evaluasi), kedua metode sama-sama selesai dalam waktu di bawah 0.1 ms. Pada skala ini, faktor eksternal seperti **context switch OS**, **cache CPU**, dan **variasi clock** berpengaruh lebih besar daripada perbedaan algoritma itu sendiri.

Yang bisa disimpulkan secara konsisten adalah:
- Brute Force mengevaluasi **lebih banyak titik** (91 vs 40) namun tiap evaluasinya **lebih ringan** (hanya loop counter, tanpa RNG)
- Random Search mengevaluasi **lebih sedikit titik** namun tiap evaluasinya **sedikit lebih berat** (memanggil `random.randint()` dua kali)
- Pada dataset kecil, keduanya **hampir setara** dan pemenang tiap run bisa berganti

Jika ruang solusi membesar ke ribuan titik ke atas, Random Search akan jauh lebih cepat karena jumlah evaluasinya tetap konstan (40 iterasi), sementara Brute Force tumbuh secara O(n²).

### Penjelasan Skalabilitas

Jika jumlah suplemen bertambah dari 3 menjadi k dengan total sajian n:
- **Brute Force:** jumlah kombinasi = C(n+k−1, k−1), tumbuh secara **kombinatorial** → tidak praktis untuk masalah besar
- **Random Search:** jumlah evaluasi tetap = jumlah iterasi (misal 40) → **skalabel** untuk masalah apapun, namun kualitas solusi bergantung pada keberuntungan

---

## Struktur Kode

### `brute_force.py`

```
brute_force.py
│
├── DATA SUPLEMEN & PARAMETER KENDALA  — konstanta nutrisi dan biaya
│
├── hitung_nutrisi(x1, x2, x3)  — hitung kalori, protein, natrium, biaya
├── cek_layak(kalori, protein, natrium)  — evaluasi apakah memenuhi kendala
│
├── brute_force()        — algoritma utama enumerasi ekshaustif
├── tampilkan_hasil()    — format dan cetak hasil ke layar
│
└── main                 — tampilkan data, jalankan algoritma, cetak hasil
```

### `random_search.py`

```
random_search.py
│
├── DATA SUPLEMEN & PARAMETER KENDALA  — konstanta nutrisi dan biaya
│
├── hitung_nutrisi(x1, x2, x3)  — hitung kalori, protein, natrium, biaya
├── cek_layak(kalori, protein, natrium)  — evaluasi apakah memenuhi kendala
├── bangkit_kandidat()   — bangkitkan satu kandidat acak yang valid (total=12)
│
├── random_search(seed)  — algoritma utama sampling acak 40 iterasi
├── tampilkan_hasil()    — format dan cetak hasil ke layar
│
└── main                 — tampilkan data, jalankan algoritma, uji multi-seed
```

---

## Kesesuaian dengan Rubrik Penilaian (Kriteria 2 — Bobot 20%)

| Indikator Rubrik | Implementasi |
|---|---|
| Kode/simulasi berjalan benar tanpa error | Diuji dengan `python brute_force.py` dan `python random_search.py` |
| Log evaluasi jelas | Tabel log per-iterasi di Random Search; log solusi layak di Brute Force |
| Hasil tercatat lengkap | Biaya, kalori, protein, natrium, waktu eksekusi, jumlah layak/tidak layak |
| Perbandingan efisiensi & kelayakan akurat | Tabel perbandingan eksplisit di README; analisis skalabilitas |
| Solusi terbaik tercatat | Ditampilkan beserta verifikasi semua kendala klinis |
| Analisis infeasibilitas | Bukti matematis dengan substitusi variabel dan penjelasan kontradiksi |
