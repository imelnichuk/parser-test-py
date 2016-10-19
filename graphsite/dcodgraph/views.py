from django.http import HttpResponse
from django.shortcuts import render

from .models import Regions, CountriesValues

import json


def index(request):
    regions_list = Regions.objects.order_by('name')
    context = {
        'regions_list': regions_list,
    }
    return render(request, 'dcodgraph/index.html', context)


def region_data(request, region_id):
    region_data = []

    countries = CountriesValues.objects.filter(
                    region_id = region_id).order_by('-value')

    for cntr in countries:
        region_data.append({
            "country": cntr.country,
            "value": float(cntr.value)
        })

    #return JsonResponse(region_data, safe=False)
    return HttpResponse(json.dumps(region_data), content_type="application/json")
