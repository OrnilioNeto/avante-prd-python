import os
import requests

BASE = r'C:\Users\Ornilio Neto\Documents\projetos\avante-python'
TOKEN = 'c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe'
USER = 'avante'
API = f'https://www.pythonanywhere.com/api/v0/user/{USER}/files/path'

FILES = [
    'apps/convites/models.py',
    'apps/convites/views.py',
    'apps/convites/urls.py',
    'apps/alunos/models.py',
    'apps/alunos/views.py',
    'apps/alunos/urls.py',
    'apps/core/views.py',
    'apps/core/urls.py',
    'templates/convites/convite_list.html',
    'templates/convites/convite_form.html',
    'templates/convites/convite_register.html',
    'templates/alunos/aluno_detail.html',
    'apps/convites/migrations/0002_convitealuno_max_uses_convitealuno_use_count.py',
    'apps/alunos/migrations/0002_aluno_dia_vencimento_aluno_valor_mensalidade.py',
]

API_URL = 'https://www.pythonanywhere.com/api/v0/user/avante/files/path'
HEADERS = {'Authorization': f'Token {TOKEN}'}

PA_BASE = '/home/avante/avante-prd-python'

for f in FILES:
    local = os.path.join(BASE, f)
    remote_path = f'{PA_BASE}/{f}'
    
    with open(local, 'rb') as fh:
        content = fh.read()
    
    resp = requests.post(
        f'{API_URL}{remote_path}/',
        headers=HEADERS,
        files={'content': ('file.py', content, 'text/plain')},
    )
    
    if resp.status_code in (200, 201):
        print(f'OK: {f}')
    else:
        print(f'FAIL ({resp.status_code}): {f} -> {resp.text[:200]}')

print('All files uploaded.')
