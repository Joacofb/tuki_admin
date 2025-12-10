from django.urls import path
from . import views

app_name = 'workorder'

urlpatterns = [
    path('<uuid:workorder_id>/', views.workorder, name='workorder'),
    path('add/<uuid:vehicle_id>/', views.add_workorder_for_vehicle, name='add_for_vehicle')
    ]
