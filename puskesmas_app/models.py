from django.db import models
from django.db.models import Count
from django.db.models import Q
from django.db.models.functions import TruncYear, TruncMonth

# from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.core.validators import (
    MinValueValidator, MaxValueValidator
)

from django.utils import timezone

from dateutil.relativedelta import relativedelta

from calendar import day_name
from django.contrib.auth.models import User

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


from .static_var import KELURAHAN_DI_SURABAYA
from .static_var import KECAMATAN_DI_SURABAYA

# puskesmas
class Puskesmas(models.Model):
    nama = models.CharField(max_length=60)
    kecamatan = models.CharField(max_length=50, choices = KECAMATAN_DI_SURABAYA, null=True, blank=True)
    kelurahan = models.CharField(max_length=50, choices = KELURAHAN_DI_SURABAYA, null=True, blank=True)
    alamat = models.TextField()

    def __str__(self):
        return self.nama


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
    file_excel = models.FileField(upload_to= 'file_excel_import', unique=True)
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
        
    def get_umur(self):
        if self.tanggal_lahir:
            return relativedelta(timezone.now().date(), self.tanggal_lahir).years
        else:
            return None


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

# manager untuk class pemeriksaan
# class MerokokManajer(models.Manager):
#     def get_queryset(self):
#         jumlah_yang_merokok = super().get_queryset().filter(merokok=True)
#         return super().get_queryset().filter(merokok=True)


# database asli
class Pemeriksaan(models.Model):

    LIST_OF_MONTHS = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    dari_file = models.ForeignKey(DataPemeriksaan, on_delete=models.CASCADE)
    migrasi_dari_excel = models.BooleanField(default=False)
    tanggal = models.DateField(null=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, null=True)
    umur = models.IntegerField(null=True)

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

    # ext
    indeks_masa_tubuh = models.FloatField(null=True)
    
    # tambahan
    
    from .static_var import NORMAL_ABNORMAL
    
    tajam_penglihatan = models.CharField(max_length=9, choices=NORMAL_ABNORMAL, null=True)
    tajam_pendengaran = models.CharField(max_length=9, choices=NORMAL_ABNORMAL, null=True)
    gangguan_mental_emosional = models.NullBooleanField()
    
    def __str__(self):
        return "{}, {}".format(self.tanggal, self.pasien.nama_pasien)

    # only for a_list = ['merokok', 'kurang_aktifitas_fisik', 
    # 'kurang_sayur_dan_buah', 'konsumsi_alkohol', 
    # 'benjolan_payudara', 'iva',]
    @staticmethod
    def qs_model_rekapitulasi(tahun:int, item:str, kecamatan:str = None):
        if kecamatan :
            qs = Pemeriksaan.objects.filter(
                tanggal__year=tahun,
                dari_file__petugas_puskesmas__puskesmas__kecamatan = kecamatan
                )
        else:
            qs = Pemeriksaan.objects.filter(tanggal__year=tahun)
        
        data = qs.aggregate(
            # menggunakan parameter distinct untuk menghilangkan duplikasi
            p_true=Count('pasien', filter=Q(**{item: True}), distinct=True),
            p_false=Count('pasien', filter=Q(**{item: False}), distinct=True),
            p_none=Count('pasien', filter=Q(**{item: None}), distinct=True),
            )
        return (data['p_true'] or 0, 
                data['p_false'] or 0,
                data['p_none'] or 0,
                )
    
    @staticmethod
    def get_jumlah_beresiko_dan_diperiksa(tahun:int, item:str, kecamatan:str=None):
        """mendapatkan jumlah pemeriksaan dari item untuk keperluan 
        output pada halaman rekapitulasi_fr
        dengan return (jumlah_beresiko, jumlah_yang_diperiksa)"""
        if kecamatan :
            qs = Pemeriksaan.objects.filter(
                tanggal__year=tahun,
                dari_file__petugas_puskesmas__puskesmas__kecamatan=kecamatan
                )
        else:
            qs = Pemeriksaan.objects.filter(tanggal__year=tahun)
        
        if item == 'tekanandarah' :
            data = qs.aggregate(
                p_true=Count('pasien', filter=Q(sistol__gt=140), distinct=True),
                p_false=Count('pasien', filter=Q(sistol__lte=140), distinct=True),
                p_none=Count('pasien', filter=Q(sistol=None), distinct=True),
            )
            _ = (data['p_true'] or 0,
                 data['p_false'] or 0,
                 data['p_none'] or 0,)
        
        elif item == 'asamurat' :
            data = qs.aggregate(
                p_true=Count('pasien', filter=Q(trigliserida__gt=7), distinct=True),
                p_false=Count('pasien', filter=Q(trigliserida__lte=7), distinct=True),
                p_none=Count('pasien', filter=Q(trigliserida=None), distinct=True),
            )
            
            _ = (data['p_true'] or 0, 
                data['p_false'] or 0, 
                data['p_none'] or 0,)
        
        elif item == 'gula' :
            data = qs.aggregate(
                p_true=Count('pasien', filter=Q(gula__lt=80) | Q(gula__gt=144), distinct=True),
                p_false=Count('pasien', filter=Q(gula__gt=80, gula__lt=144), distinct=True),
                p_none=Count('pasien', filter=Q(gula=None), distinct=True),
            )
            
            _ = (data['p_true'] or 0,
                 data['p_false'] or 0,
                 data['p_none'] or 0,)
        
        elif item == 'amfetamin_urin':
            _ = (0, 0)
        
        elif item == 'kolestrol' :
            data = qs.aggregate(
                p_true=Count('pasien', filter=Q(kolestrol__gt=200), distinct=True),
                p_false=Count('pasien', filter=Q(kolestrol__lte=200), distinct=True),
                p_none=Count('pasien', filter=Q(sistol=None), distinct=True),
            )
            
            _ = (data['p_true'] or 0, 
                data['p_false'] or 0, 
                data['p_none'] or 0,)
        
        elif item == 'imt' :
            data = qs.aggregate(
                p_true=Count('pasien', filter=Q(indeks_masa_tubuh__gt=25), distinct=True),
                p_false=Count('pasien', filter=Q(indeks_masa_tubuh__lte=25), distinct=True),
                p_none=Count('pasien', filter=Q(indeks_masa_tubuh=None), distinct=True),
            )
            _ = (data['p_true'] or 0,
                 data['p_false'] or 0,
                 data['p_none'] or 0,)
        
        elif item == 'lingkar_perut' :
            data = qs.aggregate(
                p_true=Count('pasien', filter=Q(lingkar_perut__gt=90), distinct=True),
                p_false=Count('pasien', filter=Q(lingkar_perut__lte=90), distinct=True),
                p_none=Count('pasien', filter=Q(lingkar_perut=None), distinct=True),
            )
            _ = (data['p_true'] or 0,
                 data['p_false'] or 0,
                 data['p_none'] or 0,)
        
        else:
            _ = Pemeriksaan.qs_model_rekapitulasi(tahun, item)
        
        jumlah_beresiko = _[0]
        jumlah_yang_diperiksa = _[0] + _[1]
        return jumlah_beresiko, jumlah_yang_diperiksa

    @staticmethod
    def get_month_str(index):
        return Pemeriksaan.LIST_OF_MONTHS[index-1]

    @staticmethod
    def get_data_analisa_grafik(qs, item, loop, extra):
        
        jumlah_ya = []
        jumlah_tidak = []
        total_ya = []
        total_tidak = []

        for i in range(0, loop):
            
            if len(extra) > 0:
                fs = qs.filter(**extra[i])
            else:
                fs = qs
            
            if item == 'tekanandarah':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(sistol__gt=140), distinct=True),
                    p_false=Count('pasien', filter=Q(sistol__lte=140), distinct=True),
                    p_none=Count('pasien', filter=Q(sistol=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            elif item == 'trigliserida':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(trigliserida__gt=7), distinct=True),
                    p_false=Count('pasien', filter=Q(trigliserida__lte=7), distinct=True),
                    p_none=Count('pasien', filter=Q(trigliserida=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            elif item == 'gula':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(gula__lt=80) | Q(gula__gt=144), distinct=True),
                    p_false=Count('pasien', filter=Q(gula__gt=80, gula__lt=144), distinct=True),
                    p_none=Count('pasien', filter=Q(gula=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            elif item == 'kolestrol':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(kolestrol__gt=200), distinct=True),
                    p_false=Count('pasien', filter=Q(kolestrol__lte=200), distinct=True),
                    p_none=Count('pasien', filter=Q(kolestrol=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            elif item == 'indeks_masa_tubuh':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(indeks_masa_tubuh__gt=25), distinct=True),
                    p_false=Count('pasien', filter=Q(indeks_masa_tubuh__lte=25), distinct=True),
                    p_none=Count('pasien', filter=Q(indeks_masa_tubuh=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            elif item == 'lingkar_perut':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(lingkar_perut__gt=90), distinct=True),
                    p_false=Count('pasien', filter=Q(lingkar_perut__lte=90), distinct=True),
                    p_none=Count('pasien', filter=Q(lingkar_perut=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            elif item == 'pengukuran_fungsi_paru':
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(pengukuran_fungsi_paru='Normal'), distinct=True),
                    p_false=Count('pasien', filter=Q(pengukuran_fungsi_paru='Buruk'), distinct=True),
                    p_none=Count('pasien', filter=Q(pengukuran_fungsi_paru=None), distinct=True),
                )
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)
                
            else:
                data = fs.aggregate(
                    p_true=Count('pasien', filter=Q(**{item: True}), distinct=True),
                    p_false=Count('pasien', filter=Q(**{item: False}), distinct=True),
                    p_none=Count('pasien', filter=Q(**{item: None}), distinct=True),
                )
                
                _ = (data['p_true'] or 0,
                     data['p_false'] or 0,
                     data['p_none'] or 0,)

            jumlah_pasien = _[0] + _[1]

            if _[0] == 0:
                hasil_ya = 0
            else:
                percent = (_[0]/jumlah_pasien) * 100.0
                hasil_ya = percent

            if _[1] == 0:
                hasil_tidak = 0
            else:
                percent = (_[1]/jumlah_pasien) * 100.0
                hasil_tidak = percent
            
            if _[0] == 0 and _[1] == 0:
                pass
            else:
                total_ya.append(hasil_ya)
                total_tidak.append(hasil_tidak)

            jumlah_ya.append(hasil_ya)
            jumlah_tidak.append(hasil_tidak)

        # tambah total
        jumlah_ya.append(sum(total_ya)/len(total_ya) if len(total_ya) > 0 else 0)
        jumlah_tidak.append(sum(total_tidak)/len(total_tidak) if len(total_tidak) > 0 else 0)
        return [jumlah_ya, jumlah_tidak, total_ya, total_tidak]

    @staticmethod
    def get_data_analisa_grafik_jenis_kelamin(qs, item, loop, extra):
    
        jumlah_laki = []
        jumlah_perempuan = []
        total_laki = []
        total_perempuan = []
    
        for i in range(0, loop):
        
            if len(extra) > 0:
                fs = qs.filter(**extra[i])
            else:
                fs = qs
        
            if item == 'tekanandarah':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(sistol__gt=140, pasien__gender__in=['L', 'l']), distinct=True),
                    p_true_p=Count('pasien', filter=Q(sistol__gt=140, pasien__gender__in=['P', 'p']), distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            elif item == 'trigliserida':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(trigliserida__gt=7, pasien__gender__in=['L', 'l']), distinct=True),
                    p_true_p=Count('pasien', filter=Q(trigliserida__gt=7, pasien__gender__in=['p', 'p']), distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            elif item == 'gula':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(gula__lt=80, pasien__gender__in=['L', 'l']) |
                                                    Q(gula__gt=144, pasien__gender__in=['L', 'l']), distinct=True),
                    p_true_p=Count('pasien', filter=Q(gula__lt=80, pasien__gender__in=['P', 'p']) |
                                                    Q(gula__gt=144, pasien__gender__in=['P', 'p']), distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            elif item == 'kolestrol':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(kolestrol__gt=200, pasien__gender__in=['L', 'l']), distinct=True),
                    p_true_p=Count('pasien', filter=Q(kolestrol__gt=200, pasien__gender__in=['P', 'p']), distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            elif item == 'indeks_masa_tubuh':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(indeks_masa_tubuh__gt=25, pasien__gender__in=['L', 'l']),
                                   distinct=True),
                    p_true_p=Count('pasien', filter=Q(indeks_masa_tubuh__gt=25, pasien__gender__in=['P', 'p']),
                                   distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            elif item == 'lingkar_perut':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(lingkar_perut__gt=90, pasien__gender__in=['L', 'l']),
                                   distinct=True),
                    p_true_p=Count('pasien', filter=Q(lingkar_perut__gt=90, pasien__gender__in=['P', 'p']),
                                   distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            elif item == 'pengukuran_fungsi_paru':
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(pengukuran_fungsi_paru='Normal', pasien__gender__in=['L', 'l']),
                                   distinct=True),
                    p_true_p=Count('pasien', filter=Q(pengukuran_fungsi_paru='Normal', pasien__gender__in=['P', 'p']),
                                   distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
        
            else:
                data = fs.aggregate(
                    p_true_l=Count('pasien', filter=Q(**{item: True}, pasien__gender__in=['L', 'l']), distinct=True),
                    p_true_p=Count('pasien', filter=Q(**{item: True}, pasien__gender__in=['P', 'p']), distinct=True),
                )
                _ = (
                    data['p_true_l'] or 0,
                    data['p_true_p'] or 0,
                )
                
            jumlah_pasien = _[0] + _[1]

            if _[0] == 0:
                hasil_ya = 0
            else:
                percent = (_[0] / jumlah_pasien) * 100.0
                hasil_ya = percent
                total_laki.append(percent)

            if _[1] == 0:
                hasil_tidak = 0
            else:
                percent = (_[1] / jumlah_pasien) * 100.0
                hasil_tidak = percent
                total_perempuan.append(percent)

            if _[0] == 0 and _[1] == 0:
                pass
            else:
                total_laki.append(hasil_ya)
                total_perempuan.append(hasil_tidak)

            jumlah_laki.append(hasil_ya)
            jumlah_perempuan.append(hasil_tidak)

        # tambah total
        jumlah_laki.append(sum(total_laki) / len(total_laki) if len(total_laki) > 0 else 0)
        jumlah_perempuan.append(sum(total_perempuan) / len(total_perempuan) if len(total_perempuan) > 0 else 0)
        return [jumlah_laki, jumlah_perempuan, total_laki, total_perempuan]

    # def save(self, *args, **kwargs):
    #     # Check how the current values differ from ._loaded_values. For example,
    #     # prevent changing the creator_id of the model. (This example doesn't
    #     # support cases where 'creator_id' is deferred).
    #     if not self._state.adding and (
    #             self.creator_id != self._loaded_values['creator_id']):
    #         raise ValueError("Updating the value of creator isn't allowed")
    #     super().save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        if (self.berat_badan is not None) and (self.tinggi_badan is not None):
            # self.first_char for referencing to the current object
            imt = (self.berat_badan / self.tinggi_badan**2) * 100**2
            imt = round(imt, 2)
            self.indeks_masa_tubuh = imt
        else :
            self.indeks_masa_tubuh = None
        
        if (self.pasien.tanggal_lahir is not None) and (self.tanggal is not None):
            umur = self.tanggal.year - self.pasien.tanggal_lahir.year
            self.umur = umur
        else :
            umur = None
        super().save(*args, **kwargs)
    

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
            choices= YEAR_CHOICES, unique=True
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


