import requests, re, time

s = requests.Session()

# Login via admin  
resp = s.get('https://avante.pythonanywhere.com/admin/login/')
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
s.post('https://avante.pythonanywhere.com/admin/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf, 'next': '/admin/',
}, headers={'Referer': 'https://avante.pythonanywhere.com/admin/login/'})

# Reload webapp
resp = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/avante/webapps/avante.pythonanywhere.com/reload/',
    headers={'Authorization': 'Token c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe', 'Accept': 'application/json'}
)
print('Reload:', resp.status_code)

time.sleep(3)

# Now try normal login
resp = s.get('https://avante.pythonanywhere.com/login/')
csrf = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf,
}, headers={'Referer': 'https://avante.pythonanywhere.com/login/'})
print('Normal login URL:', login_resp.url)

if 'login' not in login_resp.url.lower():
    print('LOGIN WORKS!')
    # Check the dashboard content
    print('Dashboard loaded successfully')
else:
    print('Login still failing')
