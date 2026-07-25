from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    path('filiais/', include('apps.filiais.urls')),
    path('professores/', include('apps.professores.urls')),
    path('alunos/', include('apps.alunos.urls')),
    path('convites/', include('apps.convites.urls')),
    path('parametros/', include('apps.parametros.urls')),
    path('relatorios/', include('apps.relatorios.urls')),
    path('midias/', include('apps.midia.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)