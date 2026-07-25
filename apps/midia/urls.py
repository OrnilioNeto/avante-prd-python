from django.urls import path
from . import views

app_name = 'midia'

urlpatterns = [
    path('', views.MidiaListView.as_view(), name='list'),
    path('nova/', views.MidiaCreateView.as_view(), name='create'),
    path('<int:pk>/editar/', views.MidiaUpdateView.as_view(), name='update'),
    path('<int:pk>/excluir/', views.MidiaDeleteView.as_view(), name='delete'),
]
