import requests, re, time

s = requests.Session()

# Login
resp = s.get('https://avante.pythonanywhere.com/login/')
match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text)
csrf = match.group(1)

login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrf,
})
time.sleep(1)

print('Login URL:', login_resp.url)

if 'login' not in login_resp.url.lower():
    print('LOGGED IN!')
    
    # Call deploy
    resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
    print('Deploy:', resp.status_code)
    print(resp.text[:3000])
else:
    print('Login failed')
    # Debug: check if there's an error message
    if 'inv' in login_resp.text.lower():
        import re
        errors = re.findall(r'class="[^"]*error[^"]*"[^>]*>([^<]+)', login_resp.text, re.I)
        print('Errors:', errors)
