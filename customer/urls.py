from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('all/', views.all_customers, name='all'),
]
