import requests, re, time

s = requests.Session()

# 1. Check login page static URLs
resp = s.get('https://avante.pythonanywhere.com/login/')
print(f'Login page: {resp.status_code}')

logo_url = None
match = re.search(r'src="([^"]*avante\.jpeg[^"]*)"', resp.text)
if match:
    logo_url = match.group(1)
    print(f'Logo URL: {logo_url}')
    if logo_url.startswith('/static/'):
        print('  -> Absolute path: OK')

match = re.search(r'href="([^"]*styles\.css[^"]*)"', resp.text)
if match:
    css_url = match.group(1)
    print(f'Styles URL: {css_url}')

# 2. Actually fetch the logo to verify it serves
if logo_url:
    logo_resp = requests.get(f'https://avante.pythonanywhere.com{logo_url}')
    print(f'Logo fetch: {logo_resp.status_code} ({len(logo_resp.content)} bytes)')

# 3. Login via admin
resp = s.get('https://avante.pythonanywhere.com/admin/login/')
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
s.post('https://avante.pythonanywhere.com/admin/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf, 'next': '/admin/',
}, headers={'Referer': 'https://avante.pythonanywhere.com/admin/login/'})

# 4. Check normal login
resp = s.get('https://avante.pythonanywhere.com/login/')
csrf = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf,
}, headers={'Referer': 'https://avante.pythonanywhere.com/login/'})
print(f'Normal login URL: {login_resp.url}')

if 'login' not in login_resp.url.lower():
    # 5. Access filiais
    time.sleep(1)
    filiais_resp = s.get('https://avante.pythonanywhere.com/filiais/')
    print(f'Filiais: {filiais_resp.status_code} - {"OK" if filiais_resp.status_code == 200 else "FAIL"}')
    
    # 6. Access convites
    convites_resp = s.get('https://avante.pythonanywhere.com/convites/')
    print(f'Convites: {convites_resp.status_code} - {"OK" if convites_resp.status_code == 200 else "FAIL"}')
else:
    print('Login failed')
