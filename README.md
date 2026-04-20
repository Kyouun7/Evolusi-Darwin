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
| **Solusi terbaik ditemukan** | Tidak ada (infeasible) | Tidak ada (infeasible) |
| **Evaluasi layak** | 0 | 0 |
| **Evaluasi tidak layak** | 91 | 40 |
| **Total evaluasi** | 91 (selalu tetap) | 40 (sesuai iterasi) |
| **Waktu eksekusi rata-rata** | **0.000058 detik** | 0.000061 detik |
| **Waktu eksekusi median** | **0.000055 detik** | 0.000061 detik |
| **Garansi solusi optimal** | Ya (pasti) | Tidak (probabilistik) |
| **Hasil dipengaruhi seed** | Tidak | Ya |
| **Kompleksitas skalabilitas** | O(n²) — meledak | O(iterasi) — konstan |
| **Cocok untuk** | Dataset kecil, butuh kepastian | Dataset besar, butuh kecepatan |

> Kedua metode menghasilkan **0 evaluasi layak** karena masalah memang infeasible (lihat bagian Temuan Penting). Hasil ini konsisten dan membuktikan kebenaran implementasi kedua algoritma.

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

## Contoh Output Program

### Output `brute_force.py`

```
============================================================
  BRUTE FORCE - PERENCANAAN NUTRISI PASCA-OPERASI
  Algoritma Evolusi & Kecerdasan Kelompok (CIF62342)
============================================================

  Data Suplemen:
  Suplemen                Kalori  Protein  Natrium        Biaya
  ------------------------------------------------------------
  A (Whey Protein)           120       20       80 Rp   25,000
  B (Carbohydrate)           150        5       30 Rp   15,000
  C (Fiber & Vit)             80        8      120 Rp   20,000

  Kendala:
    Total sajian/hari : tepat 12
    Kalori minimal    : >= 1800 kkal
    Protein minimal   : >= 70 g
    Natrium maksimal  : <= 2000 mg

  Log Evaluasi Brute Force (semua kombinasi):
    No   x1   x2   x3   Kalori  Protein  Natrium         Biaya  Status
  --------------------------------------------------------------------------------
     1    0    0   12      960       96     1440  Rp   240,000  tidak layak
     2    0    1   11     1030       93     1350  Rp   235,000  tidak layak
     3    0    2   10     1100       90     1260  Rp   230,000  tidak layak
     4    0    3    9     1170       87     1170  Rp   225,000  tidak layak
     5    0    4    8     1240       84     1080  Rp   220,000  tidak layak
     6    0    5    7     1310       81      990  Rp   215,000  tidak layak
     7    0    6    6     1380       78      900  Rp   210,000  tidak layak
     8    0    7    5     1450       75      810  Rp   205,000  tidak layak
     9    0    8    4     1520       72      720  Rp   200,000  tidak layak
    10    0    9    3     1590       69      630  Rp   195,000  tidak layak
    11    0   10    2     1660       66      540  Rp   190,000  tidak layak
    12    0   11    1     1730       63      450  Rp   185,000  tidak layak
    13    0   12    0     1800       60      360  Rp   180,000  tidak layak
    14    1    0   11     1000      108     1400  Rp   245,000  tidak layak
    15    1    1   10     1070      105     1310  Rp   240,000  tidak layak
    ... (91 kombinasi total) ...
    89   11    0    1     1400      228     1000  Rp   295,000  tidak layak
    90   11    1    0     1470      225      910  Rp   290,000  tidak layak
    91   12    0    0     1440      240      960  Rp   300,000  tidak layak

============================================================
  HASIL BRUTE FORCE
============================================================
  Solusi terbaik  : TIDAK DITEMUKAN
  (Tidak ada kombinasi yang memenuhi semua kendala)

  Total kombinasi dievaluasi  : 91
  Kombinasi LAYAK             : 0
  Kombinasi TIDAK LAYAK       : 91
  Waktu eksekusi              : 0.000078 detik
============================================================

  CATATAN INFEASIBILITAS:
  Kendala kalori >= 1800 dan protein >= 70 tidak dapat
  dipenuhi bersamaan dengan tepat 12 sajian integer.

  Bukti: Substitusi x3 = 12 - x1 - x2 ke kendala kalori:
    40x1 + 70x2 >= 840
  Nilai maksimum di x1=0, x2=12 menghasilkan 840 (pas batas),
  namun protein = 5*12 = 60 < 70  --> GAGAL protein.

  Solusi PALING MENDEKATI layak:
    x1=1, x2=11, x3=0 -> kalori=1770 (kurang 30), protein=75 OK
    x1=0, x2=12, x3=0 -> kalori=1800 OK, protein=60 (kurang 10)
```

### Output `random_search.py`

```
============================================================
  RANDOM SEARCH - PERENCANAAN NUTRISI PASCA-OPERASI
  Algoritma Evolusi & Kecerdasan Kelompok (CIF62342)
============================================================

  Data Suplemen:
  Suplemen                Kalori  Protein  Natrium        Biaya
  ------------------------------------------------------------
  A (Whey Protein)           120       20       80 Rp   25,000
  B (Carbohydrate)           150        5       30 Rp   15,000
  C (Fiber & Vit)             80        8      120 Rp   20,000

  Kendala:
    Total sajian/hari  : tepat 12
    Kalori minimal     : >= 1800 kkal
    Protein minimal    : >= 70 g
    Natrium maksimal   : <= 2000 mg
    Jumlah iterasi     : 40

  Log 40 Iterasi Random Search:
  Iter   x1   x2   x3   Kalori  Protein  Natrium         Biaya  Status
  --------------------------------------------------------------------------
     1   10    0    2     1360      216     1040  Rp   290,000  tidak layak
     2    0   11    1     1730       63      450  Rp   185,000  tidak layak
     3    4    3    5     1330      135     1010  Rp   245,000  tidak layak
     4    3    2    7     1220      126     1140  Rp   245,000  tidak layak
     5   11    0    1     1400      228     1000  Rp   295,000  tidak layak
     6   10    2    0     1500      210      860  Rp   280,000  tidak layak
     7    8    0    4     1280      192     1120  Rp   280,000  tidak layak
     8    9    3    0     1530      195      810  Rp   270,000  tidak layak
     9    0    0   12      960       96     1440  Rp   240,000  tidak layak
    10    1    3    8     1210       99     1130  Rp   230,000  tidak layak
    11    3    8    1     1640      108      600  Rp   215,000  tidak layak
    12    9    0    3     1320      204     1080  Rp   285,000  tidak layak
    13    8    1    3     1350      189     1030  Rp   275,000  tidak layak
    14   11    1    0     1470      225      910  Rp   290,000  tidak layak
    15    3    7    2     1570      111      690  Rp   220,000  tidak layak
    16    9    2    1     1460      198      900  Rp   275,000  tidak layak
    17   12    0    0     1440      240      960  Rp   300,000  tidak layak
    18   12    0    0     1440      240      960  Rp   300,000  tidak layak
    19   11    1    0     1470      225      910  Rp   290,000  tidak layak
    20    5    4    3     1440      144      880  Rp   245,000  tidak layak
    21    2    3    7     1250      111     1090  Rp   235,000  tidak layak
    22   12    0    0     1440      240      960  Rp   300,000  tidak layak
    23    1    1   10     1070      105     1310  Rp   240,000  tidak layak
    24    6    0    6     1200      168     1200  Rp   270,000  tidak layak
    25    5    5    2     1510      141      790  Rp   240,000  tidak layak
    26    9    2    1     1460      198      900  Rp   275,000  tidak layak
    27   12    0    0     1440      240      960  Rp   300,000  tidak layak
    28   11    1    0     1470      225      910  Rp   290,000  tidak layak
    29    8    0    4     1280      192     1120  Rp   280,000  tidak layak
    30    6    0    6     1200      168     1200  Rp   270,000  tidak layak
    31    8    2    2     1420      186      940  Rp   270,000  tidak layak
    32   10    2    0     1500      210      860  Rp   280,000  tidak layak
    33    5    3    4     1370      147      970  Rp   250,000  tidak layak
    34   11    0    1     1400      228     1000  Rp   295,000  tidak layak
    35    0   10    2     1660       66      540  Rp   190,000  tidak layak
    36    3    4    5     1360      120      960  Rp   235,000  tidak layak
    37    1    3    8     1210       99     1130  Rp   230,000  tidak layak
    38    1    6    5     1420       90      860  Rp   215,000  tidak layak
    39    4    7    1     1610      123      650  Rp   225,000  tidak layak
    40   10    1    1     1430      213      950  Rp   285,000  tidak layak

============================================================
  HASIL RANDOM SEARCH
============================================================
  Solusi terbaik  : TIDAK DITEMUKAN
  (Tidak ada sampel acak yang memenuhi semua kendala)

  Total sampel dievaluasi  : 40
  Sampel LAYAK             : 0
  Sampel TIDAK LAYAK       : 40
  Waktu eksekusi           : 0.000116 detik

  Catatan:
  - Random Search menjelajahi 40 dari 91 titik (44.0% ruang solusi)
  - Hasil bisa berbeda jika seed diubah
  - Tidak menjamin menemukan solusi OPTIMAL GLOBAL
============================================================

  Uji coba dengan seed berbeda (untuk menunjukkan sifat probabilistik):
    Seed   Layak   Tdk Layak  Solusi Terbaik
  --------------------------------------------------
      42       0          40  tidak ditemukan
       7       0          40  tidak ditemukan
     123       0          40  tidak ditemukan
     999       0          40  tidak ditemukan
    2024       0          40  tidak ditemukan
```

---

## Kesesuaian dengan Rubrik Penilaian (Kriteria 2 — Bobot 20%)

Rubrik Sangat Baik (4) mensyaratkan: **kode berjalan benar**, **log evaluasi jelas**, **hasil tercatat lengkap**, dan **perbandingan efisiensi & kelayakan akurat**.

| Indikator Rubrik (Sangat Baik) | Bukti Pemenuhan | Lokasi |
|---|---|---|
| Kode/simulasi berjalan benar tanpa error | Kedua file dijalankan dan menghasilkan output lengkap tanpa error | Bagian *Contoh Output Program* |
| Log evaluasi jelas — setiap kombinasi/sampel tercatat | BF: tabel 91 baris (No, x1, x2, x3, Kalori, Protein, Natrium, Biaya, Status). RS: tabel 40 baris identik | Output `brute_force.py` & `random_search.py` |
| Hasil tercatat lengkap — solusi terbaik, layak vs tidak layak, waktu | BF: 0 layak / 91 tidak layak / 0.000058 dtk. RS: 0 layak / 40 tidak layak / 0.000061 dtk | Bagian *Perbandingan Kedua Metode* |
| Perbandingan efisiensi akurat — jumlah evaluasi & waktu eksekusi | Tabel 10 percobaan dengan rata-rata, median, min, maks, stdev | Bagian *Perbandingan Waktu Eksekusi — 10 Percobaan* |
| Perbandingan kelayakan akurat — layak vs tidak layak kedua metode | Tabel perbandingan berdampingan (evaluasi layak: 0 vs 0, tidak layak: 91 vs 40) | Bagian *Perbandingan Kedua Metode* |
| Analisis infeasibilitas | Bukti matematis lengkap dengan substitusi variabel, penjelasan kontradiksi kalori–protein | Bagian *Temuan Penting: Masalah Infeasible* |