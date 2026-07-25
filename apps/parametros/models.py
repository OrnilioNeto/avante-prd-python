from django.db import models


class Modalidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Modalidade'
        verbose_name_plural = 'Modalidades'

    def __str__(self):
        return self.nome


class HorarioTreino(models.Model):
    descricao = models.CharField(max_length=255, verbose_name='Descrição')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Horário de Treino'
        verbose_name_plural = 'Horários de Treino'

    def __str__(self):
        return self.descricao


class GraduacaoParametro(models.Model):
    faixa = models.CharField(max_length=50, verbose_name='Faixa')
    grau = models.IntegerField(verbose_name='Grau')
    meses_para_proxima_graduacao = models.IntegerField(verbose_name='Meses p/ Próxima Graduação')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Parâmetro de Graduação'
        verbose_name_plural = 'Parâmetros de Graduação'
        ordering = ['faixa', 'grau']

    def __str__(self):
        return f'{self.faixa} {self.grau} - {self.meses_para_proxima_graduacao} meses'


PERMISSOES_CHOICES = [
    ('ver_alunos', 'Ver Alunos'),
    ('criar_alunos', 'Criar Alunos'),
    ('editar_alunos', 'Editar Alunos'),
    ('ver_financeiro', 'Ver Financeiro'),
    ('registrar_pagamento', 'Registrar Pagamento'),
    ('excluir_pagamento', 'Excluir Pagamento'),
    ('registrar_graduacao', 'Registrar Graduação'),
    ('ver_relatorios', 'Ver Relatórios'),
    ('gerenciar_convites', 'Gerenciar Convites'),
    ('gerenciar_parametros', 'Gerenciar Parâmetros'),
    ('ver_dashboard', 'Ver Dashboard'),
]


class PerfilAcesso(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome do Perfil')
    permissoes = models.JSONField(default=list, blank=True, verbose_name='Permissões')
    is_admin = models.BooleanField(default=False, verbose_name='Acesso Administrativo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil de Acesso'
        verbose_name_plural = 'Perfis de Acesso'

    def __str__(self):
        return self.nome

    def has_permissao(self, permissao):
        if self.is_admin:
            return True
        return permissao in self.permissoes


class AcademiaParametro(models.Model):
    secao = models.CharField(max_length=100, verbose_name='Secao')
    titulo = models.CharField(max_length=150, verbose_name='Titulo')
    tipo = models.CharField(max_length=50, verbose_name='Tipo')
    idade_min = models.IntegerField(null=True, blank=True, verbose_name='Idade Minima')
    idade_max = models.IntegerField(null=True, blank=True, verbose_name='Idade Maxima')
    conteudo = models.TextField(blank=True, verbose_name='Conteudo')
    ordem = models.IntegerField(default=0, verbose_name='Ordem')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Parametro da Academia'
        verbose_name_plural = 'Parametros da Academia'
        ordering = ['secao', 'ordem', 'titulo']

    def __str__(self):
        return f'[{self.secao}] {self.titulo}'
