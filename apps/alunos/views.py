from datetime import datetime, date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from .models import Aluno, MensalidadePagamento, GraduacaoAluno
from apps.parametros.models import Modalidade, HorarioTreino
from apps.core.mixins import RoleFilterMixin, RoleFilterDetailMixin, PermissaoMixin


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
        return super().form_valid(form)


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
