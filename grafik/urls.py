from django.urls import path

from .views import (
    ticket_class_view,
    ticket_class_view_2,
    ticket_class_view_3,
    json_example,
    chart_data
)

app_name = 'grafik'

urlpatterns = [
    path('', ticket_class_view, name='grafik_ticket_class'),
    path('titanic2', ticket_class_view_2, name='grafik_ticket_class_2'),
    path('titanic3', ticket_class_view_3, name='grafik_ticket_class_3'),
    path('json-example/', json_example, name='json_example'),
    path('json-example/data', chart_data, name='chart_data')
]
