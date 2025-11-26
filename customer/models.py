import uuid
from django.db import models


class Customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    customer_address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.customer_name
    