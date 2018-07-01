from django.contrib import admin

from . models import (
    Dokter, Jadwal_Dokter, Poliklinik, Pasien,
    Resep, Pembayaran, Pendaftaran, Rekam_medis,
    Pemeriksaan, Person, Puskesmas, PetugasPuskesmas,
    DataPemeriksaan, DemografiPenduduk
)

@admin.register(DemografiPenduduk)
class DemografiPendudukAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DemografiPenduduk._meta.get_fields()]

@admin.register(Puskesmas)
class PuskesmasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat')

@admin.register(PetugasPuskesmas)
class PetugasPuskesmasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'alamat', 'puskesmas','no_ktp', 'no_hp', 'email')

@admin.register(DataPemeriksaan)
class DataPemeriksaanAdmin(admin.ModelAdmin):
    list_display = ('file_excel', 'imported_file',
                    'tanggal_upload','tanggal_revisi',
                    )
    # list_display = [field.name for field in DataPemeriksaan._meta.get_fields()]


class PemeriksaanInline(admin.TabularInline):
    model = Pemeriksaan


@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    
    list_filter = ('dari_file',)
    search_fields = ('nama_pasien', 'nama_panggilan')
    inlines = [
        PemeriksaanInline,
    ]
    list_display = ('nama_pasien', 'gender', 'no_hp',
                    'pekerjaan', 'tanggal_lahir', 'dari_file')


@admin.register(Pemeriksaan)
class PemeriksaanAdmin(admin.ModelAdmin):
    # list_display = ('tanggal', 'pasien', 'dari_file',
    #                 'migrasi_dari_excel')
    actions_on_top = True
    list_display = [field.name for field in Pemeriksaan._meta.get_fields()]
    list_filter = ('dari_file',)




