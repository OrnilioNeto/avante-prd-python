import requests, time, datetime

TOKEN = 'c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe'
USER = 'avante'
BASE = f'https://www.pythonanywhere.com/api/v0/user/{USER}'
HEADERS = {'Authorization': f'Token {TOKEN}', 'Accept': 'application/json'}

# Upload a clean migration script
script = '#!/bin/bash\n'
script += 'cd /home/avante/avante-prd-python\n'
script += 'source venv/bin/activate\n'
script += 'echo "=== MIGRATE ===" >> /home/avante/deploy.log\n'
script += 'python manage.py migrate --noinput >> /home/avante/deploy.log 2>&1\n'
script += 'echo "=== COLLECTSTATIC ===" >> /home/avante/deploy.log\n'
script += 'python manage.py collectstatic --noinput >> /home/avante/deploy.log 2>&1\n'
script += 'echo "=== DONE ===" >> /home/avante/deploy.log\n'

resp = requests.post(
    f'{BASE}/files/path/home/avante/run_migrate.sh/',
    headers=HEADERS,
    files={'content': ('run_migrate.sh', script.encode(), 'text/plain')}
)
print('Upload script:', resp.status_code)

# Schedule it for the next minute
now = datetime.datetime.utcnow()
minute = (now.minute + 2) % 60

resp = requests.post(
    f'{BASE}/schedule/',
    headers=HEADERS,
    json={
        'command': 'bash /home/avante/run_migrate.sh',
        'enabled': True,
        'interval': 'hourly',
        'hour': '*',
        'minute': str(minute),
        'description': 'Deploy migration'
    }
)
print('Schedule:', resp.status_code, resp.text[:500])
if resp.status_code == 201:
    task = resp.json()
    task_id = task.get('id')
    print(f'Scheduled task {task_id} for minute {minute}')
    
    # Wait for it to execute
    print('Waiting for task to run...')
    time.sleep(150)  # wait 2.5 minutes
    
    # Check the log
    resp = requests.get(
        f'{BASE}/files/path/home/avante/deploy.log/',
        headers=HEADERS
    )
    print('Log:', resp.status_code)
    if resp.status_code == 200:
        print(resp.text[:1000])
    
    # Delete the task
    if task_id:
        resp = requests.delete(f'{BASE}/schedule/{task_id}/', headers=HEADERS)
        print('Delete task:', resp.status_code)
