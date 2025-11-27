# customer/views.py
from django.shortcuts import render, get_object_or_404
from .models import Customer


def customer_list(request):
    customers = Customer.objects.all().order_by("customer_name")
    return render(request, "customer/customer_list.html", {"customers": customers})


def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # vehículos de este cliente (related_name='vehicles' en Vehicle)
    vehicles = customer.vehicles.all()

    # para cada vehículo, los últimos 5 trabajos
    vehicle_workorders = []
    for v in vehicles:
        last_workorders = v.workorders.order_by("-date")[:5]
        vehicle_workorders.append((v, last_workorders))

    context = {
        "customer": customer,
        "vehicle_workorders": vehicle_workorders,
    }
    return render(request, "customer/customer_detail.html", context)
