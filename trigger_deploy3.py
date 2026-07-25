import requests, re, time

s = requests.Session()
resp = s.get('https://avante.pythonanywhere.com/login/')
match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text)
if not match:
    print('No CSRF')
    exit(1)
csrf = match.group(1)
time.sleep(1)
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf,
})
time.sleep(2)
print('Login URL:', login_resp.url)
if 'login' not in login_resp.url.lower():
    print('Logged in!')
    resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
    print('Deploy:', resp.status_code)
    print(resp.text[:3000])
else:
    print('Login failed')
