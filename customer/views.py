from django.shortcuts import render
from .models import Customer


# Create your views here.
def all_customers(request):
    get_customers = Customer.objects.all()

    return render(request, 'customer/all_customers.html', {'customers': get_customers})


def add_customer(request):
    pass

def delete_customer(request, customer_id):
    pass

def edit_customer(request, customer_id):
    pass

def customer(request, customer_id):
    pass
