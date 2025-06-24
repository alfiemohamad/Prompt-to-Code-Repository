from typing import Literal

RiskCategory = Literal["rendah", "sedang", "tinggi"]

def validate_input(
    penghasilan_bulanan: float,
    keterlambatan: int,
    usia: int,
    status_pekerjaan: str,
    total_pinjaman: int
) -> None:
    if penghasilan_bulanan < 0:
        raise ValueError("Penghasilan bulanan tidak boleh negatif")
    if keterlambatan < 0:
        raise ValueError("Frekuensi keterlambatan tidak boleh negatif")
    if usia < 18 or usia > 100:
        raise ValueError("Usia harus antara 18 dan 100 tahun")
    if status_pekerjaan not in ["karyawan", "wirausaha", "tidak bekerja"]:
        raise ValueError("Status pekerjaan tidak valid")
    if total_pinjaman < 0:
        raise ValueError("Total pinjaman tidak boleh negatif")

def hitung_skor_risiko(
    penghasilan_bulanan: float,
    keterlambatan: int,
    usia: int,
    status_pekerjaan: str,
    total_pinjaman: int
) -> RiskCategory:
    """
    Menghitung skor risiko nasabah berdasarkan parameter yang diberikan.
    """
    validate_input(penghasilan_bulanan, keterlambatan, usia, status_pekerjaan, total_pinjaman)
    
    skor = 0

    # Penghasilan bulanan
    if penghasilan_bulanan < 3000000:
        skor += 2
    elif penghasilan_bulanan < 7000000:
        skor += 1

    # Frekuensi keterlambatan pembayaran
    if keterlambatan >= 5:
        skor += 2
    elif keterlambatan >= 2:
        skor += 1

    # Usia dan status pekerjaan
    if usia < 25 and status_pekerjaan == "tidak bekerja":
        skor += 2
    elif usia < 25 or status_pekerjaan == "tidak bekerja":
        skor += 1

    # Total pinjaman aktif
    if total_pinjaman >= 3:
        skor += 2
    elif total_pinjaman == 2:
        skor += 1

    # Penentuan kategori risiko
    if skor <= 2:
        return "rendah"
    elif skor <= 4:
        return "sedang"
    else:
        return "tinggi"