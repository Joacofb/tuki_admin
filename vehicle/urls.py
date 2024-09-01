from django.urls import path
from . import views

app_name = 'vehicle'

urlpatterns = [
    path('all/', views.all_vehicles, name='all'),
    path('add/', views.add_vehicle, name='add'),
]
