from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('clients/', views.client_list, name='client_list'),
    path('handovers/', views.handover_list, name='handover_list'),
    path('engineer-handoffs/', views.engineer_handoff_list, name='engineer_handoff_list'),
]
