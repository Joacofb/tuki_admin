from django.contrib import admin
from .models import VehicleModel, Vehicle


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = (
        "vehiclemodel_brand",
        "vehiclemodel_name",
        "vehiclemodel_version",
        "vehiclemodel_production",
    )
    search_fields = ("vehiclemodel_brand", "vehiclemodel_name", "vehiclemodel_version")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vehicle_plate", "vehicle_customer", "vehicle_model")
    search_fields = ("vehicle_plate", "vehicle_customer__customer_name")
    list_filter = ("vehicle_model__vehiclemodel_brand",)
