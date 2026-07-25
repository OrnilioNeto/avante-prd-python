import requests, re

s = requests.Session()

# Get CSRF
resp = s.get('https://avante.pythonanywhere.com/login/')
print('Session cookies:', dict(s.cookies))

match = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text)
csrf = match.group(1)
print('CSRF:', csrf[:20])

# Actually check if there's an error div already
if 'invalid' in resp.text.lower():
    print('Already has error on GET?!')

# Login POST
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrf,
}, allow_redirects=False)
print('POST status:', login_resp.status_code)
print('POST URL:', login_resp.url)
print('Location header:', login_resp.headers.get('Location'))
print('Cookies after POST:', dict(s.cookies))

# Check response body for error messages
if 'inv' in login_resp.text.lower() or 'erro' in login_resp.text.lower():
    # Find error messages
    errors = re.findall(r'(?:invalido|erro|error)[^<]*', login_resp.text, re.I)
    print('Error snippets:', errors[:5])

# The login form has 'Usuário e senha inválidos' message
if 'inv' in login_resp.text:
    print('Login form shows invalid credentials')
