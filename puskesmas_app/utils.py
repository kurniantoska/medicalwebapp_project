
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from datetime import datetime

from .models import DataPemeriksaan

import pandas as pd
import pytz
import numpy as np

from puskesmas_app.models import Pasien, Pemeriksaan, DataPemeriksaan


def ubah_timestamp_ke_tanggal(var_timestamp):
    timestamp_str = str(var_timestamp)
    timestamp_int = int(timestamp_str[:9])
    return datetime.fromtimestamp(timestamp_int)
    
def ubah_timestamp_ke_tgl_periksa(var_timestamp):
    timestamp_str = str(var_timestamp)
    timestamp_int = int(timestamp_str[:10])
    return datetime.fromtimestamp(timestamp_int)

class EksekusiImportBerkasExcelPasien():
    """untuk melakukan import data dimulai dengan mengisi berkas \n
    from puskesmas_app.models import Pasien, Pemeriksaan, DataPemeriksaan
    from puskesmas_app.utils import EksekusiImportBerkasExcelPasien
    eksekusi1 = EksekusiImportBerkasExcelPasien()
    eksekusi1.data_import = DataPemeriksaan.objects.get(file_excel__iexact='x.xlsx')
    eksekusi1.berkas = eksekusi1.data_import.file_excel.path
    import_stage_1 = eksekusi1.baca_data_file_excel()
    import_stage_2 = eksekusi1.data_pasien_tuple_list()
    import_stage_3 = eksekusi1.parsing_data_pasien()
    pasien, dup, berhasil = eksekusi1.data_duplikasi_cek_dan_import()
    """
    berkas = None
    baris_awal = 9
    jumlah_data = 5
    kolom_awal = 'B'
    kolom_akhir = 'AX'
    data_import = None


    def make_to_real_none(self, data):
        if data == 'None' or data == 'nan' or data == 'Nan':
            data = None
        return data


    def baca_data_file_excel(self):
        """Baca data pemeriksaan dari file excel dengan nilai yang ada dari
        db DataPemeriksaan.file_excel.path
        nilai return yaitu: berupa dataframe pandas dari file excel.
        """
        berkas = self.berkas
        baris_awal = self.baris_awal
        kolom_awal = self.kolom_awal
        kolom_akhir = self.kolom_akhir

        isi_parse = "{}:{}".format(kolom_awal, kolom_akhir)
        data_frame_proses = pd.DataFrame(['kosong'])

        try:
            # pandas current
            data_frame_proses = pd.read_excel(berkas, skiprows=baris_awal-1,
                                              header=None, usecols=isi_parse)
            # pandas old 20.3
            # data_frame_proses = pd.read_excel(berkas, skiprows=baris_awal-1,
            #                                   header=None, parse_cols=isi_parse)
            data_frame_proses.replace(np.nan, 'None', inplace=True)
            data_frame_proses.replace("'", "", inplace=True)
        except FileNotFoundError:
            print('Berkas Gak Ketemu coba lagi!')
        return data_frame_proses

    def baca_data_pemeriksaan_pasien(self):
        """melakukan pembacaan data untuk rekam medis pasien
        lakukan perubahan """

    def data_pasien_tuple_list(self):
        """input pandas data frame dengan var 'data_proses'
        dan return tuple pasien_list"""
        data_proses = self.baca_data_file_excel()
        pasien_list = []
        # seleksi data pasien sehingga tidak ada duplikasi dengan acuan no ktp.
        for n in range(self.jumlah_data):
            pasien_list.append(data_proses.loc[n, 2:16].tolist())
        return tuple(pasien_list)

    def parsing_data_pasien(self):
        import_data_stage2 = self.data_pasien_tuple_list()
        jumlah_data = self.jumlah_data
        local_tz = pytz.timezone("Asia/Makassar", )
        data_per_baris = []
        for i in range(jumlah_data):
            try:
                value_tanggal_lahir = import_data_stage2[i][3].date()
            except:
                tanggal_lahir = import_data_stage2[i][3]
                if type(tanggal_lahir) == type(1) :
                    value_tanggal_lahir = ubah_timestamp_ke_tanggal(tanggal_lahir)
                else :
                    value_tanggal_lahir = None
            
            baris = {
                'no_ktp': import_data_stage2[i][0],
                'nama_pasien': import_data_stage2[i][1],
                'nama_panggilan': import_data_stage2[i][2],
                'tanggal_lahir': value_tanggal_lahir,
                'jenis_kelamin': import_data_stage2[i][4],
                'agama': import_data_stage2[i][5],
                'alamat': import_data_stage2[i][6],
                'no_hp': import_data_stage2[i][7],
                'pendidikan_terakhir': import_data_stage2[i][8],
                'pekerjaan': import_data_stage2[i][9],
                'status': import_data_stage2[i][10],
                'golongan_darah': import_data_stage2[i][11],
                'email': import_data_stage2[i][12],
                'migrasi_dari_excel': True,
            }
            data_per_baris.append(baris)
        return data_per_baris

    def data_duplikasi_cek_dan_import(self):
        data_import = self.data_import
        import_stage_3 = self.parsing_data_pasien()
        status_data_duplikat = 0
        status_data_berhasil_import = 0

        # modif 1
        object_pasien = []
        for i in range(len(import_stage_3)):
            # x = None // asli
            # try:
            #     nilai_tanggal_lahir = import_stage_3[i]['tanggal_lahir'].date()
            # except:
            #     nilai_tanggal_lahir = None
            nilai_tanggal_lahir = import_stage_3[i]['tanggal_lahir']
            
            try :
                temp= Pasien.objects.get_or_create(
                no_ktp = (import_stage_3[i]['no_ktp']),
                nama_pasien= import_stage_3[i]['nama_pasien'],
                nama_panggilan = import_stage_3[i]['nama_panggilan'],
                tanggal_lahir = nilai_tanggal_lahir,
                gender = import_stage_3[i]['jenis_kelamin'],
                agama = self.make_to_real_none(import_stage_3[i]['agama']),
                alamat = import_stage_3[i]['alamat'],
                no_hp = import_stage_3[i]['no_hp'],
                pendidikan_terakhir = import_stage_3[i]['pendidikan_terakhir'],
                pekerjaan = import_stage_3[i]['pekerjaan'],
                status = import_stage_3[i]['status'],
                golongan_darah = self.make_to_real_none(import_stage_3[i]['golongan_darah']),
                email = import_stage_3[i]['email'],
                migrasi_dari_excel = True,
                )
            except MultipleObjectsReturned :
                temp= Pasien.objects.filter(
                    no_ktp = import_stage_3[i]['no_ktp'],
                    nama_pasien= import_stage_3[i]['nama_pasien'],
                    nama_panggilan = import_stage_3[i]['nama_panggilan'],
                    tanggal_lahir = nilai_tanggal_lahir,
                    gender = import_stage_3[i]['jenis_kelamin'],
                    agama = self.make_to_real_none(import_stage_3[i]['agama']),
                    alamat = import_stage_3[i]['alamat'],
                    no_hp = import_stage_3[i]['no_hp'],
                    pendidikan_terakhir = import_stage_3[i]['pendidikan_terakhir'],
                    pekerjaan = import_stage_3[i]['pekerjaan'],
                    status = import_stage_3[i]['status'],
                    golongan_darah = self.make_to_real_none(import_stage_3[i]['golongan_darah']),
                    email = import_stage_3[i]['email'],
                    migrasi_dari_excel = True,
                ).first()
                
            object_pasien.append(temp)
            try :
                if temp[1] :
                    status_data_berhasil_import += 1
                    temp[0].dari_file = data_import
                    temp[0].save()
                else :
                    status_data_duplikat += 1
            except:
                status_data_duplikat += 1

        # if status_data_duplikat + status_data_berhasil_import == self.jumlah_data:
        #     self.data_import.imported_file = True
        #     self.data_import.save()
        return object_pasien, status_data_duplikat, status_data_berhasil_import


    def data_rekam_medis(self):
        """var 'data' diisi dengan dataframe lengkap
        sementara itu 'jumlah_data' diisi dengan
        banyaknya data yang akan diproses
        baris_awal  = ...
        jumlah_data = ...
        kolom_awal  = ...
        kolom_akhir = ...
        lakukan ekseternal dengan meassign object baru
        untuk keperluan data rekam medis disamping data pasien.
        """

        data = self.baca_data_file_excel()
        jumlah_data = self.jumlah_data

        data_tanggal = data.loc[:jumlah_data - 1, 1]
        data_attr = data.loc[:jumlah_data - 1, 14:]
        complete_data_pemeriksaan = pd.concat([data_tanggal, data_attr], axis=1)
        # complete_data_pemeriksaan[0] = 
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Tidak'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Ya'] = 'True'
        
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'TIDAK'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'YA'] = 'True'
        
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'tidak'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'ya'] = 'True'

        complete_data_pemeriksaan[complete_data_pemeriksaan == 'tidak Ikut'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'ikut'] = 'True'
        
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Tidak Ikut'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Ikut'] = 'True'

        complete_data_pemeriksaan[complete_data_pemeriksaan == 'negatif'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'positif'] = 'True'

        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Negatif'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Positif'] = 'True'
        
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'tidak Ditemukan'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'ditemukan'] = 'True'


        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Tidak Ditemukan'] = 'False'
        complete_data_pemeriksaan[complete_data_pemeriksaan == 'Ditemukan'] = 'True'
        complete_data_pemeriksaan.replace(np.nan, 'None', inplace=True)

        # return data as dictionary
        return complete_data_pemeriksaan

    def parsing_data_pemeriksaan(self):
        pass
        # rekam_medis_stage1 = self.data_rekam_medis()
        # rekam_medis_dictionary = {}
        # for data in rekam_medis_stage1[1]:
        #


    def insert_data_pemeriksaan_ke_database(self, pasien= None):
        rekam_medis_stage1 = self.data_rekam_medis()
        """pasien, dup, berhasil = eksekusi1.data_duplikasi_cek_dan_import()"""
        object_pemeriksaan = []
        status_data_berhasil_import = 0
        status_data_duplikat = 0

        for i in range(len(rekam_medis_stage1)):
            # x = None // asli
            try:
                nilai_tanggal_pemeriksaan = rekam_medis_stage1[1][i].date()
            except:
                # cek apakah tanggal bernilai dalam bentuk timestamp
                if type(rekam_medis_stage1[1][i]) == type(1) or type(rekam_medis_stage1[1][i]) == type(np.int64(1)) :
                    nilai_tanggal_pemeriksaan = ubah_timestamp_ke_tgl_periksa(rekam_medis_stage1[1][i])
                else :
                    nilai_tanggal_pemeriksaan = None
            
            try : 
                nilai_pasien = pasien[i][0]
            except TypeError:
                nilai_pasien = pasien[i]

            temp = Pemeriksaan.objects.get_or_create(
                dari_file=self.data_import,
                migrasi_dari_excel=True,
                tanggal= nilai_tanggal_pemeriksaan,
                pasien = nilai_pasien,
                
                # Riwayat penyakit Tidak Menular Pada Keluarga
                diabetes_keluarga= self.make_to_real_none(rekam_medis_stage1[15][i]),
                hipertensi_keluarga= self.make_to_real_none(rekam_medis_stage1[16][i]),
                penyakit_jantung_keluarga= self.make_to_real_none(rekam_medis_stage1[17][i]),
                stroke_keluarga= self.make_to_real_none(rekam_medis_stage1[18][i]),
                asma_keluarga= self.make_to_real_none(rekam_medis_stage1[19][i]),
                kanker_keluarga= self.make_to_real_none(rekam_medis_stage1[20][i]),
                kolestrol_tinggi_keluarga = self.make_to_real_none(rekam_medis_stage1[21][i]),

                # Riwayat penyakit Tidak Menular Pada Diri Sendiri
                diabetes_diri= self.make_to_real_none(rekam_medis_stage1[22][i]),
                hipertensi_diri= self.make_to_real_none(rekam_medis_stage1[23][i]),
                penyakit_jantung_diri= self.make_to_real_none(rekam_medis_stage1[24][i]),
                stroke_diri= self.make_to_real_none(rekam_medis_stage1[25][i]),
                asma_diri= self.make_to_real_none(rekam_medis_stage1[26][i]),
                kanker_diri= self.make_to_real_none(rekam_medis_stage1[27][i]),
                kolestrol_tinggi_diri= self.make_to_real_none(rekam_medis_stage1[28][i]),

                # wawancara pada pasien
                merokok= self.make_to_real_none(rekam_medis_stage1[29][i]),
                kurang_aktifitas_fisik= self.make_to_real_none(rekam_medis_stage1[30][i]),
                kurang_sayur_dan_buah= self.make_to_real_none(rekam_medis_stage1[31][i]),
                konsumsi_alkohol= self.make_to_real_none(rekam_medis_stage1[32][i]),

                # Tekanan Darah Pada Pasien
                sistol= self.make_to_real_none(rekam_medis_stage1[33][i]),
                diastol= self.make_to_real_none(rekam_medis_stage1[34][i]),

                # Indeks Masa Tubuh
                tinggi_badan= self.make_to_real_none(rekam_medis_stage1[35][i]),
                berat_badan= self.make_to_real_none(rekam_medis_stage1[36][i]),

                lingkar_perut= self.make_to_real_none(rekam_medis_stage1[37][i]),
                pengukuran_fungsi_paru= self.make_to_real_none(rekam_medis_stage1[38][i]),

                # pemeriksaan lab pada pasien
                gula= self.make_to_real_none(rekam_medis_stage1[39][i]),
                kolestrol= self.make_to_real_none(rekam_medis_stage1[40][i]),
                trigliserida= self.make_to_real_none(rekam_medis_stage1[41][i]),
                benjolan_payudara= self.make_to_real_none(rekam_medis_stage1[42][i]),
                iva= self.make_to_real_none(rekam_medis_stage1[43][i]),
                kadar_alkohol_pernapasan= self.make_to_real_none(rekam_medis_stage1[44][i]),
                tes_amfetamin_urin= self.make_to_real_none(rekam_medis_stage1[45][i]),

                # penyuluhan
                penyuluhan_iva_and_cbe= self.make_to_real_none(rekam_medis_stage1[46][i]),
                penyuluhan_rokok= self.make_to_real_none(rekam_medis_stage1[47][i]),
                penyuluhan_potensi_cedera= self.make_to_real_none(rekam_medis_stage1[48][i]),
                )

            object_pemeriksaan.append(temp)
            if temp[1]:
                status_data_berhasil_import += 1
            else:
                status_data_duplikat += 1

        if status_data_duplikat + status_data_berhasil_import == self.jumlah_data:
            self.data_import.imported_file = True
            self.data_import.save()
        return object_pemeriksaan, status_data_duplikat, status_data_berhasil_import


def group_check(user):
    return user.groups.filter(name__in=['puskesmas',])
    
    





