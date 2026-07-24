from django.urls import path
from . import views

app_name = 'convites'

urlpatterns = [
    path('', views.ConviteListView.as_view(), name='list'),
    path('novo/', views.ConviteCreateView.as_view(), name='create'),
    path('<int:pk>/excluir/', views.ConviteDeleteView.as_view(), name='delete'),
]
