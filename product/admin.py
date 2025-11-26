from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "product_supplier",
        "product_price",
        "product_stock",
        "product_is_active",
    )
    search_fields = ("product_name", "product_supplier", "product_sku")
    list_filter = ("product_type", "product_supplier", "product_is_active")
