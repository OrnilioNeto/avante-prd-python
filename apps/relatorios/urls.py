from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

app_name = 'relatorios'

urlpatterns = [
    path('atrasados/', login_required(lambda request: render(request, 'relatorios/alunos_atrasados.html')), name='atrasados'),
]
