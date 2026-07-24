from django.db import models


class Filial(models.Model):
    class Status(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        INATIVO = 'inativo', 'Inativo'

    nome = models.CharField(max_length=255, verbose_name='Nome')
    is_filial = models.BooleanField(default=True, verbose_name='É Filial?')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVO)
    rua = models.CharField(max_length=255, blank=True, verbose_name='Rua')
    numero = models.CharField(max_length=20, blank=True, verbose_name='Número')
    bairro = models.CharField(max_length=255, blank=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=255, blank=True, verbose_name='Cidade')
    cep = models.CharField(max_length=10, blank=True, verbose_name='CEP')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'
        ordering = ['nome']

    def __str__(self):
        return self.nome
