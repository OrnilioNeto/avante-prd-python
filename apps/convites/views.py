from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from .models import ConviteAluno
from apps.alunos.models import Aluno
from apps.accounts.models import User
from apps.parametros.models import Modalidade


class ConviteListView(LoginRequiredMixin, ListView):
    model = ConviteAluno
    template_name = 'convites/convite_list.html'
    context_object_name = 'convites'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['base_url'] = f"{self.request.scheme}://{self.request.get_host()}"
        return ctx


class ConviteCreateView(LoginRequiredMixin, CreateView):
    model = ConviteAluno
    template_name = 'convites/convite_form.html'
    fields = ['filial', 'max_uses', 'expires_at']
    success_url = reverse_lazy('convites:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ConviteDeleteView(LoginRequiredMixin, DeleteView):
    model = ConviteAluno
    success_url = reverse_lazy('convites:list')


class ConviteToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        convite = get_object_or_404(ConviteAluno, pk=pk)
        convite.active = not convite.active
        convite.save()
        return redirect('convites:list')


class ConviteRegisterView(View):
    template_name = 'convites/convite_register.html'

    def get(self, request, token):
        convite = get_object_or_404(ConviteAluno, token=token, active=True)
        if convite.expires_at < timezone.now():
            return render(request, self.template_name, {'error': 'Este convite expirou.', 'convite': convite})
        if convite.max_uses and convite.use_count >= convite.max_uses:
            return render(request, self.template_name, {'error': 'Este convite já atingiu o limite de usos.', 'convite': convite})
        modalidades = Modalidade.objects.filter(ativo=True).order_by('nome')
        return render(request, self.template_name, {'convite': convite, 'modalidades': modalidades})

    def post(self, request, token):
        convite = get_object_or_404(ConviteAluno, token=token, active=True)
        if convite.expires_at < timezone.now():
            return render(request, self.template_name, {'error': 'Este convite expirou.', 'convite': convite})
        if convite.max_uses and convite.use_count >= convite.max_uses:
            return render(request, self.template_name, {'error': 'Este convite já atingiu o limite de usos.', 'convite': convite})

        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf', '')
        data_nascimento = request.POST.get('data_nascimento')
        telefone = request.POST.get('telefone', '')
        email = request.POST.get('email', '')
        data_inicio = request.POST.get('data_inicio')
        modalidades_ids = request.POST.getlist('modalidades')
        tem_responsavel = request.POST.get('tem_responsavel') == 'true'

        errors = {}
        if not nome:
            errors['nome'] = 'Nome é obrigatório.'
        if not data_nascimento:
            errors['data_nascimento'] = 'Data de nascimento é obrigatória.'
        if not telefone:
            errors['telefone'] = 'Telefone é obrigatório.'
        if not email:
            errors['email'] = 'E-mail é obrigatório.'
        if not data_inicio:
            errors['data_inicio'] = 'Data de início é obrigatória.'
        if not modalidades_ids:
            errors['modalidades'] = 'Selecione ao menos uma modalidade.'
        if cpf and User.objects.filter(cpf=cpf).exists():
            errors['cpf'] = 'Este CPF já está cadastrado.'

        if errors:
            modalidades = Modalidade.objects.filter(ativo=True).order_by('nome')
            ctx = {'convite': convite, 'errors': errors, 'data': request.POST, 'modalidades': modalidades}
            return render(request, self.template_name, ctx)

        user = User.objects.create_user(
            username=cpf or email,
            email=email,
            password='123456',
            first_name=nome.split()[0] if nome else '',
            last_name=' '.join(nome.split()[1:]) if len(nome.split()) > 1 else '',
            cpf=cpf or '',
            telefone=telefone,
            role='aluno',
            filial=convite.filial,
        )

        Aluno.objects.create(
            nome=nome,
            data_nascimento=data_nascimento,
            telefone=telefone,
            email=email,
            cpf=cpf or '',
            data_inicio=data_inicio,
            faixa='Branca',
            grau=0,
            status='ativo',
            filial=convite.filial,
            modalidades=modalidades_ids,
            tem_responsavel=tem_responsavel,
            responsavel_nome=request.POST.get('responsavel_nome', ''),
            responsavel_cpf=request.POST.get('responsavel_cpf', ''),
            responsavel_telefone=request.POST.get('responsavel_telefone', ''),
        )

        convite.use_count += 1
        convite.used_at = timezone.now()
        convite.save()

        login(request, user)
        return redirect('core:dashboard')
