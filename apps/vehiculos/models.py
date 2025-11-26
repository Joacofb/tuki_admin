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


class Vehicle(models.Model):
    vehicle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vehicle_brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    vehicle_model = models.CharField(max_length=255)
    vehicle_version = models.CharField(max_length=255)
    vehicle_production = models.CharField(max_length=50)
    vehicle_details = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.vehicle_brand} - {self.vehicle_model} - {self.vehicle_version}'

