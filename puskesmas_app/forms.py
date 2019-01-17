from django.forms import ModelForm
from django import forms
from . models import DataPemeriksaan, DemografiPenduduk, Puskesmas


class DataPemeriksaanForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(DataPemeriksaanForm, self).__init__(*args, **kwargs)
        
        if not self.request.user.is_staff:
            del self.fields['petugas_puskesmas']

    class Meta:
        model = DataPemeriksaan
        fields = ('petugas_puskesmas','file_excel',)
        
        
class ImportFileExcelForm(forms.Form):
    berkas = forms.ModelChoiceField(queryset=DataPemeriksaan.objects.filter(imported_file=False))
    jumlah_data = forms.IntegerField(required=False)

    
class AnalisaTabelForm(forms.Form):
    PEMERIKSAAN_CHOICE = (
        ('merokok', 'Merokok'),  # boolean
        ('gula', 'Gula Darah'),  # input
        ('benjolan_payudara', 'Benjolan Payudara'),  # boolean
        ('indeks_masa_tubuh', 'Index Massa Tubuh'),  # input
        ('iva', 'IVA'),  # boolean
        ('kadar_alkohol_pernapasan', 'Alkohol dalam Pernapasan'),  # boolean
        ('kolestrol', 'Kolesterol'),  # input
        ('konsumsi_alkohol', 'Konsumsi Alkohol'),  # boolean
        ('kurang_aktifitas_fisik', 'Kurang Aktifitas'),  # boolean
        ('lingkar_perut', 'Lingkar Perut'),  # input
        ('pengukuran_fungsi_paru', 'Fungsi Paru Sederhana'),  # input
        ('kurang_sayur_dan_buah', 'Kurang Sayuran dan Buah'),  # boolean
        ('tes_amfetamin_urin', 'Amfetamin Urin'),  # boolean
        ('tekanandarah', 'Tekanan Darah'),  # input
        ('trigliserida', 'Trigliserida'),  # input
        ('penyuluhan_potensi_cedera', 'Penyuluhan Cedera'),  # boolean
        ('penyuluhan_rokok', 'Penyuluhan Rokok'),  # boolean
        ('penyuluhan_iva_and_cbe', 'Penyuluhan IVA'),  # boolean
        ('tajam_penglihatan', 'Tajam Penglihatan'),  # input
        ('tajam_pendengaran', 'Tajam Pendengaran'),  # input
        ('gangguan_mental_emosional', 'Gangguan Mental Emosional'),  # input
        
        ('diabetes_keluarga', 'Riwayat Diabetes Keluarga'),
        ('hipertensi_keluarga', 'Riwayat Hipertensi Keluarga'),
        ('penyakit_jantung_keluarga', 'Riwayat Penyakit Jantung Keluarga'),
        ('stroke_keluarga', 'Riwayat Stroke Keluarga'),
        ('asma_keluarga', 'Riwayat Asma Keluarga'),
        ('kanker_keluarga', 'Riwayat Kanker Keluarga'),
        ('kolestrol_tinggi_keluarga', 'Riwayat Kolesterol Keluarga'),
        
        ('diabetes_diri', 'Riwayat Diabetes Individu'),
        ('hipertensi_diri', 'Riwayat Hipertensi Individu'),
        ('penyakit_jantung_diri', 'Riwayat Penyakit Jantung Individu'),
        ('stroke_diri', 'Riwayat Stroke Individu'),
        ('asma_diri', 'Riwayat Asma Individu'),
        ('kanker_diri', 'Riwayat Kanker Individu'),
        ('kolestrol_tinggi_diri', 'Riwayat Kolesterol Individu'),
    )

    JENIS_CHOICE = (
        ('wilayah', 'Wilayah'),
        ('jenis_kelamin', 'Jenis Kelamin'),
        ('usia', 'Usia'),
        ('waktu', 'Waktu'),
    )
    puskesmas = forms.ModelChoiceField(queryset=Puskesmas.objects.all(), label="PUSKESMAS")
    dari = forms.CharField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    sd = forms.CharField(widget=forms.TextInput(attrs={'class': 'datepicker'}))
    jenis = forms.ChoiceField(choices=JENIS_CHOICE)
    pemeriksaan = forms.ChoiceField(choices=PEMERIKSAAN_CHOICE)
    
    
class AnalisaTabelDinasKotaForm(AnalisaTabelForm):
    def __init__(self, *args, **kwargs):
        super(AnalisaTabelDinasKotaForm, self).__init__(*args, **kwargs)
        self.fields.pop('puskesmas')
    

class DemografiPendudukForm(ModelForm):
    class Meta:
        model = DemografiPenduduk
        fields = '__all__'
        labels = {
            "u15_19_laki_laki": "LAKI-LAKI UMUR 15 - 19 TAHUN",
            "u15_19_perempuan": "PEREMPUAN UMUR 15 - 19 TAHUN",
            "u20_44_laki_laki" : "LAKI-LAKI UMUR 20 - 44 TAHUN",
            "u20_44_perempuan" : "PEREMPUAN UMUR 20 - 44 TAHUN",
            "u45_54_laki_laki" : "LAKI-LAKI UMUR 45- 54 TAHUN",
            "u45_54_perempuan" : "PEREMPUAN UMUR 45 - 54 TAHUN",
            "u30_50_perempuan" : "PEREMPUAN UMUR 30 - 50 TAHUN [PEMERIKSAAN IVA]",
            "u55_59_laki_laki" : "LAKI-LAKI UMUR 55 - 59 TAHUN",
            "u55_59_perempuan" : "PEREMPUAN UMUR 55 - 59 TAHUN",
            "u60_69_laki_laki" : "LAKI-LAKI UMUR 60 - 69 TAHUN",
            "u60_69_perempuan" : "PEREMPUAN UMUR 60 - 69 TAHUN",
            "u70_lebih_laki_laki" : "LAKI-LAKI UMUR LEBIH DARI 70 TAHUN",
            "u70_lebih_perempuan" : "PEREMPUAN UMUR LEBIH DARI 70 TAHUN",
        }
