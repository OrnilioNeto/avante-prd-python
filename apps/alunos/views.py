from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from .models import Aluno, MensalidadePagamento, GraduacaoAluno
from apps.parametros.models import Modalidade, HorarioTreino


class AlunoListView(LoginRequiredMixin, ListView):
    model = Aluno
    template_name = 'alunos/aluno_list.html'
    context_object_name = 'alunos'
    paginate_by = 50


class AlunoCreateView(LoginRequiredMixin, CreateView):
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


class AlunoUpdateView(LoginRequiredMixin, UpdateView):
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


class AlunoDetailView(LoginRequiredMixin, DetailView):
    model = Aluno
    template_name = 'alunos/aluno_detail.html'
    context_object_name = 'aluno'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['pagamentos'] = MensalidadePagamento.objects.filter(aluno=self.object)
        ctx['graduacoes'] = GraduacaoAluno.objects.filter(aluno=self.object)
        return ctx


class MensalidadeCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        referencia_mes = request.POST.get('referencia_mes')
        vencimento_em = request.POST.get('vencimento_em')
        valor = request.POST.get('valor')
        pago_em = request.POST.get('pago_em') or None
        observacao = request.POST.get('observacao', '')

        MensalidadePagamento.objects.create(
            aluno=aluno,
            user=request.user,
            referencia_mes=referencia_mes,
            vencimento_em=vencimento_em,
            valor=valor,
            pago_em=pago_em,
            observacao=observacao,
        )
        return redirect('alunos:detail', pk=pk)


class MensalidadeDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        pagamento = get_object_or_404(MensalidadePagamento, pk=pk)
        aluno_pk = pagamento.aluno.pk
        pagamento.delete()
        return redirect('alunos:detail', pk=aluno_pk)


class GraduacaoCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        faixa_nova = request.POST.get('faixa_nova')
        grau_novo = request.POST.get('grau_novo')
        graduado_em = request.POST.get('graduado_em')
        observacao = request.POST.get('observacao', '')

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
        aluno.save()

        return redirect('alunos:detail', pk=pk)
