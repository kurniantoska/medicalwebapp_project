import json
from django.http import JsonResponse
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Passenger

# Create your views here.
def ticket_class_view(request):
    dataset = Passenger.objects \
        .values('ticket_class')\
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')
    context = {
        'dataset': dataset
    }
    return render(request, 'ticket_class.html', context)

def ticket_class_view_2(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')
    categories = list()
    survived_series = list()
    not_survived_series = list()

    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])
        survived_series.append(entry['survived_count'])
        not_survived_series.append(entry['not_survived_count'])

    context = {
        'categories' : json.dumps(categories),
        'survived_series' : json.dumps(survived_series),
        'not_survived_series' : json.dumps(not_survived_series)
    }

    return render(request, 'ticket_class_2.html', context)

def ticket_class_view_3(request):
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    categories = list()
    survived_series_data = list()
    not_survived_series_data = list()

    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])
        survived_series_data.append(entry['survived_count'])
        not_survived_series_data.append(entry['not_survived_count'])

    survived_series = {
        'name' : 'Survived',
        'data' : survived_series_data,
        'color' : 'blue'
    }

    not_survived_series = {
        'name' : 'Not Survived',
        'data' : not_survived_series_data,
        'color' : 'red'
    }

    chart = {
        'chart': {'type':'column'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        'series': [survived_series, not_survived_series ]
    }

    dump = json.dumps(chart)
    context = {
        'chart' : dump
    }
    return render(request, 'ticket_class_3.html', context)


def json_example(request):
    return render(request, 'json_example.html')

def chart_data(request):
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('embarked')) \
        .order_by('embarked')

    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]

    chart = {
        'chart' : {'type' : 'pie'},
        'title' : {'text': 'Titanic Survivors by Ticket Class'},
        'series' : [{
            'name' : 'Embarkation Port',
            'data' : list(map(lambda row:{'name':port_display_name[row['embarked']], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)