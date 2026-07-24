from django import forms
from django.contrib.auth import get_user_model
from .models import Professor

User = get_user_model()

class ProfessorForm(forms.ModelForm):
    primeiro_nome = forms.CharField(max_length=150, label='Primeiro Nome')
    ultimo_nome = forms.CharField(max_length=150, label='Ultimo Nome')
    email = forms.EmailField(label='E-mail')
    cpf = forms.CharField(max_length=14, label='CPF')
    telefone = forms.CharField(max_length=20, required=False, label='Telefone')

    class Meta:
        model = Professor
        fields = ['filiais', 'faixa', 'grau']
        labels = {
            'filiais': 'Filiais',
            'faixa': 'Faixa',
            'grau': 'Grau',
        }

    def save(self, commit=True):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['cpf'],
            email=data['email'],
            password='123456',
            first_name=data['primeiro_nome'],
            last_name=data['ultimo_nome'],
            cpf=data['cpf'],
            telefone=data.get('telefone', ''),
            role='professor',
        )
        professor = super().save(commit=False)
        professor.user = user
        if commit:
            professor.save()
            self.save_m2m()
        return professor