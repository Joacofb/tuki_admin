# customer/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Customer


def customer_list(request):
    search_data = request.GET.get('search_customer', '')

    customers = Customer.objects.all().order_by("customer_name")

    if search_data:
        customers = customers.filter(
            Q(customer_name__icontains=search_data)
            | Q(customer_email__icontains=search_data)
            | Q(customer_phone__icontains=search_data)
        )

    return render(request, "customer/all_customers.html", {"customers": customers})


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

def add_customer(request):

    if request.method == "POST":
        customer_name = request.POST.get("customer_name", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        customer_email = request.POST.get("customer_email", "").strip()

        customer_type = request.POST.get("customer_type", "").strip()
        customer_billing = request.POST.get("customer_billing", "").strip()

        if customer_name and customer_phone:
            customer = Customer.objects.create(
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email or None,
                customer_type=customer_type or None,
                customer_billing=customer_billing or None,
            )
            
            return redirect('customer:detail', customer_id=customer.customer_id)

        else:
            messages.error(request, "Asigna un nombre y un telefono para crear un cliente.")


    return render(request, 'customer/add_customer.html')

def delete_customer(request, customer_id):
    get_customer = get_object_or_404(Customer, customer_id=customer_id)
    context = {
        'customer': get_customer,
    }

    if request.method == 'POST':
        get_customer.delete()
        return redirect('customer:list')
    
    return render(request, "customer/delete_customer.html", context)