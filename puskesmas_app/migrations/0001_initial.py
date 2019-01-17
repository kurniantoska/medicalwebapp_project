# Generated by Django 2.0.6 on 2019-01-17 01:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPemeriksaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_excel', models.FileField(unique=True, upload_to='file_excel_import')),
                ('imported_file', models.BooleanField(default=False)),
                ('tanggal_upload', models.DateTimeField(auto_now_add=True)),
                ('tanggal_revisi', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DemografiPenduduk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tahun', models.PositiveIntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019)], unique=True, validators=[django.core.validators.MinValueValidator(2015), django.core.validators.MaxValueValidator(2019)])),
                ('u15_19_laki_laki', models.IntegerField()),
                ('u15_19_perempuan', models.IntegerField()),
                ('u20_44_laki_laki', models.IntegerField()),
                ('u20_44_perempuan', models.IntegerField()),
                ('u45_54_laki_laki', models.IntegerField()),
                ('u45_54_perempuan', models.IntegerField()),
                ('u30_50_perempuan', models.IntegerField()),
                ('u55_59_laki_laki', models.IntegerField()),
                ('u55_59_perempuan', models.IntegerField()),
                ('u60_69_laki_laki', models.IntegerField()),
                ('u60_69_perempuan', models.IntegerField()),
                ('u70_lebih_laki_laki', models.IntegerField()),
                ('u70_lebih_perempuan', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Dokter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nip', models.CharField(max_length=20)),
                ('nama_dokter', models.CharField(max_length=200)),
                ('alamat', models.TextField()),
                ('no_hp', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Jadwal_Dokter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=1)),
                ('dokter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Dokter')),
            ],
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kecamatan', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Kelurahan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kelurahan', models.CharField(max_length=30)),
                ('kecamatan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Kecamatan')),
            ],
        ),
        migrations.CreateModel(
            name='Pasien',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_bpjs', models.CharField(max_length=30, null=True)),
                ('no_ktp', models.CharField(max_length=30)),
                ('nama_pasien', models.CharField(max_length=200)),
                ('nama_panggilan', models.CharField(max_length=200)),
                ('tanggal_lahir', models.DateField(null=True)),
                ('gender', models.CharField(choices=[('L', 'Laki-laki'), ('l', 'Laki-laki'), ('P', 'Perempuan'), ('p', 'Perempuan'), ('TJ', 'Gak Jelas')], default='TJ', max_length=20)),
                ('agama', models.CharField(choices=[('Islam', 'Islam'), ('Katolik', 'Katolik'), ('Protestan', 'Protestan'), ('Hindu', 'Hindu'), ('Budha', 'Budha'), ('Khonghucu', 'Khonghucu'), ('Kepercayaan', 'Kepercayaan')], max_length=20, null=True)),
                ('alamat', models.TextField()),
                ('no_hp', models.CharField(max_length=20, null=True)),
                ('pendidikan_terakhir', models.CharField(choices=[('Tidak Sekolah', 'Tidak Sekolah'), ('SD/SLTP', 'SD/SLTP'), ('SLTA', 'SLTA'), ('Diploma', 'Diploma'), ('Sarjana', 'Sarjana'), ('Pascasarjana', 'Pascasarjana')], max_length=20)),
                ('pekerjaan', models.CharField(choices=[('Staff Kantor', 'Staff Kantor'), ('IRT/Tidak Bekerja', 'IRT/Tidak Bekerja'), ('Petani', 'Petani'), ('Pedagang', 'Pedagang'), ('Nelayan', 'Nelayan'), ('Pendidikan', 'Pendidikan'), ('Pengemudi', 'Pengemudi'), ('Pensiunan', 'Pensiunan'), ('Lainnya', 'Lainnya')], max_length=30)),
                ('status', models.CharField(choices=[('Menikah', 'Menikah'), ('Belum', 'Belum'), ('Janda/Duda', 'Janda/Duda'), ('None', 'Gak Jelas')], max_length=20)),
                ('golongan_darah', models.CharField(max_length=2, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('migrasi_dari_excel', models.BooleanField(default=False)),
                ('dari_file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.DataPemeriksaan')),
            ],
        ),
        migrations.CreateModel(
            name='Pembayaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarif_dokter', models.IntegerField()),
                ('harga_obat', models.IntegerField()),
                ('total_harga', models.IntegerField()),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Pasien')),
            ],
        ),
        migrations.CreateModel(
            name='Pemeriksaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('migrasi_dari_excel', models.BooleanField(default=False)),
                ('tanggal', models.DateField(null=True)),
                ('umur', models.IntegerField(null=True)),
                ('diabetes_keluarga', models.NullBooleanField()),
                ('hipertensi_keluarga', models.NullBooleanField()),
                ('penyakit_jantung_keluarga', models.NullBooleanField()),
                ('stroke_keluarga', models.NullBooleanField()),
                ('asma_keluarga', models.NullBooleanField()),
                ('kanker_keluarga', models.NullBooleanField()),
                ('kolestrol_tinggi_keluarga', models.NullBooleanField()),
                ('diabetes_diri', models.NullBooleanField()),
                ('hipertensi_diri', models.NullBooleanField()),
                ('penyakit_jantung_diri', models.NullBooleanField()),
                ('stroke_diri', models.NullBooleanField()),
                ('asma_diri', models.NullBooleanField()),
                ('kanker_diri', models.NullBooleanField()),
                ('kolestrol_tinggi_diri', models.NullBooleanField()),
                ('merokok', models.NullBooleanField()),
                ('kurang_aktifitas_fisik', models.NullBooleanField()),
                ('kurang_sayur_dan_buah', models.NullBooleanField()),
                ('konsumsi_alkohol', models.NullBooleanField()),
                ('sistol', models.IntegerField(null=True)),
                ('diastol', models.IntegerField(null=True)),
                ('tinggi_badan', models.FloatField(null=True)),
                ('berat_badan', models.FloatField(null=True)),
                ('lingkar_perut', models.FloatField(null=True)),
                ('pengukuran_fungsi_paru', models.CharField(choices=[(None, ''), ('Normal', 'Normal'), ('Buruk', 'Buruk')], max_length=10, null=True)),
                ('gula', models.IntegerField(null=True)),
                ('kolestrol', models.IntegerField(null=True)),
                ('trigliserida', models.IntegerField(null=True)),
                ('benjolan_payudara', models.NullBooleanField(choices=[(None, ''), (True, 'Ditemukan'), (False, 'Tidak Ditemukan')])),
                ('iva', models.NullBooleanField(choices=[(None, ''), (True, 'Positif'), (False, 'Negatif')])),
                ('kadar_alkohol_pernapasan', models.NullBooleanField(choices=[(None, ''), (True, 'Positif'), (False, 'Negatif')])),
                ('tes_amfetamin_urin', models.NullBooleanField(choices=[(None, ''), (True, 'Positif'), (False, 'Negatif')])),
                ('penyuluhan_iva_and_cbe', models.NullBooleanField(choices=[(None, ''), (True, 'Ikut'), (False, 'Tidak Ikut')])),
                ('penyuluhan_rokok', models.NullBooleanField(choices=[(None, ''), (True, 'Ikut'), (False, 'Tidak Ikut')])),
                ('penyuluhan_potensi_cedera', models.NullBooleanField(choices=[(None, ''), (True, 'Ikut'), (False, 'Tidak Ikut')])),
                ('indeks_masa_tubuh', models.FloatField(null=True)),
                ('tajam_penglihatan', models.CharField(choices=[(True, 'Normal'), (False, 'Abnormal')], max_length=9, null=True)),
                ('tajam_pendengaran', models.CharField(choices=[(True, 'Normal'), (False, 'Abnormal')], max_length=9, null=True)),
                ('gangguan_mental_emosional', models.IntegerField()),
                ('dari_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.DataPemeriksaan')),
                ('pasien', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Pasien')),
            ],
        ),
        migrations.CreateModel(
            name='Pendaftaran',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_daftar', models.DateTimeField()),
                ('keluhan', models.TextField()),
                ('dokter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Dokter')),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Pasien')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('birth_date', models.DateField()),
                ('location', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PetugasDinasKota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_dinas', models.CharField(max_length=40)),
                ('alamat_dinas', models.TextField()),
                ('no_hp', models.CharField(max_length=17)),
            ],
        ),
        migrations.CreateModel(
            name='PetugasPuskesmas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=60)),
                ('alamat', models.TextField()),
                ('no_ktp', models.CharField(max_length=30)),
                ('no_hp', models.CharField(max_length=17)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Poliklinik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenis_poli', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Puskesmas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=60)),
                ('kecamatan', models.CharField(blank=True, choices=[('karang pilang', 'Karang Pilang'), ('jambangan', 'Jambangan'), ('gayungan', 'Gayungan'), ('wonocolo', 'Wonocolo'), ('tenggilis mejoyo', 'Tenggilis Mejoyo'), ('gunung anyar', 'Gunung Anyar'), ('rungkut', 'Rungkut'), ('sukolilo', 'Sukolilo'), ('mulyorejo', 'Mulyorejo'), ('gubeng', 'Gubeng'), ('wonokromo', 'Wonokromo'), ('dukuh pakis', 'Dukuh Pakis'), ('wiyung', 'Wiyung'), ('lakasantri', 'Lakasantri'), ('sambikerep', 'Sambikerep'), ('tandes', 'Tandes'), ('suko manunggal', 'Suko Manunggal'), ('sawahan', 'Sawahan'), ('tegalsari', 'Tegalsari'), ('genteng', 'Genteng'), ('tambaksari', 'Tambaksari'), ('kenjeran', 'Kenjeran'), ('bulak', 'Bulak'), ('simokerto', 'Simokerto'), ('semampir', 'Semampir'), ('pabean cantian', 'Pabean Cantian'), ('bubutan', 'Bubutan'), ('krembangan', 'Krembangan'), ('asemrowo', 'Asemrowo'), ('benowo', 'Benowo'), ('pakal', 'Pakal')], max_length=50, null=True)),
                ('kelurahan', models.CharField(blank=True, choices=[('Karang Pilang', (('karang_pilang', 'Karang Pilang'), ('kabraon', 'Kebraon'), ('kedurus', 'Kedurus'), ('warugunung', 'Warugunung'))), ('Jambangan', (('jambangan', 'Jambangan'), ('karah', 'Karah'), ('kebonsari', 'Kebonsari'), ('pagesangan', 'Pagesangan'))), ('Gayungan', (('dukuh_manunggal', 'Dukuh Menanggal'), ('gayungan', 'Gayungan'), ('ketintang', 'Ketintang'), ('menanggal', 'Menanggal'))), ('Wonocolo', (('bendul_merisi', 'Bendul Merisi'), ('jemur_wonosari', 'Jemur Wonosari'), ('margorejo', 'Margorejo'), ('sidosermo', 'Sidosermo'), ('siwalankerto', 'Siwalankerto'))), ('Tenggilis Mejoyo', (('kendangsari', 'Kendangsari'), ('kutisari', 'Kutisari'), ('panjang_jiwo', 'Panjang Jiwo'), ('prapen', 'Prapen'), ('tenggilis_mejoyo', 'Tenggilis Mejoyo'))), ('Gunung Anyar', (('gunung_anyar', 'Gunung Anyar'), ('gunung_anyar_tambak', 'Gunung Anyar Tambak'), ('rungkut_menaggal', 'Rungkut Menaggal'), ('rungkut_tengah', 'Rungkut Tengah'))), ('Rungkut', (('kali_rungkut', 'Kali Rungkut'), ('kedung_baruk', 'Kedung Baruk'), ('medokan_ayu', 'Medokan Ayu'), ('penjaringan_sari', 'Penjaringan Sari'), ('rungkut_kidul', 'Rungkut Kidul'), ('wonorejo', 'Woonorejo'))), ('Sukolilo', (('gebang_putih', 'Gebang Putih'), ('keputih', 'Keputih'), ('klampis_ngasem', 'Klampis Ngasem'), ('medokan_semampir', 'Medokan Semampir'), ('menur_pumpungan', 'Menur Pumpungan'), ('ngindeng_jangkungan', 'Nginden Jangkungan'), ('semolowaru', 'Semolowaru'))), ('Mulyorejo', (('dukuh_sutorejo', 'Dukuh Sutorejo'), ('kalijudan', 'Kalijudan'), ('kalisari', 'Kalisari'), ('kejawen_putih', 'Kejawen Putih'), ('manyar_sabrangan', 'Manyar Sabrangan'), ('mulyorejo', 'Mulyorejo'))), ('Gubeng', (('airlangga', 'Airlangga'), ('baratajaya', 'Baratajaya'), ('gubeng', 'Gubeng'), ('kertajaya', 'Kertajaya'), ('mojo', 'Mojo'), ('pucang_sewu', 'Pucang Sewu'))), ('Wonokromo', (('darmo', 'Darmo'), ('jagir', 'Jagir'), ('ngagel', 'Ngagel'), ('ngagelrejo', 'Ngagelrejo'), ('sawunggaling', 'Sawunggaling'), ('wonokrommo', 'Wonokromo'))), ('Dukuh Pakis', (('dukuh_kupang', 'Dukuh Kupang'), ('dukuh_pakis', 'Dukuh Pakis'), ('gununngsari', 'Gunungsari'), ('pradahkali_kendal', 'Pradahkali Kendal'))), ('Wiyung', (('babatan', 'Babatan'), ('balas_klumprik', 'Balas Klumprik'), ('jajar_manunggal', 'Jajar Manunggal'), ('wiyung', 'Wiyung'))), ('Lakasantri', (('bangkingan', 'Bangkingan'), ('jeruk', 'Jeruk'), ('lakasantri', 'Lakasantri'), ('lidah_kulon', 'Lidah Kulon'), ('lidah_wetan', 'Lidah Wetan'), ('sumur_welut', 'Sumur Welut'))), ('Sambikerep', (('bringin', 'Bringin'), ('lontar', 'Lontar'), ('made', 'Made'), ('sambikerep', 'Sambikerep'))), ('Tandes', (('balongsari', 'Balongsari'), ('banjar_sugihan', 'Banjar Sugihan'), ('karangpoh', 'Karangpoh'), ('manukan_kulon', 'Manukan Kulon'), ('manukan_wetan', 'Manukan Wetan'), ('tandes', 'Tandes'))), ('Suko Manunggal', (('putat_gede', 'Putat Gede'), ('simomulyo', 'Simomulyo'), ('simomulyo_baru', 'Simomulyo Baru'), ('sono_kwijenan', 'Sono Kwijenan'), ('suko_manunggal', 'Suko Manunggal'), ('tanjungsari', 'Tanjungsari'))), ('Sawahan', (('banyu_urip', 'Banyu Urip'), ('kupang_krajan', 'Kupang Krajan'), ('pakis', 'Pakis'), ('petemon', 'Petemon'), ('putat_jaya', 'Putat Jaya'), ('sawahan', 'Sawahan'))), ('Tegalsari', (('dr_sutomo', 'Dr. Sutomo'), ('kedungdoro', 'Kedungdoro'), ('keputran', 'Keputran'), ('tegalsari', 'Tegalsari'), ('wonosari', 'Wonosari'))), ('Genteng', (('embong_kaliasin', 'Embong Kaliasin'), ('genteng', 'Genteng'), ('kapasari', 'Kapasari'), ('ketabang', 'Ketabang'), ('peneleh', 'Peneleh'))), ('Tambaksari', (('dukuh_setro', 'Dukuh Setro'), ('gading', 'Gading'), ('kapasmasya_baru', 'Kapasmadya Baru'), ('pacar_keling', 'Pacar Keling'), ('pacar_kembang', 'Pacar Kembang'), ('ploso', 'Ploso'), ('rangkah', 'Rangkah'), ('tambasari', 'Tambaksari'))), ('Kenjeran', (('bulak_banteng', 'Bulak Banteng'), ('sidotopo_wetan', 'Sidotopo Wetan'), ('tambak_wedi', 'Tambak Wedi'), ('tanah_kali_kedinding', 'Tanah Kali Kedinding'))), ('Bulak', (('bulak', 'Bulak'), ('kedung_cowek', 'Kedung Cowek'), ('kenjeran', 'Kenjeran'), ('komplek_kenjeran', 'Komplek Kenjeran'), ('sukolilo', 'Sukolilo'))), ('Simokerto', (('kapasan', 'Kapasan'), ('sidodadi', 'Sidodadi'), ('simokerto', 'Simokerto'), ('simowalang', 'Simowalang'), ('tambakrejo', 'Tambakrejo'))), ('Semampir', (('ampel', 'Ampel'), ('pegirian', 'Pegirian'), ('sidotopo', 'Sidotopo'), ('ujung', 'Ujung'), ('wonokusumo', 'Wonokusumo'))), ('Pabean Cantian', (('bongkaran', 'Bongkaran'), ('krembangan_utara', 'Kembangan Utara'), ('nyamplungan', 'Nyamplungan'), ('perak_timur', 'Perak Timur'), ('perak_utara', 'Perak Utara'))), ('Bubutan', (('alon_alon_contong', 'Alon Alon Contong'), ('bubutan', 'Bubutan'), ('gundih', 'Gundih'), ('jepara', 'Jepara'), ('tembok_dukuh', 'Tembok Dukuh'))), ('Krembangan', (('dupak', 'Dupak'), ('kemayoran', 'Kemayoran'), ('krembangan_selatan', 'Krembangan Selatan'), ('morokrembangan', 'Morokrembangan'), ('perak_barat', 'Perak Barat'))), ('Asemrowo', (('asemrowo', 'Asemrowo'), ('genting', 'Genting'), ('greges', 'Greges'), ('kalianak', 'Kalianak'), ('tambak_langon', 'Tambak Langon'))), ('Benowo', (('kandangan', 'Kandangan'), ('klakahrejo', 'Klakahrejo'), ('romokalisari', 'Romokalisari'), ('sememi', 'Sememi'), ('tambak_oso_wilangoon', 'Tambak Oso Wilangon'))), ('Pakal', (('babat_jerawat', 'Babat Jerawat'), ('benowo', 'benowo'), ('pakal', 'Pakal'), ('sumberrejo', 'Sumberrejo'), ('tambakdono', 'Tambakdono')))], max_length=50, null=True)),
                ('alamat', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Rekam_medis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal_periksa', models.DateTimeField()),
                ('pemeriksaan', models.CharField(max_length=200)),
                ('diagnosa', models.TextField()),
                ('dokter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Dokter')),
                ('pasien', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Pasien')),
            ],
        ),
        migrations.CreateModel(
            name='Resep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_obat', models.CharField(max_length=50)),
                ('jenis_obat', models.CharField(max_length=50)),
                ('keterangan', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='rekam_medis',
            name='resep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Resep'),
        ),
        migrations.AddField(
            model_name='petugaspuskesmas',
            name='puskesmas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puskesmas', to='puskesmas_app.Puskesmas'),
        ),
        migrations.AddField(
            model_name='petugaspuskesmas',
            name='user_link',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_link', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pendaftaran',
            name='poli',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Poliklinik'),
        ),
        migrations.AddField(
            model_name='pembayaran',
            name='resep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Resep'),
        ),
        migrations.AddField(
            model_name='dokter',
            name='poli',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.Poliklinik'),
        ),
        migrations.AddField(
            model_name='datapemeriksaan',
            name='petugas_puskesmas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='puskesmas_app.PetugasPuskesmas'),
        ),
    ]
