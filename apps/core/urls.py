from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('minha-conta/', views.minha_conta, name='minha_conta'),
    path('__deploy__/', views.deploy_view, name='deploy'),
]
