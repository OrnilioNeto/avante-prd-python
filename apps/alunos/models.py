from django.db import models
from apps.filiais.models import Filial


class Aluno(models.Model):
    class Status(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        INATIVO = 'inativo', 'Inativo'
        PAUSADO = 'pausado', 'Pausado'

    nome = models.CharField(max_length=255, verbose_name='Nome')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    email = models.EmailField(blank=True, verbose_name='E-mail')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    data_inicio = models.DateField(verbose_name='Data de Início')
    faixa = models.CharField(max_length=50, verbose_name='Faixa')
    grau = models.IntegerField(default=0, verbose_name='Grau')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVO)
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, verbose_name='Filial')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class GraduacaoAluno(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='graduacoes')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    faixa_anterior = models.CharField(max_length=50, verbose_name='Faixa Anterior')
    grau_anterior = models.IntegerField(verbose_name='Grau Anterior')
    faixa_nova = models.CharField(max_length=50, verbose_name='Faixa Nova')
    grau_novo = models.IntegerField(verbose_name='Grau Novo')
    graduado_em = models.DateField(verbose_name='Graduado Em')
    observacao = models.TextField(blank=True, verbose_name='Observação')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Graduação'
        verbose_name_plural = 'Graduações'
        ordering = ['-graduado_em']

    def __str__(self):
        return f'{self.aluno}: {self.faixa_anterior} -> {self.faixa_nova}'


class MensalidadePagamento(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='pagamentos')
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    referencia_mes = models.DateField(verbose_name='Mês de Referência')
    vencimento_em = models.DateField(verbose_name='Vencimento')
    pago_em = models.DateField(null=True, blank=True, verbose_name='Pago Em')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    observacao = models.TextField(blank=True, verbose_name='Observação')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-referencia_mes']

    def __str__(self):
        return f'{self.aluno} - {self.referencia_mes.strftime("%m/%Y")}'
