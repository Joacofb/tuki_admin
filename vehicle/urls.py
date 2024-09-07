from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path('all/', views.all_vehicles, name='all'),
    path('add/', views.add_vehicle, name='add'),
    path('<uuid:vehicle_id>/', views.vehicle, name='vehicle'),
    path('<uuid:vehicle_id>/delete', views.delete_vehicle, name='delete'),
    path('<uuid:vehicle_id>/edit', views.edit_vehicle, name='edit'),
]
