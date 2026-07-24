from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('', views.AlunoListView.as_view(), name='list'),
    path('novo/', views.AlunoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.AlunoDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.AlunoUpdateView.as_view(), name='update'),
]
