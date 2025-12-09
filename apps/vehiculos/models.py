import uuid
from django.db import models

BRAND_CHOICES = [
    ('ALFA ROMEO', 'ALFA ROMEO'),
    ('AUDI', 'AUDI'),
    ('CHERY', 'CHERY'),
    ('CITROEN', 'CITROEN'),
    ('CHEVROLET', 'CHEVROLET'),
    ('DODGE', 'DODGE'),
    ('IKA', 'IKA'),
    ('OPEL', 'OPEL'),
    ('FIAT', 'FIAT'),
    ('FORD', 'FORD'),
    ('PEUGEOT', 'PEUGEOT'),
    ('RASTROJERO', 'RASTROJERO'),
    ('RENAULT', 'RENAULT'),
    ('HONDA', 'HONDA'),
    ('SUSUKI', 'SUSUKI'),
    ('TOYOTA', 'TOYOTA'),
    ('VOLKSWAGEN', 'VOLKSWAGEN'),
]


class VehicleModel(models.Model):
    vehiclemodel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehiclemodel_brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    vehiclemodel_name = models.CharField(max_length=255)
    vehiclemodel_version = models.CharField(max_length=255)
    vehiclemodel_production = models.CharField(max_length=50)
    vehiclemodel_details = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Vehicle model"
        verbose_name_plural = "Vehicle models"

    def __str__(self):
        return f'{self.vehiclemodel_brand} - {self.vehiclemodel_name} - {self.vehiclemodel_version}'

from customer.models import Customer

class Vehicle(models.Model):
    vehicle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Nuevo: el duenio del auto
    vehicle_customer = models.ForeignKey(
        'customer.Customer',
        related_name='vehicles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Nuevo: el tipo de vehiculo
    vehicle_model = models.ForeignKey(
        VehicleModel,
        related_name='vehicles',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Patente del auto concreto
    vehicle_plate = models.CharField(max_length=7, blank=True, null=True)

    vehicle_color = models.CharField(max_length=30, blank=True, null=True)
    vehicle_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        base = f"{self.vehicle_plate or ''} - {self.vehicle_customer or ''}".strip(" -")
        return base or str(self.vehicle_id)