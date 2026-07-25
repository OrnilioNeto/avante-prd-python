from django.contrib import admin
from .models import Aluno, GraduacaoAluno, MensalidadePagamento, Presenca

admin.site.register(Aluno)
admin.site.register(GraduacaoAluno)
admin.site.register(MensalidadePagamento)
admin.site.register(Presenca)
