import requests

TOKEN = 'c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe'
USER = 'avante'
BASE = f'https://www.pythonanywhere.com/api/v0/user/{USER}'
HEADERS = {'Authorization': f'Token {TOKEN}', 'Accept': 'application/json'}

# Upload a migration script
script_content = '''#!/bin/bash
cd /home/avante/avante-prd-python
source venv/bin/activate
python manage.py migrate --noinput 2>&1
python manage.py collectstatic --noinput 2>&1
'''

resp = requests.post(
    f'{BASE}/files/path/home/avante/migrate.sh/',
    headers=HEADERS,
    files={'content': ('migrate.sh', script_content.encode(), 'text/plain')}
)
print(f'Upload script: {resp.status_code}')

# Create a scheduled task to run it
resp = requests.post(
    f'{BASE}/schedule/',
    headers=HEADERS,
    json={
        'command': 'bash /home/avante/migrate.sh',
        'interval': 'once',
        'enabled': True,
    }
)
print(f'Schedule: {resp.status_code} {resp.text[:300]}')

# Trigger a webapp reload
resp = requests.post(
    f'{BASE}/webapps/avante.pythonanywhere.com/reload/',
    headers=HEADERS,
)
print(f'Reload: {resp.status_code} {resp.text[:300]}')
