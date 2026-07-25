from django.db import models
from apps.filiais.models import Filial


class Professor(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='professor_profile')
    filiais = models.ManyToManyField(Filial, related_name='professores', blank=True)
    perfil_acesso = models.ForeignKey('parametros.PerfilAcesso', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Perfil de Acesso')
    faixa = models.CharField(max_length=50, verbose_name='Faixa')
    grau = models.IntegerField(default=0, verbose_name='Grau')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def has_permissao(self, permissao):
        if self.perfil_acesso:
            return self.perfil_acesso.has_permissao(permissao)
        return False
