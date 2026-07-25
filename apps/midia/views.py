from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import MidiaTreino
from apps.core.mixins import PermissaoMixin


class MidiaListView(LoginRequiredMixin, PermissaoMixin, ListView):
    permission_required = 'gerenciar_midia'
    model = MidiaTreino
    template_name = 'midia/midia_list.html'
    context_object_name = 'midias'
    paginate_by = 20


class MidiaCreateView(LoginRequiredMixin, PermissaoMixin, CreateView):
    permission_required = 'gerenciar_midia'
    model = MidiaTreino
    template_name = 'midia/midia_form.html'
    fields = ['titulo', 'descricao', 'tipo', 'arquivo', 'url_youtube', 'data_publicacao']
    success_url = reverse_lazy('midia:list')

    def get_initial(self):
        return {'data_publicacao': date.today()}


class MidiaUpdateView(LoginRequiredMixin, PermissaoMixin, UpdateView):
    permission_required = 'gerenciar_midia'
    model = MidiaTreino
    template_name = 'midia/midia_form.html'
    fields = ['titulo', 'descricao', 'tipo', 'arquivo', 'url_youtube', 'data_publicacao']
    success_url = reverse_lazy('midia:list')


class MidiaDeleteView(LoginRequiredMixin, PermissaoMixin, DeleteView):
    permission_required = 'gerenciar_midia'
    model = MidiaTreino
    template_name = 'midia/midia_confirm_delete.html'
    success_url = reverse_lazy('midia:list')
