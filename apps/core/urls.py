from django.urls import path
from . import views
from apps.alunos import views as alunos_views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('meu-painel/', views.minha_conta, name='minha_conta'),
    path('responsavel/', views.responsavel_dashboard, name='responsavel_dashboard'),
    path('minha-conta/', views.minha_conta),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
    path('professor/mensalidades-atrasadas/', views.mensalidades_atrasadas, name='mensalidades_atrasadas'),
    path('professor/financeiro/', views.financeiro, name='financeiro'),
    path('upload-profile-photo/', views.upload_profile_photo, name='upload_profile_photo'),
    path('presenca/', alunos_views.registrar_presenca, name='registrar_presenca'),
    path('cartao/<int:aluno_id>/', alunos_views.cartao_atleta, name='cartao_atleta'),
    path('__deploy__/', views.deploy_view, name='deploy'),
    path('__test-email__/', views.test_email, name='test_email'),
]
