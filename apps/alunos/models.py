import uuid

from django.db import models
from django.utils.crypto import get_random_string
from apps.filiais.models import Filial
from apps.parametros.models import Modalidade, HorarioTreino


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
    codigo = models.CharField(max_length=10, unique=True, blank=True, verbose_name='Código do Aluno')
    data_inicio = models.DateField(verbose_name='Data de Início')
    modalidades = models.JSONField(null=True, blank=True, verbose_name='Modalidades')
    faixa = models.CharField(max_length=50, verbose_name='Faixa')
    grau = models.IntegerField(default=0, verbose_name='Grau')
    data_ultima_graduacao = models.DateField(null=True, blank=True, verbose_name='Última Graduação')
    horario_treino = models.ForeignKey(HorarioTreino, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Horário de Treino')
    dia_vencimento = models.IntegerField(null=True, blank=True, verbose_name='Dia do Vencimento')
    valor_mensalidade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor da Mensalidade')
    tem_responsavel = models.BooleanField(default=False, verbose_name='Tem Responsável')
    responsavel_nome = models.CharField(max_length=255, blank=True, verbose_name='Nome do Responsável')
    responsavel_cpf = models.CharField(max_length=14, blank=True, verbose_name='CPF do Responsável')
    responsavel_telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone do Responsável')
    responsavel_telefone2 = models.CharField(max_length=20, blank=True, verbose_name='Telefone 2 do Responsável')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ATIVO)
    filial = models.ForeignKey(Filial, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Filial')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            while True:
                code = 'A' + get_random_string(4, '0123456789')
                if not Aluno.objects.filter(codigo=code).exists():
                    self.codigo = code
                    break
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']

    @property
    def filial_nome(self):
        return self.filial.nome if self.filial else '-'

    @property
    def horario_treino_descricao(self):
        return self.horario_treino.descricao if self.horario_treino else '-'

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


class Presenca(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='presencas')
    data = models.DateField(verbose_name='Data')
    marcado_por = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
        unique_together = ('aluno', 'data')
        ordering = ['-data']

    def __str__(self):
        return f'{self.aluno} - {self.data}'
