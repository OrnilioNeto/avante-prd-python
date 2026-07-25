import requests, time, json

TOKEN = 'c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe'
USER = 'avante'
BASE = f'https://www.pythonanywhere.com/api/v0/user/{USER}'
HEADERS = {'Authorization': f'Token {TOKEN}', 'Accept': 'application/json'}

# Use existing console
console_id = 47590257

def send_and_wait(cmd, wait=5):
    resp = requests.post(
        f'{BASE}/consoles/{console_id}/send_input/',
        headers=HEADERS,
        data={'input': cmd + '\n'}
    )
    print(f'Send {resp.status_code}: {cmd}')
    time.sleep(wait)
    resp = requests.get(f'{BASE}/consoles/{console_id}/get_latest_output/', headers=HEADERS)
    if resp.status_code == 200:
        print(resp.text[:600])
    return resp

cmds = [
    'cd /home/avante/avante-prd-python',
    'source venv/bin/activate',
    'python manage.py migrate --noinput 2>&1',
    'python manage.py collectstatic --noinput 2>&1',
    'touch /var/www/avante_pythonanywhere_com_wsgi.py',
]

for cmd in cmds:
    send_and_wait(cmd)
