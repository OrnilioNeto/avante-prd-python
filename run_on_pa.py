import requests
import time
import json

TOKEN = 'c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe'
USER = 'avante'
BASE = f'https://www.pythonanywhere.com/api/v0/user/{USER}'
HEADERS = {'Authorization': f'Token {TOKEN}', 'Accept': 'application/json'}

# Create a new bash console
resp = requests.post(
    f'{BASE}/consoles/',
    headers=HEADERS,
    json={'executable': 'bash', 'arguments': ''}
)
if resp.status_code != 201:
    print(f'Failed to create console: {resp.status_code} {resp.text[:300]}')
    exit(1)

console = resp.json()
console_id = console['id']
print(f'Console {console_id} created')

def send_cmd(console_id, cmd):
    resp = requests.post(
        f'{BASE}/consoles/{console_id}/send/',
        headers=HEADERS,
        json={'input': cmd + '\n'}
    )
    print(f'Sent: {cmd} -> {resp.status_code}')
    time.sleep(3)
    # Get output
    resp = requests.get(
        f'{BASE}/consoles/{console_id}/',
        headers=HEADERS
    )
    if resp.status_code == 200:
        data = resp.json()
        output = data.get('output', '')
        if output:
            print(output[:800])

# commands to run
cmds = [
    'cd /home/avante/avante-prd-python',
    'source venv/bin/activate',
    'python manage.py migrate --noinput 2>&1',
    'python manage.py collectstatic --noinput 2>&1',
    'touch /var/www/avante_pythonanywhere_com_wsgi.py',
]

for cmd in cmds:
    send_cmd(console_id, cmd)

print('Done!')

# Clean up
requests.post(
    f'{BASE}/consoles/{console_id}/send/',
    headers=HEADERS,
    json={'input': 'exit\n'}
)
