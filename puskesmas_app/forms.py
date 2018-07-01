from django.forms import ModelForm
from django import forms
from . models import DataPemeriksaan

class DataPemeriksaanForm(ModelForm):
    class Meta:
        model = DataPemeriksaan
        fields = ('petugas_puskesmas', 'file_excel',)

class ImportFileExcelForm(forms.Form):
    berkas = forms.ModelChoiceField(queryset=DataPemeriksaan.objects.filter(imported_file=False))
    jumlah_data = forms.IntegerField(required=False)
