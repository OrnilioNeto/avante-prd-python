from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import ConviteAluno


class ConviteListView(LoginRequiredMixin, ListView):
    model = ConviteAluno
    template_name = 'convites/convite_list.html'
    context_object_name = 'convites'


class ConviteCreateView(LoginRequiredMixin, CreateView):
    model = ConviteAluno
    template_name = 'convites/convite_form.html'
    fields = ['filial', 'expires_at']
    success_url = reverse_lazy('convites:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ConviteDeleteView(LoginRequiredMixin, DeleteView):
    model = ConviteAluno
    success_url = reverse_lazy('convites:list')
