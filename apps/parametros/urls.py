from django.urls import path
from . import views

app_name = 'parametros'

urlpatterns = [
    path('', views.ParametroListView.as_view(), name='list'),
    path('modalidade/criar/', views.ModalidadeCreateView.as_view(), name='modalidade_create'),
    path('modalidade/<int:pk>/excluir/', views.ModalidadeDeleteView.as_view(), name='modalidade_delete'),
    path('horario/criar/', views.HorarioCreateView.as_view(), name='horario_create'),
    path('horario/<int:pk>/excluir/', views.HorarioDeleteView.as_view(), name='horario_delete'),
    path('graduacao/criar/', views.GraduacaoCreateView.as_view(), name='graduacao_create'),
    path('graduacao/<int:pk>/excluir/', views.GraduacaoDeleteView.as_view(), name='graduacao_delete'),
    path('academia/criar/', views.AcademiaParametroCreateView.as_view(), name='academia_create'),
    path('academia/<int:pk>/excluir/', views.AcademiaParametroDeleteView.as_view(), name='academia_delete'),
]