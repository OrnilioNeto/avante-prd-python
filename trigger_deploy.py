import requests, re, time

s = requests.Session()

# Get login page for CSRF token
resp = s.get('https://avante.pythonanywhere.com/login/')
print('Login page:', resp.status_code)
match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', resp.text)
if not match:
    print('No CSRF token found')
    exit(1)

csrf = match.group(1)
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrf,
})
print('Login:', login_resp.status_code, login_resp.url)

time.sleep(1)

# Call deploy endpoint
resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
print('Deploy:', resp.status_code)
print(resp.text[:2000])
