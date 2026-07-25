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
        fields = ['filiais', 'perfil_acesso', 'faixa', 'grau']
        labels = {
            'filiais': 'Filiais',
            'perfil_acesso': 'Perfil de Acesso',
            'faixa': 'Faixa',
            'grau': 'Grau',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user:
            self.fields['primeiro_nome'].initial = self.instance.user.first_name
            self.fields['ultimo_nome'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['cpf'].initial = self.instance.user.cpf
            self.fields['telefone'].initial = self.instance.user.telefone
            self.fields['cpf'].widget.attrs['readonly'] = True

    def save(self, commit=True):
        data = self.cleaned_data
        professor = super().save(commit=False)
        if professor.pk and professor.user:
            user = professor.user
            user.first_name = data['primeiro_nome']
            user.last_name = data['ultimo_nome']
            user.email = data['email']
            user.cpf = data['cpf']
            user.telefone = data.get('telefone', '')
            if commit:
                user.save()
        else:
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
            professor.user = user
        if commit:
            professor.save()
            self.save_m2m()
        return professor