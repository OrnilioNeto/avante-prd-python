from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/mensalidades-atrasadas/', views.mensalidades_atrasadas, name='mensalidades_atrasadas'),
    path('professor/financeiro/', views.financeiro, name='financeiro'),
    path('__deploy__/', views.deploy_view, name='deploy'),
]
