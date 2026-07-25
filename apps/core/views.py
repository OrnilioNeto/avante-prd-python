from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')


@staff_member_required
def deploy_view(request):
    import subprocess, os
    output = []
    try:
        output.append('=== GIT PULL ===')
        r = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd=os.path.dirname(__file__))
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