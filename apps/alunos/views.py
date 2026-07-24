from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Aluno


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


class AlunoUpdateView(LoginRequiredMixin, UpdateView):
    model = Aluno
    template_name = 'alunos/aluno_form.html'
    fields = '__all__'
    success_url = reverse_lazy('alunos:list')


class AlunoDetailView(LoginRequiredMixin, DetailView):
    model = Aluno
    template_name = 'alunos/aluno_detail.html'
    context_object_name = 'aluno'
