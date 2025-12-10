from django.shortcuts import render, get_object_or_404, redirect

from apps.vehiculos.models import Vehicle
from .models import WorkOrder

def add_workorder_for_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    customer = vehicle.vehicle_customer

    if not customer:
        # No permitir crear una orden de trabajo sin cliente asignado (Necesario?)
        context = {
            "vehicle": vehicle,
            'error': 'Este vehiculo no tiene un cliente asignado. Asigna uno antes de crear un trabajo'
        }
        return render(request, "workorder/add_workorder.html", context)

    if request.method == "POST":
        mileage_raw = request.POST.get("mileage", "").strip()
        notes = request.POST.get("notes", "").strip()

        mileage = int(mileage_raw) if mileage_raw.isdigit() else None

        WorkOrder.objects.create(
            vehicle=vehicle,
            customer=customer,
            mileage=mileage,
            notes=notes,
        )

        return redirect("vehiculos:vehicle", vehicle_id=vehicle.vehicle_id)
    
    context = {
        'vehicle': vehicle,
        'customer': customer,
    }

    return render(request, 'workorder/add_workorder.html', context)


def workorder(request, workorder_id):

    workorder = get_object_or_404(WorkOrder, pk=workorder_id)
    items = workorder.items.select_related("product").all()

    context = {
        "workorder": workorder,
        "items": items,
    }

    return render(request, 'workorder/workorder.html', context)