from django.db import models
# from django.core.validators import RegexValidator
import uuid

TYPE_CHOICES = {
    'SALIDAS': 'SM',
    'DELANTEROS': 'SD',
    'INTERMEDIOS': 'SI',
    'TRASEROS': 'ST',
    'COLAS': 'CL',
    'ACCESORIOS': 'AC',
    'DEPORTIVOS': 'DE',
    'MATERIALES': 'MA',
    'INSUMOS': 'IN',
}

TYPE_SUPPLIERS = {
    'GIACCONE': 'GC',
    'PERTOVT': 'PT',
    'TUBOSIL': 'TS',
    'LATINA': 'LT',
    'SILENPRO': 'SP',
    'OTROS': 'OT',
}


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField(blank=True)
    product_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    product_supplier = models.CharField(max_length=100, choices=TYPE_SUPPLIERS)
    product_price = models.DecimalField(max_digits=10, decimal_places=0)
    product_currency = models.CharField(max_length=3, default='ARS')
    product_discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    product_stock = models.IntegerField(default=0)
    product_sku = models.CharField(
        max_length=10, 
        null=True,
        blank=True,
        )
    product_is_active = models.BooleanField(default=True)
    product_related_products = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'{self.product_name} || {self.product_supplier} || {self.product_sku}'
