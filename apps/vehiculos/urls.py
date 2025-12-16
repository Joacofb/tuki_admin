from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('all/', views.all_vehicles, name='all'),
    path('allmodels/', views.all_vehiclemodels, name='allmodels'),
    path('add/', views.add_vehicle, name='add'),
    path('add/<uuid:customer_id>/', views.add_vehicle, name='add_for_customer'),
    path('addmodel/', views.add_vehiclemodel, name='addmodel'),
    path('<uuid:vehicle_id>/', views.vehicle, name='vehicle'),
    path('<uuid:vehicle_id>/delete/', views.delete_vehicle, name='delete'),
    path('<uuid:vehicle_id>/edit/', views.edit_vehicle, name='edit'),
]
