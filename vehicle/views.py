from django.shortcuts import render, redirect

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
    pass


def all_vehicles(request):
    context = {'vehicles': Vehicle.objects.all()}

    return render(request, 'vehicle/all_vehicles.html', context)


def vehicle(request, vehicle_id):
    pass
