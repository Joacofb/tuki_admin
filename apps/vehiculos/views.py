from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import BRAND_CHOICES, Vehicle, VehicleModel
from django.db.models import Q
# from .forms import VehicleForm


# def add_vehicle(request):
#     context = {'brands': BRAND_CHOICES}

#     if request.method == 'POST':
#         vehicle_brand = request.POST.get('vehicle_brand', '')
#         vehicle_model = request.POST.get('vehicle_model', '')
#         vehicle_version = request.POST.get('vehicle_version', '')
#         vehicle_production = request.POST.get('vehicle_production', '')
#         vehicle_details = request.POST.get('vehicle_details', '')

#         if vehicle_brand and vehicle_model and vehicle_version:
#             Vehicle.objects.create(
#                 vehicle_brand=vehicle_brand,
#                 vehicle_model=vehicle_model,
#                 vehicle_version=vehicle_version,
#                 vehicle_production=vehicle_production,
#                 vehicle_details=vehicle_details,
#             )
#             return redirect('vehiculos:all')

#     return render(request, 'vehicle/add_vehicle.html', context)


def add_vehicle(request):
    vehicle_models = VehicleModel.objects.all().order_by(
        "vehiclemodel_brand", "vehiclemodel_name", "vehiclemodel_version"
    )

    context = {
        "brands": BRAND_CHOICES,
        "vehicle_models": vehicle_models,
        "errors": [],
    }

    if request.method == "POST":
        # 1) Intento de usar un modelo existente
        existing_model_id = request.POST.get("vehicle_model_id", "").strip()

        # 2) Datos para crear un modelo nuevo
        new_brand = request.POST.get("vehiclemodel_brand", "").strip()
        new_name = request.POST.get("vehiclemodel_name", "").strip()
        new_version = request.POST.get("vehiclemodel_version", "").strip()
        new_production = request.POST.get("vehiclemodel_production", "").strip()

        # Datos del vehículo concreto
        vehicle_plate = request.POST.get("vehicle_plate", "").strip()
        vehicle_color = request.POST.get("vehicle_color", "").strip()
        vehicle_details = request.POST.get("vehicle_details", "").strip()

        errors = []
        vehicle_model_obj = None

        # Lógica: o seleccionás un modelo existente o definís uno nuevo
        if existing_model_id:
            try:
                vehicle_model_obj = VehicleModel.objects.get(pk=existing_model_id)
            except VehicleModel.DoesNotExist:
                errors.append("El modelo de vehículo seleccionado no existe.")
        else:
            # No eligió uno existente → intento crear uno nuevo
            if not (new_brand and new_name):
                errors.append(
                    "Debes seleccionar un modelo existente o completar marca y modelo para crear uno nuevo."
                )
            else:
                vehicle_model_obj = VehicleModel.objects.create(
                    vehiclemodel_brand=new_brand,
                    vehiclemodel_name=new_name,
                    vehiclemodel_version=new_version or None,
                    vehiclemodel_production=new_production or None,
                )

        if not errors:
            Vehicle.objects.create(
                vehicle_model=vehicle_model_obj,
                vehicle_plate=vehicle_plate or None,
                vehicle_color=vehicle_color or None,
                vehicle_details=vehicle_details or None,
                # más adelante acá vas a meter vehicle_customer
            )
            return redirect("vehiculos:all")

        # Si hubo errores, los devolvemos al template
        context["errors"] = errors
        context["form_data"] = request.POST

    return render(request, "vehicle/add_vehicle.html", context)


def edit_vehicle(request, vehicle_id):
    print("DEBUG edit_vehicle: method =", request.method, "vehicle_id =", vehicle_id)
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)

    vehicle_models = VehicleModel.objects.all().order_by(
        "vehiclemodel_brand", "vehiclemodel_name", "vehiclemodel_version"
    )
        
    context = {
        "brands": BRAND_CHOICES,
        "vehicle_models": vehicle_models,
        "vehicle": vehicle,
        "errors": [],
    }

    if request.method == 'POST':

        print("DEBUG POST raw data:", request.POST)
        print("DEBUG POST as dict:", request.POST.dict())

        existing_model_id = request.POST.get("vehicle_model_id", "").strip()

        # Datos del vehículo concreto
        vehicle_plate = request.POST.get("vehicle_plate", "").strip()
        vehicle_color = request.POST.get("vehicle_color", "").strip()
        vehicle_details = request.POST.get("vehicle_details", "").strip()

        print("DEBUG read from POST:")
        print("  existing_model_id:", repr(existing_model_id))
        print("  vehicle_plate:", repr(vehicle_plate))
        print("  vehicle_color:", repr(vehicle_color))
        print("  vehicle_details:", repr(vehicle_details))

        errors = []
        vehicle_model_obj = None

        # Lógica: o seleccionás un modelo existente o definís uno nuevo
        if existing_model_id:
            try:
                vehicle_model_obj = VehicleModel.objects.get(pk=existing_model_id)
            except VehicleModel.DoesNotExist:
                errors.append("El modelo de vehículo seleccionado no existe.")

        else:
            vehicle_model_obj = vehicle.vehicle_model
        
        if not errors:

            print("DEBUG before update:", vehicle_id)

            vehicle.vehicle_model = vehicle_model_obj
            vehicle.vehicle_plate = vehicle_plate or None
            vehicle.vehicle_color = vehicle_color or None
            vehicle.vehicle_details = vehicle_details or None

            print("DEBUG to save:", vehicle_id)

            vehicle.save()

            print("DEBUG after save:", Vehicle.objects.get(pk=vehicle.pk).vehicle_details)
            return redirect("vehiculos:all")
        
        # Si hubo errores, los devolvemos al template
        context["errors"] = errors
        context["form_data"] = request.POST
            
    return render(request, "vehicle/edit_vehicle.html", context)

# def edit_vehicle(request, vehicle_id):
#     # get_vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
#     #
#     # if request.method == 'POST':
#     #     form = VehicleForm(request.POST, instance=get_vehicle)
#     #     if form.is_valid():
#     #         form.save()
#     #         return redirect('/vehicles/all')  # O redirigir a la página de detalles del vehículo
#     # else:
#     #     form = VehicleForm(instance=get_vehicle)
#     #
#     # return render(request, 'vehicle/edit_vehicle.html', {'form': form, 'vehicle': vehicle})

#     # get_vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
#     # context = {'vehicle': get_vehicle}

#     # if request.method == 'POST':
#     #     vehicle_brand = request.POST.get('vehicle_brand', '')
#     #     vehicle_model = request.POST.get('vehicle_model', '')
#     #     vehicle_version = request.POST.get('vehicle_version', '')
#     #     vehicle_production = request.POST.get('vehicle_production', '')
#     #     vehicle_details = request.POST.get('vehicle_details', '')

#     #     if vehicle_brand and vehicle_model and vehicle_version:
#     #         get_vehicle.vehicle_brand = vehicle_brand
#     #         get_vehicle.vehicle_model = vehicle_model
#     #         get_vehicle.vehicle_version = vehicle_version
#     #         get_vehicle.vehicle_production = vehicle_production
#     #         get_vehicle.vehicle_details = vehicle_details

#     #         get_vehicle.save()

#     #         return redirect('vehiculos:vehicle', vehicle_id=vehicle_id)

#     # return render(request, 'vehicle/edit_vehicle.html', context)




def delete_vehicle(request, vehicle_id):
    get_vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    context = {'vehicle': get_vehicle}

    if request.method == 'POST':
        get_vehicle.delete()
        return redirect('vehiculos:all')

    return render(request, 'vehicle/delete_vehicle.html', context)


def all_vehicles(request):
    search_data = request.GET.get('search_vehicle', '')

    # if search_data:
    #     vehicles = Vehicle.objects.filter(vehicle_model__icontains=search_data).order_by('vehicle_brand')
    # else:
    #     vehicles = Vehicle.objects.all().order_by('vehicle_brand')

    vehicles = Vehicle.objects.select_related('vehicle_model', 'vehicle_customer')

    if search_data:
        vehicles = vehicles.filter(
            Q(vehicle_plate__icontains=search_data)
            | Q(vehicle_model__vehiclemodel_name__icontains=search_data)
            | Q(vehicle_model__vehiclemodel_brand__icontains=search_data)
            | Q(vehicle_customer__customer_name__icontains=search_data)
        )

    vehicles = vehicles.order_by('vehicle_model__vehiclemodel_brand', 'vehicle_plate')

    paginator = Paginator(vehicles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_data': search_data,
    }

    return render(request, 'vehicle/all_vehicles.html', context)


def vehicle(request, vehicle_id):
    get_vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    context = {'vehicle': get_vehicle}

    return render(request, 'vehiculos/vehicle.html', context)
