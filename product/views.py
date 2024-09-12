from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm


def all_products(request):
    search_data = request.GET.get('search_product', '')

    if search_data:
        get_products = Product.objects.filter(product_sku__icontains=search_data).order_by('product_sku')
    else:
        get_products = Product.objects.all().order_by('product_sku')

    paginator = Paginator(get_products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'search_data': search_data,
        'page_obj': page_obj
    }

    return render(request, 'product/all_products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()

    return render(request, 'product/add_product.html', {'form': form})
