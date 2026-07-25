from datetime import date, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from apps.alunos.models import Aluno, MensalidadePagamento, GraduacaoAluno


@login_required
def dashboard(request):
    user = request.user
    ctx = {}

    if user.is_superuser or user.role == 'super_admin':
        alunos = Aluno.objects.all()
    elif user.role == 'professor':
        try:
            filiais = user.professor_profile.filiais.all()
            alunos = Aluno.objects.filter(filial__in=filiais)
        except:
            alunos = Aluno.objects.none()
    else:
        alunos = Aluno.objects.filter(cpf=user.cpf)

    total_alunos = alunos.count()

    hoje = date.today()
    pagamentos_em_dia = MensalidadePagamento.objects.filter(
        aluno__in=alunos, pago_em__isnull=False
    ).values('aluno').distinct().count()

    pagamentos_atrasados = alunos.filter(
        ~Q(pagamentos__pago_em__isnull=False)
    ).count()

    ctx['total_alunos'] = total_alunos
    ctx['pagamentos_em_dia'] = pagamentos_em_dia
    ctx['pagamentos_atrasados'] = pagamentos_atrasados

    return render(request, 'core/dashboard.html', ctx)


@login_required
def minha_conta(request):
    user = request.user
    aluno = get_object_or_404(Aluno, cpf=user.cpf)
    hoje = date.today()

    pagamentos = MensalidadePagamento.objects.filter(aluno=aluno)
    ultimo_pagamento = pagamentos.order_by('-referencia_mes').first()
    pagamentos_em_atraso = pagamentos.filter(pago_em__isnull=True, vencimento_em__lt=hoje)
    pagamentos_em_dia = pagamentos.filter(pago_em__isnull=False)

    proximo_vencimento = None
    if aluno.dia_vencimento:
        mes = hoje.month
        ano = hoje.year
        if hoje.day > aluno.dia_vencimento:
            mes += 1
            if mes > 12:
                mes = 1
                ano += 1
        from datetime import date
        try:
            proximo_vencimento = date(ano, mes, aluno.dia_vencimento)
        except:
            pass

    graduacoes = GraduacaoAluno.objects.filter(aluno=aluno)

    return render(request, 'core/minha_conta.html', {
        'aluno': aluno,
        'pagamentos': pagamentos,
        'ultimo_pagamento': ultimo_pagamento,
        'pagamentos_em_atraso': pagamentos_em_atraso,
        'pagamentos_em_dia': pagamentos_em_dia,
        'proximo_vencimento': proximo_vencimento,
        'graduacoes': graduacoes,
    })


@staff_member_required
def deploy_view(request):
    import subprocess, os
    # Use repo root (two levels up from this file)
    repo_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output = []
    try:
        output.append('=== GIT RESET + CLEAN + PULL ===')
        r = subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=True, text=True, cwd=repo_root)
        output.append(r.stdout + r.stderr)
        r = subprocess.run(['git', 'clean', '-fd'], capture_output=True, text=True, cwd=repo_root)
        output.append(r.stdout + r.stderr)
        r = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd=repo_root)
        output.append(r.stdout + r.stderr)
        output.append('=== MIGRATE ===')
        call_command('migrate', '--noinput')
        output.append('=== COLLECTSTATIC ===')
        call_command('collectstatic', '--noinput', '--clear')
        output.append('=== TOUCH WSGI ===')
        subprocess.run(['touch', '/var/www/avante_pythonanywhere_com_wsgi.py'])
        output.append('=== DONE ===')
    except Exception as e:
        output.append(f'ERROR: {e}')
    return HttpResponse('<pre>' + '\n'.join(output) + '</pre>')