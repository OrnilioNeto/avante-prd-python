from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.filiais.models import Filial
from apps.parametros.models import (
    Modalidade, HorarioTreino, GraduacaoParametro, PerfilAcesso,
)
from apps.professores.models import Professor
from apps.accounts.models import User
from apps.alunos.models import Aluno


def run():
    filial, _ = Filial.objects.get_or_create(
        nome='Avante Unidade 3',
        defaults=dict(
            status='ativo',
            is_filial=True,
            rua='Enock Garcia',
            numero='30',
            bairro='Lagoa Grande',
            cidade='Maciana',
            cep='59285-731',
            telefone='84 9172-9554',
        ),
    )

    perfil, _ = PerfilAcesso.objects.get_or_create(
        nome='Administrador',
        defaults=dict(
            permissoes=[
                'ver_alunos', 'criar_alunos', 'editar_alunos',
                'ver_financeiro', 'registrar_pagamento', 'excluir_pagamento',
                'registrar_graduacao', 'ver_relatorios',
                'gerenciar_convites', 'gerenciar_parametros', 'ver_dashboard', 'gerenciar_midia',
            ],
            is_admin=True,
        ),
    )

    Modalidade.objects.get_or_create(nome='JIUJITSU', defaults=dict(ativo=True))

    HorarioTreino.objects.get_or_create(
        descricao='Seg-Sex 20:00 - 21:00',
        defaults=dict(ativo=True),
    )

    for grau in range(5):
        GraduacaoParametro.objects.get_or_create(
            faixa='Branca', grau=grau,
            defaults=dict(meses_para_proxima_graduacao=6, ativo=True),
        )

    professor_user, _ = User.objects.get_or_create(
        username='anderson',
        defaults=dict(
            email='anderson@gmail.com',
            cpf='11111111111',
            first_name='Anderson Diego',
            last_name='da Silva Costa',
            role='professor',
            must_change_password=False,
            telefone='84991464250',
            filial=filial,
            faixa='Preta',
            grau=0,
        ),
    )
    if _:
        professor_user.set_password('anderson')
        professor_user.save()

    professor, created = Professor.objects.get_or_create(
        user=professor_user,
        defaults=dict(faixa='Preta', grau=0, perfil_acesso=perfil),
    )
    if created:
        professor.filiais.add(filial)

    horario = HorarioTreino.objects.filter(
        descricao='Seg-Sex 20:00 - 21:00'
    ).first()

    alunos_data = [
        dict(nome='João Miguel Santos', telefone='84911111111', email='joao@email.com'),
        dict(nome='Maria Clara Oliveira', telefone='84922222222', email='maria@email.com'),
        dict(nome='Pedro Henrique Lima', telefone='84933333333', email='pedro@email.com'),
        dict(nome='Ana Beatriz Souza', telefone='84944444444', email='ana@email.com'),
        dict(nome='Lucas Gabriel Costa', telefone='84955555555', email='lucas@email.com'),
    ]

    modalidade = Modalidade.objects.filter(nome='JIUJITSU').first()

    for i, data in enumerate(alunos_data):
        cpf_base = '10178415430'
        cpf = str(int(cpf_base) + i)
        aluno, created = Aluno.objects.get_or_create(
            cpf=cpf,
            defaults=dict(
                nome=data['nome'],
                data_nascimento=date(2000 + i, 1 + i % 12, 1 + i % 28),
                telefone=data['telefone'],
                email=data['email'],
                data_inicio=date(2026, 1, 1),
                faixa='Branca',
                grau=0,
                status='ativo',
                dia_vencimento=5,
                valor_mensalidade=Decimal('150.00'),
                filial=filial,
                horario_treino=horario,
            ),
        )
        if created and modalidade:
            aluno.modalidades = [modalidade.pk]
            aluno.save(update_fields=['modalidades'])
        nome_parts = data['nome'].split()
        user, _ = User.objects.get_or_create(
            username=cpf,
            defaults=dict(
                cpf=cpf,
                email=data['email'],
                first_name=nome_parts[0] if nome_parts else data['nome'],
                last_name=' '.join(nome_parts[1:]) if len(nome_parts) > 1 else '',
                role='aluno',
                must_change_password=True,
            ),
        )
        user.set_password(cpf)
        user.save(update_fields=['password'])

    return dict(filial=filial.nome, professor=professor_user.get_full_name(), alunos=5)


class Command(BaseCommand):
    help = 'Seed banco com dados iniciais (filial, parametros, professor, alunos)'

    def handle(self, *args, **options):
        result = run()
        self.stdout.write(self.style.SUCCESS(
            f"Filial: {result['filial']} | "
            f"Professor: {result['professor']} | "
            f"Alunos: {result['alunos']}"
        ))
