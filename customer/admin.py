from django.contrib import admin
from .models import Customer

# Register your models here.
# admin.site.register(Customer)
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "customer_phone", "customer_email")
    search_fields = ("customer_name", "customer_phone", "customer_email")