from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Modalidade, HorarioTreino, GraduacaoParametro, AcademiaParametro


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'super_admin'


class ParametroListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = 'parametros/parametro_list.html'

    def get_queryset(self):
        return Modalidade.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modalidades'] = Modalidade.objects.order_by('nome')
        context['horarios'] = HorarioTreino.objects.order_by('descricao')
        context['graduacoes'] = GraduacaoParametro.objects.order_by('faixa', 'grau')
        context['academia_parametros'] = AcademiaParametro.objects.order_by('secao', 'ordem', 'titulo')
        return context


class ModalidadeCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Modalidade
    fields = ['nome']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class ModalidadeDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Modalidade
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


class HorarioCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = HorarioTreino
    fields = ['descricao']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class HorarioDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = HorarioTreino
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


class GraduacaoCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = GraduacaoParametro
    fields = ['faixa', 'grau', 'meses_para_proxima_graduacao']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class GraduacaoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = GraduacaoParametro
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


class AcademiaParametroCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AcademiaParametro
    fields = ['secao', 'titulo', 'tipo', 'idade_min', 'idade_max', 'conteudo', 'ordem']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class AcademiaParametroDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = AcademiaParametro
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'