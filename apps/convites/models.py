import secrets
from django.db import models
from apps.filiais.models import Filial


class ConviteAluno(models.Model):
    token = models.CharField(max_length=64, unique=True, default=secrets.token_urlsafe)
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    filial = models.ForeignKey(Filial, on_delete=models.CASCADE, verbose_name='Filial')
    expires_at = models.DateTimeField(verbose_name='Expira Em')
    max_uses = models.IntegerField(null=True, blank=True, verbose_name='Usos Máximos', help_text='Deixe em branco para ilimitado')
    use_count = models.IntegerField(default=0, verbose_name='Usos Atuais')
    active = models.BooleanField(default=True, verbose_name='Ativo')
    used_at = models.DateTimeField(null=True, blank=True, verbose_name='Usado Em')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Convite'
        verbose_name_plural = 'Convites'

    def __str__(self):
        return f'Convite {self.token[:8]}... ({self.filial})'
