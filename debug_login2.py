import requests, re

s = requests.Session()

# Get admin login page
resp = s.get('https://avante.pythonanywhere.com/admin/login/')
print('GET admin login:', resp.status_code)
print('Cookies:', dict(s.cookies))

# Extract CSRF token
match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
if not match:
    print('No CSRF in admin page')
    # Search for any form
    forms = re.findall(r'<form[^>]*>', resp.text)
    print('Forms found:', len(forms))
    exit(1)

csrf = match.group(1)
print('CSRF from form:', csrf[:20])

# Also get the cookie token
cookie_csrf = s.cookies.get('csrftoken', '')
print('CSRF cookie:', cookie_csrf[:20])

# Login
login_resp = s.post('https://avante.pythonanywhere.com/admin/login/', data={
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrf,
    'next': '/admin/',
}, headers={'Referer': 'https://avante.pythonanywhere.com/admin/login/'})
print('POST login:', login_resp.status_code, login_resp.url)

if 'admin' in login_resp.url and 'login' not in login_resp.url:
    print('ADMIN LOGIN SUCCESS!')
    # Access deploy
    resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
    print('Deploy:', resp.status_code)
    print(resp.text[:3000])
else:
    print('Admin login failed')
    print('Response snippet:', login_resp.text[1000:2000])
