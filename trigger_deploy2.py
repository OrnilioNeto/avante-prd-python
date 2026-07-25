import requests, re

s = requests.Session()

# Get login page for CSRF token and cookie
resp = s.get('https://avante.pythonanywhere.com/login/')
print('GET login:', resp.status_code)
print('Cookies:', dict(s.cookies))

# Extract CSRF token from the login page
match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text)
if not match:
    print('No CSRF token found')
    # Try to find it in the form
    with open('login_page.html', 'w', encoding='utf-8') as f:
        f.write(resp.text)
    exit(1)

csrf = match.group(1)
print('CSRF:', csrf[:30])

# Login
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrf,
}, headers={'Referer': 'https://avante.pythonanywhere.com/login/'})
print('POST login:', login_resp.status_code, login_resp.url)
print('Login cookies:', dict(s.cookies))

print('Login URL:', login_resp.url)
if 'login' not in login_resp.url.lower():
    print('Login successful!')
    
    # Call deploy
    deploy_resp = s.get('https://avante.pythonanywhere.com/__deploy__/')
    print('Deploy:', deploy_resp.status_code)
    print(deploy_resp.text[:2000])
else:
    print('Login failed - still on login page')
