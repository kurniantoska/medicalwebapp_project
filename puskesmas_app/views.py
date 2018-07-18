
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test

from django.db.models import Count
from django.db.models import Q


from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import (
    DataPemeriksaan, Puskesmas, Pemeriksaan,
    DemografiPenduduk,
)


from .forms import (
    DataPemeriksaanForm, ImportFileExcelForm, DemografiPendudukForm
)

from .utils import EksekusiImportBerkasExcelPasien

from django.shortcuts import redirect

from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,
)


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



# Create your views here.
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
def import_data(request):
    # print(request.POST)
    
    if not request.user.groups.filter(name__in=['puskesmas',]) :
        return HttpResponseForbidden('<h1>403 Forbidden</h1> <a href="/">home</a>', content_type='text/html')
    else:
        dataPemeriksaanAll = DataPemeriksaan.objects.all()
        if 'btn_form' in request.POST:
            form_2 = None
            form = DataPemeriksaanForm(request.POST, request.FILES)
            if form.is_valid():
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
            form = DataPemeriksaanForm()
            form_2 = ImportFileExcelForm()
    
        context = {
            'form' : form,
            'form_2' : form_2,
            'dataPemeriksaanObject' : dataPemeriksaanAll,
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
    
    a_list = ['merokok', 'kurang_aktifitas_fisik', 'kurang_sayur_dan_buah',
              'konsumsi_alkohol', 'benjolan_payudara', 'iva',]
              
              
    qs = Pemeriksaan.objects.filter(date_check__year=a_year)

    for item in a_list :
        data = qs.aggregate(
            p1=Count('pk', filter=Q(**{item: True})),
    		p2=Count('pk', filter=Q(**{item: False})),
            p3=Count('pk', filter=Q(**{item: None})),
        )
        jumlah_yg[item] = data['p1'] or 0
        jumlah_yg_tidak[item] = data['p2'] or 0
        jumlah_tdk_diperiksa[item] = data['p3'] or 0

    context = {
        'daftar_faktor_resiko' : daftar_faktor_resiko,
    }
    
    template = 'rekapitulasi_fr_htm.html'
    return render(request, template, context)

def analisa_tabel(request):
    context = locals()
    template = 'analisa_tabel.html'
    return render(request, template, context)

def analisa_grafik(request):
    """ analisa grafik dengan url /puskesmas/penduduk/ """
    context = locals()
    template = 'analisa_grafik.html'
    return render(request, template, context)

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
    
    
    
    
    
    