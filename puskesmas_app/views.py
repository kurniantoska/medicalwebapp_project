
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db.models import Count
from django.db.models import Q


from django.urls import reverse_lazy, reverse

from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from .models import (
    DataPemeriksaan, Puskesmas, Pemeriksaan,
    DemografiPenduduk, PetugasPuskesmas,
)


from .forms import (
    DataPemeriksaanForm, ImportFileExcelForm, DemografiPendudukForm,
    AnalisaTabelForm,
)

from .utils import EksekusiImportBerkasExcelPasien, postpone, to_persentase

from django.shortcuts import redirect
import pandas as pd

from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, JsonResponse,
    HttpResponseServerError, HttpResponseRedirect
)

import calendar


class DataPemeriksaanListView(ListView):
    model = DataPemeriksaan
    template_name = 'import_data.html'
    paginate_by = 100
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# @method_decorator(login_required, name='get_context_data')
class DataPemeriksaanDetailView(LoginRequiredMixin, DetailView):
    model = DataPemeriksaan
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DataPemeriksaanDeleteView(DeleteView):
    model = DataPemeriksaan
    success_url = reverse_lazy('home')


def login_page(request):
    context = locals()
    template = 'login.html'
    return render(request, template, context)

@login_required
def home_page(request):
    context = locals()
    template = 'home.html'
    return render(request, template, context)

from .utils import group_check
    
@login_required
def import_data(request, *args, **kwargs):
    
    # inisiasi variabel untuk grab nama kecamatan
    kecamatan_str = None
    
    # jika user staff maka mendapatkan full akses puskesmas
    # jika tidak maka mencoba untuk inisiasi pembatasan
    # petugas puskesmas
    if request.user.is_staff :
        petugas_puskesmas_instance = None
    else :
        try :
            petugas_puskesmas_instance = PetugasPuskesmas.objects.get(user_link=request.user)
            kecamatan_str = petugas_puskesmas_instance.puskesmas.kecamatan
        except :
            kecamatan_str = None
            return HttpResponseForbidden('<h1>403 Forbidden</h1> <p> Gunakan User Puskesmas untuk import data </p>, back to <a href="/">home</a> please.. ', content_type='text/html')

    if not request.user.groups.filter(name__in=['puskesmas',]) :
        return HttpResponseForbidden('<h1>403 Forbidden</h1> <a href="/">home</a>', content_type='text/html')
        
    else:
        dataPemeriksaanAll = DataPemeriksaan.objects.all()
        if 'btn_form' in request.POST:
            form_2 = None
            form = DataPemeriksaanForm(request.POST, request.FILES, request=request)
            if form.is_valid():
                publish = form.save(commit=False)
                if not request.user.is_staff :
                    publish.petugas_puskesmas = petugas_puskesmas_instance
                form.save()
                return redirect('puskesmas_app:import')
    
        elif 'btn_form_2' in request.POST:
            form = None
            form_2 = ImportFileExcelForm(request.POST, request.FILES)
            if form_2.is_valid():
                cleaned_data = form_2.cleaned_data
                jumlah_data = cleaned_data.get('jumlah_data')
                eksekusi1 = EksekusiImportBerkasExcelPasien()
                if jumlah_data:
                    eksekusi1.jumlah_data = jumlah_data
                file = cleaned_data.get('berkas')
                # print(file)
    
                eksekusi1.data_import = file
                # # eksekusi1.data_import = DataPemeriksaan.objects.get(file_excel__iexact='x.xlsx')
                #
                eksekusi1.berkas = eksekusi1.data_import.file_excel.path
                import_stage_1 = eksekusi1.baca_data_file_excel()
                import_stage_2 = eksekusi1.data_pasien_tuple_list() 
                import_stage_3 = eksekusi1.parsing_data_pasien()
                pasien, dup, berhasil = eksekusi1.data_duplikasi_cek_dan_import()
                # print(dup, berhasil)
                
                rekam_medis_stage1 = eksekusi1.data_rekam_medis()
                data_pemeriksaan, status_duplikat_data_pemeriksaan, status_berhasil_data_pemeriksaan = eksekusi1.insert_data_pemeriksaan_ke_database(
                    pasien)
    
                # print(data_pemeriksaan, status_duplikat_data_pemeriksaan, status_berhasil_data_pemeriksaan)
                return redirect('puskesmas_app:import')
        else:
            form = DataPemeriksaanForm(request=request)
            form_2 = ImportFileExcelForm()
        context = {
            'form' : form,
            'form_2' : form_2,
            'dataPemeriksaanObject' : dataPemeriksaanAll,
            'petugas_puskesmas_instance' : kecamatan_str
        }
    
    template = 'import_data.html'
    return render(request, template, context)


def data_demografi_penduduk(request):
    form = DemografiPendudukForm()
    if request.POST :
        form = DemografiPendudukForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form' : form,
    }
    template = 'data_demografi_penduduk_htm.html'
    return render(request, template, context)


def rekapitulasi_fr(request):
    tahun = 2018
    
    if request.method == "POST" :
        tahun = request.POST.get('select_tahun')
    
    # list untuk tampilan di template
    daftar_faktor_resiko = (
        'Merokok',
        'Kurang Aktivitas',
        'Kurang Konsumsi Sayur dan Buah',
        'Konsumsi Alkohol',
        'Tekanan Darah',
        'Indeks Masa Tubuh',
        'Gula Darah',
        'Lingkar Perut',
        'Kolesterol',
        'Trigliserida',
        'Benjolan Payudara',
        'IVA',
        'Kadar Alkohol Pernafasan',
        'Amfetamin Urin',
    )
    
    # list untuk referensi data filter di ORM
    a_list = ['merokok', 'kurang_aktifitas_fisik', 'kurang_sayur_dan_buah',
              'konsumsi_alkohol', 'tekanandarah', 'imt',
              'gula', 'lingkar_perut', 'kolestrol',
              'asamurat', 'benjolan_payudara', 'iva', 
              'kadar_alkohol_pernapasan', 'amfetamin_urin']
    
    # simpan nilai ke dalam variabel rekap, nilai kunjungan yang beresiko dan
    # jumlah yang diperiksa
    rekap = [Pemeriksaan.get_jumlah_beresiko_dan_diperiksa(tahun, x) for x in a_list ]
    
    # menyatukan var rekap dan daftar_faktor_resiko kedalam satu bagian
    # sehingga mudah untuk di panggil saat di template
    daftar_faktor_resiko = tuple(zip(daftar_faktor_resiko, rekap))
    
    context = {
        'daftar_faktor_resiko': daftar_faktor_resiko,
        'tahun': tahun,
    }
    
    template = 'rekapitulasi_fr_htm.html'
    return render(request, template, context)


class AnalisaTabelView(LoginRequiredMixin, FormView):
    model = Pemeriksaan
    template_name = 'analisa_tabel.html'
    form_class = AnalisaTabelForm
    success_url = reverse_lazy('puskesmas_app:analisa_tabel')
    
    def form_valid(self, form):
        context = dict()

        puskesmas = form.cleaned_data['puskesmas']
        dari = form.cleaned_data['dari']
        sd = form.cleaned_data['sd']
        jenis = form.cleaned_data['jenis']
        tipe_pemeriksaan = form.cleaned_data['pemeriksaan']

        nama_pemeriksaan = dict(form.fields['pemeriksaan'].choices)[tipe_pemeriksaan]
        nama_jenis = dict(form.fields['jenis'].choices)[jenis]

        split_from = dari.split('-')
        split_to = sd.split('-')

        last_day_to = calendar.monthrange(int(split_to[0]), int(split_to[1]))[1]

        date_range = {
            'tanggal__range': ["{}-1".format(dari), "{}-{}".format(sd, last_day_to)]
        }

        month_from = Pemeriksaan.get_month_str(int(split_from[1]))
        month_to = Pemeriksaan.get_month_str(int(split_to[1]))
        year_from = split_from[0]
        year_to = split_to[0]

        qs = Pemeriksaan.objects.filter(dari_file__petugas_puskesmas__puskesmas=puskesmas,
                                        tanggal__isnull=False, **date_range)

        dates = pd.date_range("{}-1".format(dari), "{}-{}".format(sd, last_day_to), freq='MS').strftime("%m %b %Y"). \
            tolist()

        tabel_title = "Proporsi {} Menurut {} di Posbindu {}".format(nama_pemeriksaan, nama_jenis, puskesmas.nama)
        tabel_sub_title = "{} {} s/d {} {}".format(month_from, year_from, month_to, year_to)
        tabel_data = []
        tabel_kolom = []
        tabel_header = []
        
        # delete soon
        tabel_categories = []

        if jenis == 'wilayah':
            
            results = Pemeriksaan.get_data_analisa_grafik(qs, tipe_pemeriksaan, 1, [])
                        
            jumlah_ya = results[4][0]
            jumlah_tidak = results[5][0]
            total_yang_diperiksa = results[4][0] + results[5][0]
            persentase_jumlah_ya = "{} %".format(round(results[0][0], 2))
            persentase_jumlah_tidak = "{} %".format(round(results[1][0], 2))
            
            tabel_header = [' ','Jumlah Ya', 'Presentase Ya', 'Jumlah Tidak', \
                            'Presentase tidak', 'Total yg diperiksa']

            tabel_data = [[puskesmas.nama, jumlah_ya, persentase_jumlah_ya, \
                            jumlah_tidak, persentase_jumlah_tidak, \
                            total_yang_diperiksa
                            ],
                          ['Total', jumlah_ya, persentase_jumlah_ya, \
                            jumlah_tidak, persentase_jumlah_tidak, \
                            total_yang_diperiksa ]
                        ]
            
            
            
            # for tabel expand data
            # for tabel_data['name'] ==
            
        elif jenis == 'usia':
            extra_q = [
                {'umur__gte': 15, 'umur__lte': 19},
                {'umur__gte': 20, 'umur__lte': 44},
                {'umur__gte': 45, 'umur__lte': 54},
                {'umur__gte': 55, 'umur__lte': 59},
                {'umur__gte': 60, 'umur__lte': 69},
                {'umur__gte': 70},
            ]
            
            tabel_header = ["", "Jumlah Ya","Persentase Ya", \
                            "Jumlah Tidak", "Persentase Tidak", \
                            "Total Yg Diperiksa"]
            
            results = Pemeriksaan.get_data_analisa_grafik(qs, tipe_pemeriksaan, len(extra_q), extra_q)
            print("========== results", results)
            
            data_kolom1 = ['15-19', '20-44', '45-54', '55-59', '60-69', '>70', 'TOTAL']
            jumlah_ya = results[4]
            persentase_ya = results[0]
            jumlah_tidak = results[5]
            persentase_tidak = results[1]
            total_yang_diperiksa = [x+y for x, y in zip(jumlah_ya, jumlah_tidak)]
            
            
            #total_
            jumlah_ya[-1] = sum(jumlah_ya[:-1])
            jumlah_tidak[-1] = sum(jumlah_tidak[:-1])
            total_yang_diperiksa[-1] = sum(total_yang_diperiksa[:-1])
            persentase_ya[-1] = jumlah_ya[-1] / total_yang_diperiksa[-1] * 100 if total_yang_diperiksa[-1] > 0 else 0
            persentase_tidak[-1] = jumlah_tidak[-1] / total_yang_diperiksa[-1] * 100 if total_yang_diperiksa[-1] > 0 else 0
            
            # finishing simbol %
            persentase_ya = to_persentase(persentase_ya)
            persentase_tidak = to_persentase(persentase_tidak)
            
            tabel_data = []
                
            for i in range(len(data_kolom1)) :
                tabel_data.append([ data_kolom1[i], jumlah_ya[i], \
                    persentase_ya[i], 
                    jumlah_tidak[i], \
                    persentase_tidak[i], \
                    total_yang_diperiksa[i]
                    ])
            
            
        else:
            extra_q = []
    
            data_value = []
            for i in dates:
                split_date_format = i.split(" ")
                tabel_categories.append(" ".join(split_date_format[1:]))
                extra_q.append({
                    'tanggal__month': split_date_format[0],
                    'tanggal__year': split_date_format[2]
                })
            tabel_categories.append('TOTAL')
            
            if jenis == "jenis_kelamin":
                results = Pemeriksaan.get_data_analisa_grafik_jenis_kelamin(qs, tipe_pemeriksaan, len(extra_q), extra_q)
                tabel_header = ["", "Jumlah Laki-laki","Persentase Laki-laki", \
                            "Jumlah Perempuan", "Persentase Perempuan", \
                            "Total Yg Diperiksa"]
                
                jumlah_laki = results[4]
                persentase_laki = results[0]
                jumlah_perempuan = results[5]
                persentase_perempuan = results[1]
                total_yang_diperiksa = [x+y for x, y in zip(jumlah_laki, jumlah_perempuan)]
                data_kolom1 = tabel_categories
                
                #total_
                jumlah_laki[-1] = sum(jumlah_laki[:-1])
                jumlah_perempuan[-1] = sum(jumlah_perempuan[:-1])
                total_yang_diperiksa[-1] = sum(total_yang_diperiksa[:-1])
                persentase_laki[-1] = jumlah_laki[-1] / total_yang_diperiksa[-1] * 100 if total_yang_diperiksa[-1] > 0 else 0
                persentase_perempuan[-1] = jumlah_perempuan[-1] / total_yang_diperiksa[-1] * 100 if total_yang_diperiksa[-1] > 0 else 0
                
                # finishing simbol %
                persentase_laki = to_persentase(persentase_laki)
                persentase_perempuan = to_persentase(persentase_perempuan)
                
                tabel_data = []
                
                
                
                for i in range(len(data_kolom1)) :
                    tabel_data.append([ data_kolom1[i], jumlah_laki[i], \
                        persentase_laki[i], 
                        jumlah_perempuan[i], \
                        persentase_perempuan[i], \
                        total_yang_diperiksa[i]
                        ])
                
                # # debug
                # print("result 0")
                # print("{}".format(results[0]))
                # print("result 1")
                # print("{}".format(results[1]))
                # print("result 2")
                # print("{}".format(results[2]))
                # print("result 3")
                # print("{}".format(results[3]))
                # print("result 4")
                # print("{}".format(results[4]))
                # print("result 5")
                # print("{}".format(results[5]))
                # print("result 6")
                # print("{}".format(results[6]))
                # print("result 7")
                # print("{}".format(results[7]))
                
            else:
                results = Pemeriksaan.get_data_analisa_grafik(qs, tipe_pemeriksaan, len(extra_q), extra_q)
                
                tabel_header = ["", "Jumlah Ya","Persentase Ya", \
                            "Jumlah Tidak", "Persentase Tidak", \
                            "Total Yg Diperiksa"]
                data_kolom1 = tabel_categories
                jumlah_ya = results[4]
                persentase_ya = results[0]
                jumlah_tidak = results[5]
                persentase_tidak = results[1]
                total_yang_diperiksa = [x+y for x, y in zip(jumlah_ya, jumlah_tidak)]
                
                
                #total_
                jumlah_ya[-1] = sum(jumlah_ya[:-1])
                jumlah_tidak[-1] = sum(jumlah_tidak[:-1])
                total_yang_diperiksa[-1] = sum(total_yang_diperiksa[:-1])
                persentase_ya[-1] = jumlah_ya[-1] / total_yang_diperiksa[-1] * 100 if total_yang_diperiksa[-1] > 0 else 0
                persentase_tidak[-1] = jumlah_tidak[-1] / total_yang_diperiksa[-1] * 100 if total_yang_diperiksa[-1] > 0 else 0
                
                # finishing simbol %
                persentase_ya = to_persentase(persentase_ya)
                persentase_tidak = to_persentase(persentase_tidak)
                
                tabel_data = []
                    
                for i in range(len(data_kolom1)) :
                    tabel_data.append([ data_kolom1[i], jumlah_ya[i], \
                        persentase_ya[i], 
                        jumlah_tidak[i], \
                        persentase_tidak[i], \
                        total_yang_diperiksa[i]
                        ])
                
                # debug
                # print("========== results", results)
                

        context.update({
            'form': form,
            'tabel_title': tabel_title,
            'tabel_sub_title': tabel_sub_title,
            'tabel_header': tabel_header,
            'tabel_data': tabel_data,
            'results': qs,
            'jenis' : jenis
        })

        return render(self.request, self.get_template_names(), context)


class AnalisaGrafikView(LoginRequiredMixin, FormView):
    model = Pemeriksaan
    template_name = 'analisa_grafik.html'
    form_class = AnalisaTabelForm
    success_url = reverse_lazy('puskesmas_app:analisa_grafik')

    def form_valid(self, form):
        context = dict()

        puskesmas = form.cleaned_data['puskesmas']
        dari = form.cleaned_data['dari']
        sd = form.cleaned_data['sd']
        jenis = form.cleaned_data['jenis']
        tipe_pemeriksaan = form.cleaned_data['pemeriksaan']

        nama_pemeriksaan = dict(form.fields['pemeriksaan'].choices)[tipe_pemeriksaan]
        nama_jenis = dict(form.fields['jenis'].choices)[jenis]

        split_from = dari.split('-')
        split_to = sd.split('-')

        last_day_to = calendar.monthrange(int(split_to[0]), int(split_to[1]))[1]

        date_range = {
            'tanggal__range': ["{}-1".format(dari), "{}-{}".format(sd, last_day_to)]
        }

        month_from = Pemeriksaan.get_month_str(int(split_from[1]))
        month_to = Pemeriksaan.get_month_str(int(split_to[1]))
        year_from = split_from[0]
        year_to = split_to[0]

        qs = Pemeriksaan.objects.filter(dari_file__petugas_puskesmas__puskesmas=puskesmas,
                                        tanggal__isnull=False, **date_range)

        dates = pd.date_range("{}-1".format(dari), "{}-{}".format(sd, last_day_to), freq='MS').strftime("%m %b %Y"). \
            tolist()

        chart_title = "Proporsi {} Menurut {} di Posbindu {}".format(nama_pemeriksaan, nama_jenis, puskesmas.nama)
        chart_sub_title = "{} {} s/d {} {}".format(month_from, year_from, month_to, year_to)
        chart_data = []
        chart_categories = []
        
        if jenis == 'wilayah':
            chart_categories.insert(0, puskesmas.nama)
            chart_categories.append('TOTAL')
            results = Pemeriksaan.get_data_analisa_grafik(qs, tipe_pemeriksaan, 1, [])
            
            chart_data.append({
                'name': 'Persentase Ya',
                'color': '#f70000',
                'data': results[0]
            })
            chart_data.append({
                'name': 'Persentase Tidak',
                'color': '#a9c283',
                'data': results[1]
            })
        elif jenis == 'usia':
            extra_q = [
                {'umur__gte': 15, 'umur__lte': 19},
                {'umur__gte': 20, 'umur__lte': 44},
                {'umur__gte': 45, 'umur__lte': 54},
                {'umur__gte': 55, 'umur__lte': 59},
                {'umur__gte': 60, 'umur__lte': 69},
                {'umur__gte': 70},
            ]
            chart_categories = ['15-19', '20-44', '45-54', '55-59', '60-69', '70<', 'TOTAL']
            results = Pemeriksaan.get_data_analisa_grafik(qs, tipe_pemeriksaan, len(extra_q), extra_q)
            
            chart_data.append({
                'name': 'Persentase Ya',
                'color': '#f70000',
                'data': results[0]
            })
            chart_data.append({
                'name': 'Persentase Tidak',
                'color': '#a9c283',
                'data': results[1]
            })
        else:
            extra_q = []
    
            data_value = []
            for i in dates:
                split_date_format = i.split(" ")
                chart_categories.append(" ".join(split_date_format[1:]))
                extra_q.append({
                    'tanggal__month': split_date_format[0],
                    'tanggal__year': split_date_format[2]
                })
            chart_categories.append('TOTAL')
            
            if jenis == "jenis_kelamin":
                results = Pemeriksaan.get_data_analisa_grafik_jenis_kelamin(qs, tipe_pemeriksaan, len(extra_q), extra_q)
                
                chart_data.append({
                    'name': 'Persentase Laki-laki',
                    'color': '#4572A7',
                    'data': results[0]
                })
                chart_data.append({
                    'name': 'Persentase Perempuan',
                    'color': '#cf9898',
                    'data': results[1]
                })
            else:
                results = Pemeriksaan.get_data_analisa_grafik(qs, tipe_pemeriksaan, len(extra_q), extra_q)
                
                chart_data.append({
                    'name': 'Persentase Ya',
                    'color': '#f70000',
                    'data': results[0]
                })
                chart_data.append({
                    'name': 'Persentase Tidak',
                    'color': '#a9c283',
                    'data': results[1]
                })
        
        context.update({
            'form': form,
            'chart_title': chart_title,
            'chart_sub_title': chart_sub_title,
            'chart_categories': chart_categories,
            'chart_data': chart_data,
            'results': qs,
        })

        return render(self.request, self.get_template_names(), context)


# def analisa_grafik(request):
#     """ analisa grafik dengan url /puskesmas/penduduk/ """
#     form = AnalisaTabelForm()
#     context = {
#         'form' : form
#     }
#     template = 'analisa_grafik.html'
#     return render(request, template, context)

def form_handle_eksekusi_import(request):
    pass
    # if request.method == 'POST':
    #     form = MyForm(request.POST) # if post method then form will be validated
    #     if form.is_valid():
    #         cd = form.cleaned_data
    #         num1 = cd.get('num1')
    #         num2 = cd.get('num2')
    #         result = cd.get('result')
    #         if float(num1) + float(num2) == float(result):
    #             # give HttpResponse only or render page you need to load on success
    #             return HttpResponse("valid entiries")
    #         else:
    #             # if sum not equal... then redirect to custom url/page
    #             return HttpResponseRedirect('/')  # mention redirect url in argument
    #
    # else:
    #     form = MyForm() # blank form object just to pass context if not post method
    # return render(request, "rr.html", {'form': form})

def registrasi_petugas(request): 
    pass


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response
            
            
class DemografiPendudukCreateView(AjaxableResponseMixin, CreateView):
    model = DemografiPenduduk
    fields = '__all__'
    template_name = 'data_demografi_penduduk_htm.html'
