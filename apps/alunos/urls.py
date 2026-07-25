from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.AlunoListView.as_view(), name='list'),
    path('novo/', views.AlunoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AlunoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.AlunoUpdateView.as_view(), name='update'),
    path('<int:pk>/mensalidade/', views.MensalidadeCreateView.as_view(), name='mensalidade_create'),
    path('mensalidade/<int:pk>/excluir/', views.MensalidadeDeleteView.as_view(), name='mensalidade_delete'),
    path('<int:pk>/graduacao/', views.GraduacaoCreateView.as_view(), name='graduacao_create'),
    path('qr-code/', views.GerarQRCodeView.as_view(), name='qr_code'),
    path('presenca-manual/', views.registrar_presenca_manual, name='presenca_manual'),
]
