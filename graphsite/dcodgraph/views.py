from django.http import HttpResponse
from django.shortcuts import render

from .models import Regions, CountriesValues
from .forms import UploadFileForm

import json

def index(request):
    regions_list = Regions.objects.order_by('name')

    is_uploaded = False
    error = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['file'].content_type == "application/json":

                handle_uploaded_file(request.FILES['file'])
                is_uploaded = True
            else:
                error = 'json-error'
    else:
        form = UploadFileForm()

    context = {
        'regions_list': regions_list,
        'form': form,
        'is_uploaded': is_uploaded,
        'error': error
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


def handle_uploaded_file(f):
    data = json.loads(f.file.read().decode('utf8'))
    data = unify_data(data)

    update_database(data)


def update_database(data):
    regions_ids = {}
    regions = list(data.keys())

    # update Regions
    for region in sorted(regions):

        region_obj, created = Regions.objects.get_or_create(
            name = region
        )
        regions_ids[region] = region_obj.region_id

    # update Countries
    for region, counties_values in data.items():
        region_id = regions_ids[region]
        for country, new_value in counties_values:

            country_obj, created = CountriesValues.objects.update_or_create(
                country = country, region_id = region_id,
                defaults={'value': new_value},
            )


def unify_data(data):
    ''' Get rid of the repeated use of the region name
        and reorganize data in more convenient structure '''

    unified_data = {}

    for el in data['data']:
        region = el['Регион']
        country_value = (el['Страна'], el['Значение'])

        if region in unified_data:
            unified_data[region].append(country_value)
        else:
            unified_data[region] = [country_value]

    return unified_data
