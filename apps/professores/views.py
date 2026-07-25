from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Professor
from .forms import ProfessorForm
from apps.core.mixins import AdminRequiredMixin


class ProfessorListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Professor
    template_name = 'professores/professor_list.html'
    context_object_name = 'professores'


class ProfessorCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'professores/professor_form.html'
    success_url = reverse_lazy('professores:list')


class ProfessorUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Professor
    form_class = ProfessorForm
    template_name = 'professores/professor_form.html'
    success_url = reverse_lazy('professores:list')


class ProfessorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Professor
    success_url = reverse_lazy('professores:list')
