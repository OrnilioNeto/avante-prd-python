from datetime import date, timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from apps.alunos.models import Aluno, MensalidadePagamento, GraduacaoAluno
from apps.midia.models import MidiaTreino
from apps.core.mixins import _user_is_admin


@login_required
def dashboard(request):
    user = request.user
    ctx = {}

    if user.role == 'aluno' and not _user_is_admin(user):
        return redirect('core:minha_conta')
    if user.role == 'professor':
        return redirect('core:professor_dashboard')
    if _user_is_admin(user):
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

    from django.db.models import Exists, OuterRef
    paid_exists = MensalidadePagamento.objects.filter(
        aluno=OuterRef('pk'), pago_em__isnull=False
    )
    pagamentos_atrasados = alunos.annotate(
        tem_pagamento=Exists(paid_exists)
    ).filter(tem_pagamento=False).count()

    ctx['total_alunos'] = total_alunos
    ctx['pagamentos_em_dia'] = pagamentos_em_dia
    ctx['pagamentos_atrasados'] = pagamentos_atrasados

    return render(request, 'core/dashboard.html', ctx)


@login_required
def upload_profile_photo(request):
    if request.method == 'POST' and request.FILES.get('profile_photo'):
        request.user.profile_photo = request.FILES['profile_photo']
        request.user.save(update_fields=['profile_photo'])
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def minha_conta(request):
    user = request.user
    aluno = get_object_or_404(Aluno, cpf=user.cpf)
    hoje = date.today()
    from django.db.models import Exists, OuterRef, Sum

    pagamentos = MensalidadePagamento.objects.filter(aluno=aluno)
    ultimo_pagamento = pagamentos.order_by('-referencia_mes').first()
    paid_for_same_month = MensalidadePagamento.objects.filter(
        aluno=OuterRef('aluno'),
        referencia_mes=OuterRef('referencia_mes'),
        pago_em__isnull=False,
    )
    pagamentos_em_atraso = pagamentos.filter(
        pago_em__isnull=True, vencimento_em__lt=hoje
    ).exclude(Exists(paid_for_same_month))
    pagamentos_em_dia = pagamentos.filter(pago_em__isnull=False)
    total_pago = pagamentos_em_dia.aggregate(total=Sum('valor'))['total'] or 0

    proximo_vencimento = None
    dia_venc = aluno.dia_vencimento or 5
    mes = hoje.month
    ano = hoje.year
    if hoje.day > dia_venc:
        mes += 1
        if mes > 12:
            mes = 1
            ano += 1
    from calendar import monthrange
    ultimo = monthrange(ano, mes)[1]
    try:
        proximo_vencimento = date(ano, mes, min(dia_venc, ultimo))
    except:
        pass

    graduacoes = GraduacaoAluno.objects.filter(aluno=aluno).order_by('-graduado_em')

    dias_desde_inicio = (hoje - aluno.data_inicio).days if aluno.data_inicio else 0
    meses_desde_ultima_grad = 0
    ult_grad = aluno.data_ultima_graduacao or aluno.data_inicio
    if ult_grad:
        meses_desde_ultima_grad = (hoje.year - ult_grad.year) * 12 + (hoje.month - ult_grad.month)

    prox_faixa = aluno.faixa
    prox_grau = 0
    progresso_grad = 0
    from apps.parametros.models import GraduacaoParametro
    FAIXAS_ORDER = ['Branca', 'Azul', 'Roxa', 'Marrom', 'Preta']
    try:
        param = GraduacaoParametro.objects.get(faixa=aluno.faixa, grau=aluno.grau, ativo=True)
        progresso_grad = min(100, int((meses_desde_ultima_grad / param.meses_para_proxima_graduacao) * 100))
        if aluno.grau >= 4:
            idx = FAIXAS_ORDER.index(aluno.faixa) if aluno.faixa in FAIXAS_ORDER else -1
            if idx != -1 and idx < len(FAIXAS_ORDER) - 1:
                prox_faixa = FAIXAS_ORDER[idx + 1]
                prox_grau = 0
            else:
                prox_faixa = aluno.faixa
                prox_grau = aluno.grau
        else:
            prox_faixa = aluno.faixa
            prox_grau = aluno.grau + 1
    except GraduacaoParametro.DoesNotExist:
        param = None

    xp = dias_desde_inicio * 10 + graduacoes.count() * 500 + pagamentos_em_dia.count() * 50
    nivel = xp // 1000 + 1
    xp_proximo_nivel = nivel * 1000
    xp_atual = xp
    xp_progresso = min(100, int((xp_atual % 1000) / 1000 * 100)) if xp_atual > 0 else 0

    ranking_data = _get_ranking(aluno)
    posicao = next((i+1 for i, (pk, _, _) in enumerate(ranking_data) if pk == aluno.pk), None)
    top3 = ranking_data[:3]
    ranking_count = len(ranking_data)

    return render(request, 'core/minha_conta.html', {
        'aluno': aluno,
        'pagamentos': pagamentos.order_by('-referencia_mes'),
        'ultimo_pagamento': ultimo_pagamento,
        'pagamentos_em_atraso': pagamentos_em_atraso,
        'pagamentos_em_dia': pagamentos_em_dia,
        'total_pago': total_pago,
        'proximo_vencimento': proximo_vencimento,
        'graduacoes': graduacoes,
        'dias_desde_inicio': dias_desde_inicio,
        'meses_desde_ultima_grad': meses_desde_ultima_grad,
        'param': param,
        'progresso_grad': progresso_grad,
        'prox_faixa': prox_faixa,
        'prox_grau': prox_grau,
        'nivel': nivel,
        'xp': xp,
        'xp_proximo_nivel': xp_proximo_nivel,
        'xp_progresso': xp_progresso,
        'posicao': posicao,
        'top3': top3,
        'ranking_count': ranking_count,
        'FAIXAS_ORDER': FAIXAS_ORDER,
        'midias': MidiaTreino.objects.filter(ativo=True)[:6],
    })


def _get_ranking(aluno=None):
    hoje = date.today()
    todos = Aluno.objects.filter(status='ativo')
    data = []
    for a in todos:
        pags = MensalidadePagamento.objects.filter(aluno=a, pago_em__isnull=False).count()
        grads = GraduacaoAluno.objects.filter(aluno=a).count()
        dias = (hoje - a.data_inicio).days if a.data_inicio else 0
        xp = dias * 10 + grads * 500 + pags * 50
        data.append((a.pk, a.nome, xp))
    data.sort(key=lambda x: x[2], reverse=True)
    return data


def _get_alunos_queryset(user):
    if _user_is_admin(user):
        return Aluno.objects.all()
    if user.role == 'professor':
        try:
            filiais = user.professor_profile.filiais.all()
            return Aluno.objects.filter(filial__in=filiais)
        except:
            return Aluno.objects.none()
    return Aluno.objects.filter(cpf=user.cpf)


@login_required
def professor_dashboard(request):
    user = request.user
    if user.role not in ('professor', 'super_admin') and not user.is_superuser:
        return render(request, 'core/dashboard.html', {'error': 'Acesso restrito a professores.'})
    from django.db.models import Sum, Exists, OuterRef

    alunos = _get_alunos_queryset(user).filter(status='ativo')
    hoje = date.today()
    mes_atual = date(hoje.year, hoje.month, 1)

    total_ativos = alunos.count()

    pagamentos_mes = MensalidadePagamento.objects.filter(
        aluno__in=alunos,
        referencia_mes=mes_atual,
    )
    em_dia = pagamentos_mes.filter(pago_em__isnull=False).count()

    paid_for_same_month = MensalidadePagamento.objects.filter(
        aluno=OuterRef('aluno'),
        referencia_mes=OuterRef('referencia_mes'),
        pago_em__isnull=False,
    )
    unpaid_valid = MensalidadePagamento.objects.filter(
        aluno__in=alunos,
        pago_em__isnull=True,
        vencimento_em__lt=hoje,
    ).exclude(Exists(paid_for_same_month))
    atrasados = unpaid_valid.values('aluno').distinct().count()

    receita_mes = pagamentos_mes.filter(pago_em__isnull=False).aggregate(
        total=Sum('valor')
    )['total'] or 0

    sem_pagamento = alunos.exclude(
        pk__in=pagamentos_mes.values('aluno')
    ).count()

    receita_prevista = alunos.aggregate(
        total=Sum('valor_mensalidade')
    )['total'] or 0

    top_atrasados = unpaid_valid.select_related('aluno', 'aluno__filial').order_by('vencimento_em')[:10]

    ultimos_alunos = alunos.order_by('-created_at')[:8]

    receita_meses = []
    for i in range(5, -1, -1):
        m = mes_atual.month - i
        y = mes_atual.year
        while m < 1:
            m += 12
            y -= 1
        ref = date(y, m, 1)
        total = MensalidadePagamento.objects.filter(
            aluno__in=alunos,
            referencia_mes=ref,
            pago_em__isnull=False,
        ).aggregate(total=Sum('valor'))['total'] or 0
        receita_meses.append({'mes': ref.strftime('%b/%Y'), 'total': float(total)})

    from apps.parametros.models import GraduacaoParametro
    prontos_graduar = []
    faixa_ordem = ['Branca','Azul','Roxa','Marrom','Preta']
    for aluno in alunos.filter(status='ativo'):
        ult_grad = aluno.data_ultima_graduacao or aluno.data_inicio
        if not ult_grad:
            continue
        meses_desde = (hoje.year - ult_grad.year) * 12 + (hoje.month - ult_grad.month)
        try:
            param = GraduacaoParametro.objects.get(
                faixa=aluno.faixa,
                grau=aluno.grau,
                ativo=True,
            )
            if meses_desde >= param.meses_para_proxima_graduacao:
                faixa_idx = faixa_ordem.index(aluno.faixa) if aluno.faixa in faixa_ordem else -1
                if aluno.grau >= 4 and faixa_idx != -1 and faixa_idx < len(faixa_ordem) - 1:
                    prox_faixa = faixa_ordem[faixa_idx + 1]
                    prox_grau = 0
                else:
                    prox_faixa = aluno.faixa
                    prox_grau = aluno.grau + 1
                prontos_graduar.append({
                    'aluno': aluno,
                    'proxima_faixa': prox_faixa,
                    'proximo_grau': prox_grau,
                    'meses_passados': meses_desde,
                    'meses_necessarios': param.meses_para_proxima_graduacao,
                })
        except GraduacaoParametro.DoesNotExist:
            pass
    prontos_graduar.sort(key=lambda x: x['meses_passados'], reverse=True)

    return render(request, 'core/professor_dashboard.html', {
        'total_ativos': total_ativos,
        'em_dia': em_dia,
        'atrasados': atrasados,
        'sem_pagamento': sem_pagamento,
        'receita_mes': receita_mes,
        'receita_prevista': receita_prevista,
        'top_atrasados': top_atrasados,
        'ultimos_alunos': ultimos_alunos,
        'receita_meses': receita_meses,
        'prontos_graduar': prontos_graduar[:10],
    })


@login_required
def mensalidades_atrasadas(request):
    user = request.user
    if user.role not in ('professor', 'super_admin') and not user.is_superuser:
        from django.http import Http404; raise Http404()
    from django.db.models import Sum, Exists, OuterRef

    alunos = _get_alunos_queryset(user)
    hoje = date.today()

    paid_for_same_month = MensalidadePagamento.objects.filter(
        aluno=OuterRef('aluno'),
        referencia_mes=OuterRef('referencia_mes'),
        pago_em__isnull=False,
    )
    pagamentos = MensalidadePagamento.objects.filter(
        aluno__in=alunos,
        pago_em__isnull=True,
        vencimento_em__lt=hoje,
    ).exclude(Exists(paid_for_same_month)).select_related('aluno', 'aluno__filial').order_by('vencimento_em')

    filial_id = request.GET.get('filial')
    mes_ref = request.GET.get('mes')

    if filial_id:
        pagamentos = pagamentos.filter(aluno__filial_id=filial_id)
    if mes_ref:
        try:
            ano, mes = int(mes_ref[:4]), int(mes_ref[5:7])
            pagamentos = pagamentos.filter(
                referencia_mes__year=ano, referencia_mes__month=mes
            )
        except (ValueError, IndexError):
            pass

    total_atrasado = pagamentos.aggregate(total=Sum('aluno__valor_mensalidade'))['total'] or 0
    qtd_atrasados = pagamentos.values('aluno').distinct().count()

    from apps.filiais.models import Filial
    filiais = Filial.objects.filter(
        pk__in=alunos.values_list('filial', flat=True).distinct()
    )

    return render(request, 'core/mensalidades_atrasadas.html', {
        'pagamentos': pagamentos[:100],
        'total_atrasado': total_atrasado,
        'qtd_atrasados': qtd_atrasados,
        'filiais': filiais,
        'filial_id': int(filial_id) if filial_id else None,
        'mes_ref': mes_ref,
        'hoje': hoje,
    })


@login_required
def financeiro(request):
    user = request.user
    if user.role not in ('professor', 'super_admin') and not user.is_superuser:
        from django.http import Http404; raise Http404()
    from django.db.models import Sum

    alunos = _get_alunos_queryset(user)
    hoje = date.today()
    mes_atual = date(hoje.year, hoje.month, 1)

    meses = []
    for i in range(11, -1, -1):
        m = mes_atual.month - i
        y = mes_atual.year
        while m < 1:
            m += 12
            y -= 1
        ref = date(y, m, 1)
        pagamentos = MensalidadePagamento.objects.filter(
            aluno__in=alunos,
            referencia_mes=ref,
        )
        recebido = pagamentos.filter(pago_em__isnull=False).aggregate(t=Sum('valor'))['t'] or 0
        pendente = pagamentos.filter(pago_em__isnull=True).aggregate(t=Sum('valor'))['t'] or 0
        meses.append({
            'mes': ref.strftime('%b/%Y'),
            'referencia': ref,
            'recebido': float(recebido),
            'pendente': float(pendente),
            'total': float(recebido) + float(pendente),
            'recebido_int': int(recebido),
            'pendente_int': int(pendente),
            'total_int': int(recebido) + int(pendente),
        })

    from apps.filiais.models import Filial
    filiais = Filial.objects.filter(
        pk__in=alunos.values_list('filial', flat=True).distinct()
    )
    resumo_filiais = []
    for filial in filiais:
        qtd = alunos.filter(filial=filial).count()
        total_mensalidades = alunos.filter(filial=filial).aggregate(
            t=Sum('valor_mensalidade')
        )['t'] or 0
        resumo_filiais.append({
            'filial': filial,
            'qtd_alunos': qtd,
            'receita_prevista': float(total_mensalidades),
        })

    receita_total_ano = MensalidadePagamento.objects.filter(
        aluno__in=alunos,
        referencia_mes__year=hoje.year,
        pago_em__isnull=False,
    ).aggregate(t=Sum('valor'))['t'] or 0

    pendente_total = MensalidadePagamento.objects.filter(
        aluno__in=alunos,
        pago_em__isnull=True,
        vencimento_em__lt=hoje,
    ).aggregate(t=Sum('valor'))['t'] or 0

    total_receita_filiais = sum(item['receita_prevista'] for item in resumo_filiais)

    return render(request, 'core/financeiro.html', {
        'meses': meses,
        'resumo_filiais': resumo_filiais,
        'receita_total_ano': receita_total_ano,
        'pendente_total': pendente_total,
        'total_alunos': alunos.count(),
        'total_receita_filiais': total_receita_filiais,
    })


@staff_member_required
def test_email(request):
    import traceback, os
    from django.conf import settings as s
    from django.core.mail import send_mail, EmailMessage
    from django.core.mail.backends.smtp import EmailBackend
    from pathlib import Path
    lines = []
    lines.append(f'os.environ EMAIL_BACKEND: {os.environ.get("EMAIL_BACKEND", "not set")}')
    lines.append(f'settings EMAIL_BACKEND: {s.EMAIL_BACKEND}')
    lines.append(f'settings EMAIL_HOST: {s.EMAIL_HOST}')
    lines.append(f'settings EMAIL_PORT: {s.EMAIL_PORT}')
    lines.append(f'settings EMAIL_HOST_USER: {s.EMAIL_HOST_USER}')
    lines.append(f'settings EMAIL_USE_TLS: {s.EMAIL_USE_TLS}')
    lines.append(f'settings DEFAULT_FROM_EMAIL: {s.DEFAULT_FROM_EMAIL}')
    to_email = request.GET.get('to', 'avantebrazilianjj@gmail.com')
    from apps.accounts.models import User
    has_user = User.objects.filter(email=to_email).exists()
    lines.append(f'Usuario com email {to_email}: {"SIM" if has_user else "NAO"}')
    lines.append(f'--- Tentando enviar email via EMAIL_BACKEND atual ---')
    try:
        send_mail('Teste Avante', 'Teste de envio via backend configurado.', None, [to_email], fail_silently=False)
        lines.append('EMAIL ENVIADO COM SUCESSO!')
    except Exception as e:
        lines.append(f'ERRO: {type(e).__name__}: {e}')
    return HttpResponse('<pre>' + '\n'.join(lines) + '</pre>')


@staff_member_required
def deploy_view(request):
    import subprocess, os
    from pathlib import Path
    repo_root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output = []
    is_authorized = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)
    secret = request.GET.get('token', '')
    deploy_secret = os.environ.get('DEPLOY_SECRET', '')
    if not is_authorized and (not secret or not deploy_secret or secret != deploy_secret):
        return redirect('/login/?next=/__deploy__/')
    try:
        output.append('=== WRITE .ENV ===')
        env_path = str(Path(repo_root) / '.env')
        env_vars = {
            'EMAIL_BACKEND': 'apps.core.brevo_email_backend.BrevoAPIEmailBackend',
            'DEFAULT_FROM_EMAIL': 'avante <avantebrazilianjj@gmail.com>',
        }
        brevo_api_key = request.GET.get('brevo_api_key') or os.environ.get('BREVO_API_KEY', '')
        if brevo_api_key:
            env_vars['BREVO_API_KEY'] = brevo_api_key
        with open(env_path, 'w') as f:
            for k, v in env_vars.items():
                if any(c in v for c in ' @#$%^&*()=!'):
                    f.write(f'{k}="{v}"\n')
                else:
                    f.write(f'{k}={v}\n')
        output.append(f'.env criado com {len(env_vars)} variaveis')
        output.append('=== GIT RESET + CLEAN + PULL ===')
        r = subprocess.run(['git', 'reset', '--hard', 'HEAD'], capture_output=True, text=True, cwd=repo_root)
        output.append(r.stdout + r.stderr)
        r = subprocess.run(['git', 'clean', '-fd'], capture_output=True, text=True, cwd=repo_root)
        output.append(r.stdout + r.stderr)
        r = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd=repo_root)
        output.append(r.stdout + r.stderr)
        output.append('=== PIP INSTALL ===')
        venv_pip = os.path.join(repo_root, 'venv', 'bin', 'pip')
        if os.path.exists(venv_pip):
            r = subprocess.run([venv_pip, 'install', '-r', os.path.join(repo_root, 'requirements.txt')], capture_output=True, text=True, cwd=repo_root)
            output.append((r.stdout + r.stderr)[-500:])
        else:
            output.append('venv pip nao encontrado, tentando pip3')
            r = subprocess.run(['pip3', 'install', '-r', os.path.join(repo_root, 'requirements.txt')], capture_output=True, text=True, cwd=repo_root)
            output.append((r.stdout + r.stderr)[-500:])
        if request.GET.get('reset'):
            output.append('=== RESET DB ===')
            call_command('flush', '--noinput')
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            if not UserModel.objects.filter(username='admin').exists():
                UserModel.objects.create_superuser('admin', 'admin@avante.com', 'admin')
            admin_user = UserModel.objects.filter(username='admin').first()
            if admin_user and admin_user.must_change_password:
                admin_user.must_change_password = False
                admin_user.save(update_fields=['must_change_password'])
            output.append('Superuser admin/admin criado')
        output.append('=== MIGRATE ===')
        call_command('migrate', '--noinput')
        if request.GET.get('reset'):
            output.append('=== SEED ===')
            try:
                call_command('seed')
                output.append('Seed concluido')
            except Exception as e:
                output.append(f'Seed error: {e}')
        output.append('=== CLEANUP DUPLICATE PAYMENTS ===')
        from django.db.models import Exists, OuterRef
        from apps.alunos.models import MensalidadePagamento
        paid = MensalidadePagamento.objects.filter(
            aluno=OuterRef('aluno'),
            referencia_mes=OuterRef('referencia_mes'),
            pago_em__isnull=False,
        )
        qs = MensalidadePagamento.objects.filter(pago_em__isnull=True).filter(Exists(paid))
        deleted, _ = qs.delete()
        output.append(f'Registros duplicados removidos: {deleted}')
        output.append('=== COLLECTSTATIC ===')
        call_command('collectstatic', '--noinput', '--clear')
        output.append('=== WRITE .ENV (pos-pull) ===')
        env_path = str(Path(repo_root) / '.env')
        with open(env_path, 'w') as f:
            for k, v in env_vars.items():
                if any(c in v for c in ' @#$%^&*()=!'):
                    f.write(f'{k}="{v}"\n')
                else:
                    f.write(f'{k}={v}\n')
        output.append('.env recriado apos git clean')
        output.append('=== TOUCH WSGI ===')
        subprocess.run(['touch', '/var/www/avante_pythonanywhere_com_wsgi.py'])
        output.append('=== DONE ===')
    except Exception as e:
        output.append(f'ERROR: {e}')
        import traceback
        output.append(traceback.format_exc())
    return HttpResponse('<pre>' + '\n'.join(output) + '</pre>')