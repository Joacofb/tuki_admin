# customer/urls.py
from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path("", views.customer_list, name="list"),
    path("<uuid:customer_id>/", views.customer_detail, name="detail"),
    path("add/", views.add_customer, name="add"),
    path("<uuid:customer_id>/delete", views.delete_customer, name="delete"),
]
