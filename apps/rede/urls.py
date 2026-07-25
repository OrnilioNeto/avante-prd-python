from django.urls import path
from . import views

app_name = 'rede'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('postar/', views.criar_post, name='criar_post'),
    path('post/<int:post_id>/curtir/', views.curtir, name='curtir'),
    path('post/<int:post_id>/comentar/', views.comentar, name='comentar'),
    path('post/<int:pk>/excluir/', views.excluir_post, name='excluir_post'),
    path('seguir/<int:user_id>/', views.seguir, name='seguir'),
    path('perfil/<int:user_id>/', views.perfil, name='perfil'),
    path('seguindo/', views.seguindo, name='seguindo'),
]
