from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Modalidade, HorarioTreino, GraduacaoParametro, AcademiaParametro, PerfilAcesso
from apps.core.mixins import PermissaoMixin


class ParametroListView(LoginRequiredMixin, PermissaoMixin, ListView):
    permission_required = 'gerenciar_parametros'
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


class ModalidadeCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'gerenciar_parametros'
    model = Modalidade
    fields = ['nome']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class ModalidadeDeleteView(LoginRequiredMixin, PermissaoMixin, DeleteView):
    permission_required = 'gerenciar_parametros'
    model = Modalidade
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


class HorarioCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'gerenciar_parametros'
    model = HorarioTreino
    fields = ['descricao']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class HorarioDeleteView(LoginRequiredMixin, PermissaoMixin, DeleteView):
    permission_required = 'gerenciar_parametros'
    model = HorarioTreino
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


class GraduacaoCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'gerenciar_parametros'
    model = GraduacaoParametro
    fields = ['faixa', 'grau', 'meses_para_proxima_graduacao']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class GraduacaoDeleteView(LoginRequiredMixin, PermissaoMixin, DeleteView):
    permission_required = 'gerenciar_parametros'
    model = GraduacaoParametro
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


class AcademiaParametroCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'gerenciar_parametros'
    model = AcademiaParametro
    fields = ['secao', 'titulo', 'tipo', 'idade_min', 'idade_max', 'conteudo', 'ordem']
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/parametro_form.html'

    def form_valid(self, form):
        form.instance.ativo = True
        return super().form_valid(form)


class AcademiaParametroDeleteView(LoginRequiredMixin, PermissaoMixin, DeleteView):
    permission_required = 'gerenciar_parametros'
    model = AcademiaParametro
    success_url = reverse_lazy('parametros:list')
    template_name = 'parametros/confirm_delete.html'


# ========== PerfilAcesso CRUD ==========

class PerfilAcessoListView(LoginRequiredMixin, PermissaoMixin, ListView):
    permission_required = 'gerenciar_parametros'
    model = PerfilAcesso
    template_name = 'parametros/perfilacesso_list.html'
    context_object_name = 'perfis'


class PerfilAcessoCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'gerenciar_parametros'
    model = PerfilAcesso
    template_name = 'parametros/perfilacesso_form.html'
    fields = ['nome', 'permissoes', 'is_admin']
    success_url = reverse_lazy('parametros:perfil_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import PERMISSOES_CHOICES
        ctx['permissoes_choices'] = PERMISSOES_CHOICES
        ctx['permissoes_selecionadas'] = []
        return ctx

    def form_valid(self, form):
        form.instance.permissoes = self.request.POST.getlist('permissoes')
        return super().form_valid(form)


class PerfilAcessoUpdateView(LoginRequiredMixin, PermissaoMixin, UpdateView):
    permission_required = 'gerenciar_parametros'
    model = PerfilAcesso
    template_name = 'parametros/perfilacesso_form.html'
    fields = ['nome', 'permissoes', 'is_admin']
    success_url = reverse_lazy('parametros:perfil_list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import PERMISSOES_CHOICES
        ctx['permissoes_choices'] = PERMISSOES_CHOICES
        ctx['permissoes_selecionadas'] = self.object.permissoes or []
        return ctx

    def form_valid(self, form):
        form.instance.permissoes = self.request.POST.getlist('permissoes')
        return super().form_valid(form)


class PerfilAcessoDeleteView(LoginRequiredMixin, PermissaoMixin, DeleteView):
    permission_required = 'gerenciar_parametros'
    model = PerfilAcesso
    success_url = reverse_lazy('parametros:perfil_list')
    template_name = 'parametros/confirm_delete.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cancel_url'] = reverse_lazy('parametros:perfil_list')
        return ctx