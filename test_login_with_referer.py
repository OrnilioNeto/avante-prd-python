import requests, re

s = requests.Session()

# First get login page to get CSRF
resp = s.get('https://avante.pythonanywhere.com/login/')
csrf = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
print('CSRF obtained')

# Login with proper Referer
login_resp = s.post(
    'https://avante.pythonanywhere.com/login/',
    data={
        'username': 'admin',
        'password': 'admin',
        'csrfmiddlewaretoken': csrf,
    },
    headers={'Referer': 'https://avante.pythonanywhere.com/login/'},
    allow_redirects=False
)
print(f'Status: {login_resp.status_code}')
print(f'Location: {login_resp.headers.get("Location")}')
print(f'Cookies: {dict(s.cookies)}')

if login_resp.status_code in (302, 301):
    print('LOGIN SUCCESS (redirect)')
    # Follow redirect
    dashboard = s.get('https://avante.pythonanywhere.com/')
    print(f'Dashboard: {dashboard.status_code}')
    
    # Now access filiais
    filiais = s.get('https://avante.pythonanywhere.com/filiais/')
    print(f'Filiais: {filiais.status_code}')
    if filiais.status_code == 200:
        # Check if it's the actual page or a redirect to login
        if 'login' not in filiais.url.lower():
            print('Filiais page loaded OK')
        else:
            print('Redirected to login (not authenticated)')
    else:
        print(f'Filiais error: {filiais.text[:500]}')
elif login_resp.status_code == 403:
    print('CSRF or Referer issue')
    print(f'Response preview: {login_resp.text[1500:2500]}')
else:
    print(f'Unexpected status: {login_resp.status_code}')
    # Check if login failed with form error
    if 'inv' in login_resp.text:
        print('Login form shows invalid credentials')
