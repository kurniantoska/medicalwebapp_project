from django.db import models
# from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.core.validators import (
    MinValueValidator, MaxValueValidator
)

from calendar import day_name
# import locale
#
# # set locale for general
# locale.setlocale(locale.LC_ALL, settings.LANGUAGE_CODE)


# Kecamatan input
class Kecamatan(models.Model):
    kecamatan = models.CharField(max_length=30)


# Kelurahan input
class Kelurahan(models.Model):
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.CharField(max_length=30)


# test_import_export apps
class Person(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    birth_date = models.DateField()
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


# poliklinik
class Poliklinik(models.Model):
    jenis_poli = models.CharField(max_length=20)

    def __str__(self):
        return self.jenis_poli


# database dokter
class Dokter(models.Model):
    nip = models.CharField(max_length=20)
    nama_dokter = models.CharField(max_length= 200)
    poli = models.ForeignKey(Poliklinik, on_delete=models.CASCADE)
    alamat = models.TextField()
    no_hp = models.CharField(max_length=16)

    def __str__(self):
        return self.nama_dokter

# Jadwal Dokter
class Jadwal_Dokter(models.Model):
    no_hari = range(8)
    list_nama_hari = tuple(zip(range(8), day_name))
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE)
    hari = models.CharField(max_length=1, choices=list_nama_hari)


from .static_var import KECAMATAN_KELURAHAN_SURABAYA


# puskesmas
class Puskesmas(models.Model):
    nama = models.CharField(max_length=60)
    kecamatan_kelurahan = models.CharField(max_length=50, choices = KECAMATAN_KELURAHAN_SURABAYA)
    alamat = models.TextField()

    def __str__(self):
        return self.nama

from django.contrib.auth.models import User

# user petugas puskesmas
class PetugasPuskesmas(models.Model):
    puskesmas = models.ForeignKey(Puskesmas, on_delete=models.CASCADE,
                                    related_name="puskesmas")
    user_link = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="user_link", null=True)
    nama = models.CharField(max_length=60)
    alamat = models.TextField()
    no_ktp = models.CharField(max_length=30)
    no_hp = models.CharField(max_length=17)
    email = models.EmailField()

    def __str__(self):
        return "{}-{}".format(self.nama, self.puskesmas.nama)


# Data Pemeriksaan Pasien
class DataPemeriksaan(models.Model):
    petugas_puskesmas = models.ForeignKey(PetugasPuskesmas, on_delete=models.CASCADE)
    file_excel = models.FileField(upload_to = 'file_excel_import', unique=True)
    imported_file = models.BooleanField(default=False)
    tanggal_upload = models.DateTimeField(auto_now_add=True, auto_now=False)
    tanggal_revisi = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.file_excel.name.split("/")[-1]

    def get_absolute_url(self):
        return reverse('puskesmas_app:data-pemeriksaan-detail',
                       kwargs={'pk': self.pk})
    def get_absolute_url_delete(self):
        return reverse('puskesmas_app:data-pemeriksaan-delete',
                        kwargs={'pk': self.pk})

# Pasien
class Pasien(models.Model):
    
    no_bpjs             = models.CharField(max_length=30, null=True)
    no_ktp              = models.CharField(max_length=30, unique=False)
    nama_pasien         = models.CharField(max_length=200)
    nama_panggilan      = models.CharField(max_length=200)
    tanggal_lahir       = models.DateField(null=True)
    
    from .static_var import (
        JENIS_KELAMIN, AGAMA, PENDIDIKAN_TERAKHIR,
        PEKERJAAN, STATUS
        )
        
    gender              = models.CharField(max_length=20, choices=JENIS_KELAMIN, default='TJ')
    agama               = models.CharField(max_length=20, choices=AGAMA, null=True)
    alamat              = models.TextField()
    no_hp               = models.CharField(max_length=20, null=True)
    pendidikan_terakhir = models.CharField(max_length=20, choices=PENDIDIKAN_TERAKHIR)
    pekerjaan           = models.CharField(max_length=30, choices=PEKERJAAN)
    status              = models.CharField(max_length=20, choices=STATUS)
    golongan_darah      = models.CharField(max_length=2, null=True)
    email               = models.EmailField(null=True)
    migrasi_dari_excel  = models.BooleanField(default=False)
    # dari_file           = models.CharField(max_length=300, null=True)
    dari_file           = models.ForeignKey(DataPemeriksaan, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{} - {}".format(self.nama_pasien, self.no_ktp)

class Resep(models.Model):
    nama_obat = models.CharField(max_length=50)
    jenis_obat = models.CharField(max_length=50)
    keterangan = models.CharField(max_length=50)

class Pembayaran(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE)
    tarif_dokter = models.IntegerField()
    harga_obat = models.IntegerField()
    total_harga = models.IntegerField()

class Pendaftaran(models.Model):
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    poli = models.ForeignKey(Poliklinik, on_delete=models.CASCADE)
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE)
    tanggal_daftar = models.DateTimeField()
    keluhan = models.TextField()

class Rekam_medis(models.Model):
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE)
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE)
    tanggal_periksa = models.DateTimeField()
    pemeriksaan = models.CharField(max_length=200)
    diagnosa = models.TextField()

# database asli
class Pemeriksaan(models.Model):
    dari_file = models.ForeignKey(DataPemeriksaan, on_delete=models.CASCADE)
    migrasi_dari_excel = models.BooleanField(default=False)
    tanggal = models.DateField(null=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, null=True)

    # Riwayat penyakit Tidak Menular Pada Keluarga
    diabetes_keluarga = models.NullBooleanField()
    hipertensi_keluarga = models.NullBooleanField()
    penyakit_jantung_keluarga = models.NullBooleanField()
    stroke_keluarga = models.NullBooleanField()
    asma_keluarga = models.NullBooleanField()
    kanker_keluarga = models.NullBooleanField()
    kolestrol_tinggi_keluarga = models.NullBooleanField()

    # Riwayat penyakit Tidak Menular Pada Diri Sendiri
    diabetes_diri = models.NullBooleanField()
    hipertensi_diri = models.NullBooleanField()
    penyakit_jantung_diri = models.NullBooleanField()
    stroke_diri = models.NullBooleanField()
    asma_diri = models.NullBooleanField()
    kanker_diri = models.NullBooleanField()
    kolestrol_tinggi_diri = models.NullBooleanField()

    # wawancara pada pasien
    merokok = models.NullBooleanField()
    kurang_aktifitas_fisik = models.NullBooleanField()
    kurang_sayur_dan_buah = models.NullBooleanField()
    konsumsi_alkohol = models.NullBooleanField()

    # Tekanan Darah Pada Pasien
    sistol = models.IntegerField(null=True)
    diastol = models.IntegerField(null=True)

    # Indeks Masa Tubuh
    tinggi_badan = models.IntegerField(null=True)
    berat_badan = models.IntegerField(null=True)

    lingkar_perut = models.IntegerField(null=True)
    
    from .static_var import PENGUKURAN_FUNGSI_PARU
    
    pengukuran_fungsi_paru = models.CharField(max_length=10, choices=PENGUKURAN_FUNGSI_PARU, null=True)

    from .static_var import BENJOLAN_PAYUDARA_CHOICES, IVA_CHOICES

    # pemeriksaan lab pada pasien
    gula = models.IntegerField(null=True)
    kolestrol = models.IntegerField(null=True)
    trigliserida = models.IntegerField(null=True)
    benjolan_payudara = models.NullBooleanField(choices=BENJOLAN_PAYUDARA_CHOICES)
    # iva = models.CharField(max_length=10, null=True)
    iva = models.NullBooleanField(choices=IVA_CHOICES)
    kadar_alkohol_pernapasan = models.NullBooleanField(choices=IVA_CHOICES)
    tes_amfetamin_urin = models.NullBooleanField(choices=IVA_CHOICES)

    from .static_var import PENYULUHAN_CHOICES
    
    # penyuluhan
    penyuluhan_iva_and_cbe = models.NullBooleanField(choices=PENYULUHAN_CHOICES)
    penyuluhan_rokok = models.NullBooleanField(choices=PENYULUHAN_CHOICES)
    penyuluhan_potensi_cedera = models.NullBooleanField(choices=PENYULUHAN_CHOICES)

    # tambahan
    
    from .static_var import NORMAL_ABNORMAL
    
    tajam_penglihatan = models.CharField(max_length=9, choices=NORMAL_ABNORMAL, null=True)
    tajam_pendengaran = models.CharField(max_length=9, choices=NORMAL_ABNORMAL, null=True)
    gangguan_mental_emosional = models.NullBooleanField()
    
    def __str__(self):
        return "{}, {}".format(self.tanggal, self.pasien.nama_pasien)

    def get_jumlah_yang_di_periksa(self):
        return Pemeriksaan.objects.count()

    def get_jumlah_yang_diperiksa_merokok(self):
        return Pemeriksaan.get_jumlah_yang_di_periksa() - Pemeriksaan.objects.filter(merokok=None).count()

    def get_jumlah_yang_diperiksa_kurang_aktifitas_fisik(self):
        return Pemeriksaan.get_jumlah_yang_di_periksa() - Pemeriksaan.objects.filter(kurang_aktifitas_fisik=None).count()




# user petugas dinas kota
class PetugasDinasKota(models.Model):
    nama_dinas = models.CharField(max_length=40)
    alamat_dinas = models.TextField()
    no_hp = models.CharField(max_length=17)


# Demografi Penduduk
class DemografiPenduduk(models.Model):
    YEAR_CHOICES = []
    for r in range(2015, (timezone.now().date().year) + 1):
        YEAR_CHOICES.append((r, r))
    YEAR_CHOICES = tuple(YEAR_CHOICES)

    tahun = models.PositiveIntegerField(
            validators=[
            MinValueValidator(2015),
            MaxValueValidator(timezone.now().date().year)],
            help_text="Gunakan Format Tahun: <YYYY>",
            choices= YEAR_CHOICES,
            )

    u15_19_laki_laki = models.IntegerField()
    u15_19_perempuan = models.IntegerField()

    u20_44_laki_laki = models.IntegerField()
    u20_44_perempuan = models.IntegerField()

    u45_54_laki_laki = models.IntegerField()
    u45_54_perempuan = models.IntegerField()

    u30_50_perempuan = models.IntegerField()

    u55_59_laki_laki = models.IntegerField()
    u55_59_perempuan = models.IntegerField()

    u60_69_laki_laki = models.IntegerField()
    u60_69_perempuan = models.IntegerField()

    u70_lebih_laki_laki = models.IntegerField()
    u70_lebih_perempuan = models.IntegerField()


