from django.contrib import admin
from .models import WorkOrder, WorkOrderItem


class WorkOrderItemInline(admin.TabularInline):
    model = WorkOrderItem
    extra = 1


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("workorder_id", "vehicle", "customer", "date", "status", "total_amount")
    list_filter = ("status", "date")
    search_fields = (
        "workorder_id",
        "vehicle__vehicle_plate",
        "customer__customer_name",
    )
    inlines = [WorkOrderItemInline]


@admin.register(WorkOrderItem)
class WorkOrderItemAdmin(admin.ModelAdmin):
    list_display = ("work_order", "product", "quantity", "unit_price", "discount", "total_line")
