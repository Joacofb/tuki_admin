# workorder/models.py
import uuid
from decimal import Decimal

from django.db import models


class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('open', 'Abierto'),
        ('closed', 'Cerrado'),
        ('quoted', 'Presupuestado'),
        ('cancelled', 'Cancelado'),
    ]

    workorder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    vehicle = models.ForeignKey(
        'vehiculos.Vehicle',
        related_name='workorders',
        on_delete=models.CASCADE,
    )

    # redundante pero práctico para reportes
    customer = models.ForeignKey(
        'customer.Customer',
        related_name='workorders',
        on_delete=models.CASCADE,
    )

    date = models.DateField(auto_now_add=True)
    mileage = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='open',
    )

    # Lo podrías calcular, pero te dejo el campo por si quieres guardar snapshot
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"WO {self.workorder_id} - {self.vehicle} - {self.date}"


class WorkOrderItem(models.Model):
    workorderitem_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    work_order = models.ForeignKey(
        WorkOrder,
        related_name='items',
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        'product.Product',
        related_name='workorder_items',
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

    # opcional: puedes calcularlo en save() si quieres
    total_line = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.unit_price is not None:
            subtotal = self.unit_price * self.quantity
            self.total_line = subtotal - (self.discount or Decimal('0.00'))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} x{self.quantity} ({self.work_order_id})"
