from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from .models import Aluno, MensalidadePagamento, GraduacaoAluno, Presenca
from apps.accounts.models import User
from apps.parametros.models import Modalidade, HorarioTreino
from apps.core.mixins import RoleFilterMixin, RoleFilterDetailMixin, PermissaoMixin
from io import BytesIO
import base64


class AlunoListView(LoginRequiredMixin, PermissaoMixin, RoleFilterMixin, ListView):
    permission_required = 'ver_alunos'
    model = Aluno
    template_name = 'alunos/aluno_list.html'
    context_object_name = 'alunos'
    paginate_by = 50


class AlunoCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'criar_alunos'
    model = Aluno
    template_name = 'alunos/aluno_form.html'
    fields = '__all__'
    success_url = reverse_lazy('alunos:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['modalidades'] = Modalidade.objects.filter(ativo=True)
        ctx['horarios'] = HorarioTreino.objects.filter(ativo=True)
        ctx['modalidades_selecionadas'] = []
        return ctx

    def form_valid(self, form):
        modalidades_ids = self.request.POST.getlist('modalidades')
        if modalidades_ids:
            form.instance.modalidades = [int(x) for x in modalidades_ids]
        response = super().form_valid(form)
        aluno = self.object
        cpf_limpo = aluno.cpf.replace('.', '').replace('-', '')
        username = cpf_limpo if not User.objects.filter(username=cpf_limpo).exists() else f'aluno_{aluno.pk}'
        if not User.objects.filter(cpf=aluno.cpf).exists():
            User.objects.create_user(
                username=username,
                cpf=aluno.cpf,
                email=aluno.email or '',
                first_name=aluno.nome.split()[0] if aluno.nome.split() else aluno.nome,
                last_name=' '.join(aluno.nome.split()[1:]) if len(aluno.nome.split()) > 1 else '',
                role='aluno',
                password=cpf_limpo,
                must_change_password=True,
            )
        return response


class AlunoUpdateView(LoginRequiredMixin, PermissaoMixin, UpdateView):
    permission_required = 'editar_alunos'
    model = Aluno
    template_name = 'alunos/aluno_form.html'
    fields = '__all__'
    success_url = reverse_lazy('alunos:list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['modalidades'] = Modalidade.objects.filter(ativo=True)
        ctx['horarios'] = HorarioTreino.objects.filter(ativo=True)
        ctx['modalidades_selecionadas'] = self.object.modalidades or []
        return ctx

    def form_valid(self, form):
        modalidades_ids = self.request.POST.getlist('modalidades')
        if modalidades_ids:
            form.instance.modalidades = [int(x) for x in modalidades_ids]
        else:
            form.instance.modalidades = []
        return super().form_valid(form)


FAIXAS_ORDER = ['Branca', 'Azul', 'Roxa', 'Marrom', 'Preta']

class AlunoDetailView(LoginRequiredMixin, PermissaoMixin, RoleFilterDetailMixin, DetailView):
    permission_required = 'ver_alunos'
    model = Aluno
    template_name = 'alunos/aluno_detail.html'
    context_object_name = 'aluno'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pagamentos'] = MensalidadePagamento.objects.filter(aluno=self.object)
        ctx['graduacoes'] = GraduacaoAluno.objects.filter(aluno=self.object)
        ctx['faixas'] = FAIXAS_ORDER
        aluno = self.object
        try:
            idx = FAIXAS_ORDER.index(aluno.faixa)
        except ValueError:
            idx = -1
        if aluno.grau >= 4 and idx >= 0 and idx < len(FAIXAS_ORDER) - 1:
            ctx['sugestao_faixa'] = FAIXAS_ORDER[idx + 1]
            ctx['sugestao_grau'] = 0
        else:
            ctx['sugestao_faixa'] = aluno.faixa
            ctx['sugestao_grau'] = aluno.grau + 1
        return ctx


class MensalidadeCreateView(LoginRequiredMixin, PermissaoMixin, View):
    permission_required = 'registrar_pagamento'
    def post(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        from decimal import Decimal
        pago_em_str = request.POST.get('pago_em')
        pago_em = datetime.strptime(pago_em_str, '%Y-%m-%d').date() if pago_em_str else date.today()
        valor = Decimal(request.POST.get('valor'))

        dia_venc = aluno.dia_vencimento or 5
        referencia_mes = date(pago_em.year, pago_em.month, 1)
        try:
            vencimento_em = date(pago_em.year, pago_em.month, dia_venc)
        except ValueError:
            from calendar import monthrange
            ultimo_dia = monthrange(pago_em.year, pago_em.month)[1]
            vencimento_em = date(pago_em.year, pago_em.month, min(dia_venc, ultimo_dia))

        existing = MensalidadePagamento.objects.filter(
            aluno=aluno, referencia_mes=referencia_mes, pago_em__isnull=True
        ).first()
        if existing:
            existing.pago_em = pago_em
            existing.valor = valor
            existing.save()
        else:
            MensalidadePagamento.objects.create(
                aluno=aluno,
                user=request.user,
                referencia_mes=referencia_mes,
                vencimento_em=vencimento_em,
                valor=valor,
                pago_em=pago_em,
            )
        return redirect('alunos:detail', pk=pk)


class MensalidadeDeleteView(LoginRequiredMixin, PermissaoMixin, View):
    permission_required = 'excluir_pagamento'
    def post(self, request, pk):
        pagamento = get_object_or_404(MensalidadePagamento, pk=pk)
        aluno_pk = pagamento.aluno.pk
        pagamento.delete()
        return redirect('alunos:detail', pk=aluno_pk)


class GraduacaoCreateView(LoginRequiredMixin, PermissaoMixin, View):
    permission_required = 'registrar_graduacao'
    def post(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        faixa_nova = request.POST.get('faixa_nova') or aluno.faixa
        grau_novo_str = request.POST.get('grau_novo')
        graduado_em_str = request.POST.get('graduado_em')
        observacao = request.POST.get('observacao', '')

        grau_novo = int(grau_novo_str)
        graduado_em = datetime.strptime(graduado_em_str, '%Y-%m-%d').date()

        GraduacaoAluno.objects.create(
            aluno=aluno,
            user=request.user,
            faixa_anterior=aluno.faixa,
            grau_anterior=aluno.grau,
            faixa_nova=faixa_nova,
            grau_novo=grau_novo,
            graduado_em=graduado_em,
            observacao=observacao,
        )

        aluno.faixa = faixa_nova
        aluno.grau = grau_novo
        aluno.data_ultima_graduacao = graduado_em
        aluno.save()

        return redirect('alunos:detail', pk=pk)


class GerarQRCodeView(LoginRequiredMixin, View):
    def get(self, request):
        import qrcode
        qr_url = request.build_absolute_uri('/presenca/')
        img = qrcode.make(qr_url)
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        return render(request, 'alunos/qr_code.html', {
            'qr_data_url': f'data:image/png;base64,{b64}',
            'qr_url': qr_url,
        })


def registrar_presenca(request):
    erro = None
    aluno = None
    presenca_hoje = False

    if request.method == 'POST':
        cpf = request.POST.get('cpf', '').strip()
        codigo = request.POST.get('codigo', '').strip()
        q = Aluno.objects.filter(status='ativo')
        if cpf:
            cpf_clean = cpf.replace('.', '').replace('-', '')
            alunos = q.filter(cpf__contains=cpf_clean)
        elif codigo:
            alunos = q.filter(codigo__iexact=codigo)
        else:
            alunos = Aluno.objects.none()
            erro = 'Informe CPF ou Código do Aluno.'

        if alunos and not erro:
            aluno = alunos.first()
            hoje = date.today()
            if Presenca.objects.filter(aluno=aluno, data=hoje).exists():
                erro = f'{aluno.nome} já teve presença registrada hoje.'
                presenca_hoje = True
            else:
                Presenca.objects.create(aluno=aluno, data=hoje)
                return redirect('core:cartao_atleta', aluno_id=aluno.pk)

    return render(request, 'alunos/registrar_presenca.html', {
        'erro': erro,
        'aluno': aluno,
        'presenca_hoje': presenca_hoje,
    })


def cartao_atleta(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    hoje = date.today()

    total_presencas = aluno.presencas.count()
    dias_desde_inicio = (hoje - aluno.data_inicio).days or 1
    assiduidade = round((total_presencas / dias_desde_inicio) * 100, 1)
    if assiduidade > 100:
        assiduidade = 100.0

    from apps.core.views import _get_ranking
    from decimal import Decimal
    faixa_ordem = ['Branca', 'Azul', 'Roxa', 'Marrom', 'Preta']
    total_xp = 0
    for g in aluno.graduacoes.all():
        total_xp += 500
    total_pago = MensalidadePagamento.objects.filter(aluno=aluno, pago_em__isnull=False).aggregate(
        total=models.Sum('valor')
    )['total'] or Decimal('0.00')
    total_xp += int(float(total_pago)) // 10

    ranking = _get_ranking(aluno)
    posicao = None
    ranking_count = 0
    for pk, nome, pts in ranking:
        ranking_count += 1
        if pk == aluno.pk:
            posicao = ranking_count

    pagamentos_em_dia = aluno.pagamentos.filter(pago_em__isnull=False)
    pagamentos_em_atraso = aluno.pagamentos.filter(pago_em__isnull=True, vencimento_em__lt=hoje)

    graduacoes = aluno.graduacoes.all()

    return render(request, 'alunos/cartao_atleta.html', {
        'aluno': aluno,
        'assiduidade': assiduidade,
        'total_presencas': total_presencas,
        'total_xp': total_xp,
        'posicao': posicao,
        'ranking_count': ranking_count,
        'dias_desde_inicio': dias_desde_inicio,
        'pagamentos_em_dia': pagamentos_em_dia,
        'pagamentos_em_atraso': pagamentos_em_atraso,
        'graduacoes': graduacoes,
        'total_pago': total_pago,
        'hoje': hoje,
        'faixas': faixa_ordem,
    })


@login_required
def registrar_presenca_manual(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        data_str = request.POST.get('data', date.today().isoformat())
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        if not Presenca.objects.filter(aluno=aluno, data=data_str).exists():
            Presenca.objects.create(aluno=aluno, data=data_str, marcado_por=request.user)
        return redirect('alunos:presenca_manual')

    alunos = Aluno.objects.filter(status='ativo').order_by('nome')
    hoje = date.today()
    presencas_hoje = Presenca.objects.filter(data=hoje, marcado_por=request.user
    ).select_related('aluno')
    return render(request, 'alunos/presenca_manual.html', {
        'alunos': alunos,
        'presencas_hoje': presencas_hoje,
        'hoje': hoje,
    })
