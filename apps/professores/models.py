from django.db import models
from apps.filiais.models import Filial


class Professor(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='professor_profile')
    filiais = models.ManyToManyField(Filial, related_name='professores', blank=True)
    faixa = models.CharField(max_length=50, verbose_name='Faixa')
    grau = models.IntegerField(default=0, verbose_name='Grau')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

    def __str__(self):
        return self.user.get_full_name() or self.user.username
