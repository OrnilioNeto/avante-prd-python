import requests, re, time

s = requests.Session()

# Login via admin
resp = s.get('https://avante.pythonanywhere.com/admin/login/')
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
login_resp = s.post('https://avante.pythonanywhere.com/admin/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf, 'next': '/admin/',
}, headers={'Referer': 'https://avante.pythonanywhere.com/admin/login/'})

if 'login' not in login_resp.url.lower():
    print('Admin login: OK')
    
    # Call deploy
    time.sleep(1)
    deploy_resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
    print('Deploy:', deploy_resp.status_code)
    print(deploy_resp.text[:2000])
    
    # Now check filiais
    time.sleep(1)
    filiais_resp = s.get('https://avante.pythonanywhere.com/filiais/')
    print(f'Filiais: {filiais_resp.status_code}')
    if filiais_resp.status_code == 200:
        print('Filiais page: OK')
    else:
        print(f'Filiais error body: {filiais_resp.text[:300]}')
else:
    print('Login failed')
