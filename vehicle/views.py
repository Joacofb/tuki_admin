from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import BRAND_CHOICES, Vehicle


def add_vehicle(request):
    context = {'brands': BRAND_CHOICES}

    if request.method == 'POST':
        vehicle_brand = request.POST.get('vehicle_brand', '')
        vehicle_model = request.POST.get('vehicle_model', '')
        vehicle_version = request.POST.get('vehicle_version', '')
        vehicle_production = request.POST.get('vehicle_production', '')
        vehicle_details = request.POST.get('vehicle_details', '')

        if vehicle_brand and vehicle_model and vehicle_version:
            Vehicle.objects.create(
                vehicle_brand=vehicle_brand,
                vehicle_model=vehicle_model,
                vehicle_version=vehicle_version,
                vehicle_production=vehicle_production,
                vehicle_details=vehicle_details,
            )
            return redirect('/vehicles/all')

    return render(request, 'vehicle/add_vehicle.html', context)


def edit_vehicle(request):
    pass


def delete_vehicle(request, vehicle_id):
    get_vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    context = {
        'vehicle': get_vehicle
    }

    if request.method == 'POST':
        get_vehicle.delete()
        return redirect('/vehicles/all')

    # get_vehicle = Vehicle.objects.get(pk=vehicle_id)
    # get_vehicle.delete()

    return render(request, 'vehicle/delete_vehicle.html', context)


def all_vehicles(request):

    search_data = request.GET.get('search_vehicle', '')

    if search_data:
        vehicles = Vehicle.objects.filter(vehicle_model__icontains=search_data).order_by('vehicle_brand')
    else:
        vehicles = Vehicle.objects.all().order_by('vehicle_brand')

    paginator = Paginator(vehicles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_data': search_data,
    }

    return render(request, 'vehicle/all_vehicles.html', context)


def vehicle(request, vehicle_id):
    get_vehicle = Vehicle.objects.get(pk=vehicle_id)
    context = {
        'vehicle': get_vehicle,
    }

    return render(request, 'vehicle/vehicle.html', context)
