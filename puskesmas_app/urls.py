"""medisproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views
from .views import DataPemeriksaanListView, DataPemeriksaanDetailView

app_name = 'puskesmas_app'
urlpatterns = [
    path('import/', views.import_data, name='import'),
    path('penduduk/', views.data_demografi_penduduk, name='penduduk'),
    path('rekapituasi_fr/', views.rekapitulasi_fr, name='rekapitulasi_fr'),
    path('analisa_tabel/', views.analisa_tabel, name='analisa_tabel'),
    path('analisa_grafik/', views.analisa_grafik, name='analisa_grafik'),
    path('data_pemeriksaan/', DataPemeriksaanListView.as_view(),
         name='data-pemeriksaan-list'),
    path('data_pemeriksaan/<int:pk>/',
         DataPemeriksaanDetailView.as_view(),
         name='data-pemeriksaan-detail'
         )


]
