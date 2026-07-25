from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'super_admin', 'Super Administrador'
        PROFESSOR = 'professor', 'Professor'
        ALUNO = 'aluno', 'Aluno'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ALUNO)
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    must_change_password = models.BooleanField(default=True, verbose_name='Deve trocar a senha')
    filial = models.ForeignKey('filiais.Filial', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Filial')
    faixa = models.CharField(max_length=50, blank=True, verbose_name='Faixa')
    grau = models.IntegerField(default=0, verbose_name='Grau')
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, verbose_name='Foto de Perfil')
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def has_permissao(self, permissao):
        if self.is_superuser or self.role == 'super_admin':
            return True
        if self.role == 'professor':
            try:
                profile = self.professor_profile
                if profile.perfil_acesso:
                    return profile.has_permissao(permissao)
            except:
                pass
        return self.role == 'aluno' and permissao == 'ver_alunos'

    def __str__(self):
        return f'{self.get_full_name()} ({self.get_role_display()})'
