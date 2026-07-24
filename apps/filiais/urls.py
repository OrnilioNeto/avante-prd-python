from django.urls import path
from . import views

app_name = 'filiais'

urlpatterns = [
    path('', views.FilialListView.as_view(), name='list'),
    path('novo/', views.FilialCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.FilialUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.FilialDeleteView.as_view(), name='delete'),
]
