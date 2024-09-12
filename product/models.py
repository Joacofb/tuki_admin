from django.db import models
import uuid

TYPE_CHOICES = {
    'SALIDAS': 'SALIDAS',
    'DELANTEROS': 'DELANTEROS',
    'INTERMEDIOS': 'INTERMEDIOS',
    'TRASEROS': 'TRASEROS',
    'COLAS': 'COLAS',
    'ACCESORIOS': 'ACCESORIOS',
    'DEPORTIVOS': 'DEPORTIVOS',
    'MATERIALES': 'MATERIALES',
    'INSUMOS': 'INSUMOS',
}

TYPE_SUPPLIERS = {
    'GIACCONE': 'GIACCONE',
    'PERTOVT': 'PERTOVT',
    'TUBOSIL': 'TUBOSIL',
    'LATINA': 'LATINA',
    'SILENPRO': 'SILENPRO',
    'OTROS': 'OTROS',
}


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    product_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    product_supplier = models.CharField(max_length=100, choices=TYPE_SUPPLIERS)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_currency = models.CharField(max_length=3, default='ARS')
    product_discount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    product_stock = models.IntegerField(default=0)
    product_sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    product_is_active = models.BooleanField(default=True)
    product_related_products = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return f'{self.product_name} || {self.product_supplier} || {self.product_sku}'
