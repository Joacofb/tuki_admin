import uuid

from django.db import models
from vehicle.models import Vehicle
from django.core.exceptions import ValidationError


def validate_carid_length(value):
    if len(value) < 6:
        raise ValidationError('La patente debe contener al menos 6 caracteres.')


class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100)
    # HACERLAS OPCIONALES
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    customer_address = models.CharField(max_length=100, blank=True, null=True)
    customer_carid = models.CharField(max_length=7, validators=[validate_carid_length])
    customer_vehicleid = models.ForeignKey(Vehicle, related_name='customer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.customer_carid} || {self.customer_name} || {self.customer_phone}'
    #
    # def get_works(self):
    #     return self.works.all()
