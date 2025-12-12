from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.vehiculos.models import Vehicle
from customer.models import Customer
from .models import WorkOrder


def add_workorder_for_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    customers = Customer.objects.all().order_by('customer_name')

    # Siempre obtenemos el cliente actual del vehículo
    customer = vehicle.vehicle_customer

    mileage_raw = ""
    notes = ""

    if request.method == "POST":
        action = request.POST.get("action") or ""  # puede venir vacío si usas otro botón del layout

        # Valores introducidos, para poder re-pintarlos si hay errores
        mileage_raw = request.POST.get("mileage", "").strip()
        notes = request.POST.get("notes", "").strip()

        # --- ACCIÓN 1: ASIGNAR CLIENTE ---
        if action == "assign_customer":
            customer_id = request.POST.get("vehicle_customer", "").strip()

            if not customer_id:
                messages.error(request, "Debes seleccionar un cliente para asignar.")
            else:
                customer_obj = Customer.objects.filter(customer_id=customer_id).first()
                if not customer_obj:
                    messages.error(request, "El cliente seleccionado no es válido.")
                else:
                    vehicle.vehicle_customer = customer_obj
                    vehicle.save()
                    messages.success(request, "Cliente asignado correctamente.")
                    return redirect("workorder:add_for_vehicle", vehicle_id=vehicle_id)

        # --- ACCIÓN 2: GUARDAR WORKORDER ---
        elif action == "":
            # Re-leer el cliente actual del vehículo por seguridad
            customer = vehicle.vehicle_customer

            if not customer:
                messages.error(
                    request,
                    "Debes asignar un cliente al vehículo antes de crear una orden de trabajo."
                )
            else:
                mileage = int(mileage_raw) if mileage_raw.isdigit() else None

                WorkOrder.objects.create(
                    vehicle=vehicle,
                    customer=customer,
                    mileage=mileage,
                    notes=notes,
                )

                messages.success(request, "Orden de trabajo creada correctamente.")
                return redirect("vehiculos:vehicle", vehicle_id=vehicle.vehicle_id)

        # Si la acción no coincide con nada conocido, simplemente caes al render con mensajes

    context = {
        "vehicle": vehicle,
        "customer": vehicle.vehicle_customer,  # actualizado si se cambió
        "customers": customers,
        "mileage": mileage_raw,
        "notes": notes,
    }

    return render(request, "workorder/add_workorder.html", context)



def workorder(request, workorder_id):

    workorder = get_object_or_404(WorkOrder, pk=workorder_id)
    items = workorder.items.select_related("product").all()

    context = {
        "workorder": workorder,
        "items": items,
    }

    return render(request, 'workorder/workorder.html', context)