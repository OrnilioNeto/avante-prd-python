from django.contrib import admin
from .models import Aluno, GraduacaoAluno, MensalidadePagamento

admin.site.register(Aluno)
admin.site.register(GraduacaoAluno)
admin.site.register(MensalidadePagamento)
