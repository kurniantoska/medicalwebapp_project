from django.forms import ModelForm
from django import forms
from . models import DataPemeriksaan, DemografiPenduduk

class DataPemeriksaanForm(ModelForm):
    class Meta:
        model = DataPemeriksaan
        fields = ('petugas_puskesmas', 'file_excel',)

class ImportFileExcelForm(forms.Form):
    berkas = forms.ModelChoiceField(queryset=DataPemeriksaan.objects.filter(imported_file=False))
    jumlah_data = forms.IntegerField(required=False)

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