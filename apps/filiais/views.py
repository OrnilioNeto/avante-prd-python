from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Filial


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'super_admin'


class FilialListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Filial
    template_name = 'filiais/filial_list.html'
    context_object_name = 'filiais'


class FilialCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Filial
    template_name = 'filiais/filial_form.html'
    fields = '__all__'
    success_url = reverse_lazy('filiais:list')


class FilialUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Filial
    template_name = 'filiais/filial_form.html'
    fields = '__all__'
    success_url = reverse_lazy('filiais:list')


class FilialDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Filial
    template_name = 'filiais/filial_confirm_delete.html'
    success_url = reverse_lazy('filiais:list')
