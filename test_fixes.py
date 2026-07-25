import requests, re, time

s = requests.Session()

# Check login page for correct static URLs
resp = s.get('https://avante.pythonanywhere.com/login/')
print('Login page loaded:', resp.status_code)

# Check logo URL
if '/static/image/avante.jpeg' in resp.text:
    print('Logo URL is absolute: OK')
else:
    # Find what the logo URL is
    match = re.search(r'src="([^"]*avante\.jpeg[^"]*)"', resp.text)
    if match:
        print('Logo URL found:', match.group(1))
    else:
        print('Logo URL not found in page')

# Check styles.css URL
if '/static/css/styles.css' in resp.text:
    print('Styles URL is absolute: OK')
else:
    match = re.search(r'href="([^"]*styles\.css[^"]*)"', resp.text)
    if match:
        print('Styles URL found:', match.group(1))

# Now login and check filiais
time.sleep(1)
csrf = re.search(r'csrfmiddlewaretoken" value="([^"]+)"', resp.text).group(1)
login_resp = s.post('https://avante.pythonanywhere.com/login/', data={
    'username': 'admin', 'password': 'admin', 'csrfmiddlewaretoken': csrf,
}, headers={'Referer': 'https://avante.pythonanywhere.com/login/'})

if 'login' not in login_resp.url.lower():
    print('Login: OK')
    
    # Access filiais
    filiais_resp = s.get('https://avante.pythonanywhere.com/filiais/')
    print(f'Filiais page: {filiais_resp.status_code}')
    if filiais_resp.status_code == 200:
        print('Filiais page loaded: OK')
    else:
        print(f'Filiais page error: {filiais_resp.text[:300]}')
else:
    print('Login failed')
