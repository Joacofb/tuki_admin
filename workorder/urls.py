from django.urls import path
from . import views

app_name = 'workorder'

urlpatterns = [
    path('<uuid:workorder_id>/', views.workorder, name='workorder'),
    ]
