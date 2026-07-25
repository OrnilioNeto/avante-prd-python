import requests
resp = requests.get('https://www.pythonanywhere.com/user/avante/consoles/47590257/frame/',
    headers={'Authorization': 'Token c9312d3d5e06c089b7ca5e5b6cd3d6a7ccb64bfe'}
)
print(resp.status_code, len(resp.text))
import re
actions = re.findall(r'action="([^"]+)"', resp.text)
print('Actions:', actions[:10])
# Look for send-related endpoints
sends = re.findall(r'/send[^"]*', resp.text)
print('Send endpoints:', sends)
