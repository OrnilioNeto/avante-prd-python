import requests, re, time

s = requests.Session()

# Try Django admin login
resp = s.get('https://avante.pythonanywhere.com/admin/login/')
print('Admin login page:', resp.status_code)

# Look for CSRF token
match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text)
if match:
    csrf = match.group(1)
    login_resp = s.post('https://avante.pythonanywhere.com/admin/login/', data={
        'username': 'admin',
        'password': 'admin',
        'csrfmiddlewaretoken': csrf,
        'next': '/admin/',
    })
    print('Admin login:', login_resp.status_code, login_resp.url)
    
    if '/admin/' in login_resp.url:
        print('Admin login SUCCESS!')
        # Now try to access deploy endpoint
        resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
        print('Deploy:', resp.status_code)
        print(resp.text[:3000])
    else:
        print('Admin login failed')
        print(login_resp.text[:500])
else:
    print('No CSRF in admin login page')
    print(resp.text[:500])
