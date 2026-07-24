from django.urls import path
from . import views

app_name = 'professores'

urlpatterns = [
    path('', views.ProfessorListView.as_view(), name='list'),
    path('novo/', views.ProfessorCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.ProfessorUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.ProfessorDeleteView.as_view(), name='delete'),
]
