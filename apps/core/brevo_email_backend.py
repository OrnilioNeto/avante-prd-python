import json
import urllib.request
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address


class BrevoAPIEmailBackend(BaseEmailBackend):
    def __init__(self, api_key=None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = api_key or settings.BREVO_API_KEY

    def send_messages(self, email_messages):
        sent = 0
        for message in email_messages:
            if self._send(message):
                sent += 1
        return sent

    def _send(self, message):
        try:
            to = [{'email': sanitize_address(addr, 'utf-8')} for addr in message.to]
            payload = {
                'sender': {'email': 'avantebrazilianjj@gmail.com', 'name': 'Avante'},
                'to': to,
                'subject': message.subject,
                'textContent': message.body,
            }
            if message.alternatives:
                html = next((alt[0] for alt in message.alternatives if alt[1] == 'text/html'), None)
                if html:
                    payload['htmlContent'] = html
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                'https://api.brevo.com/v3/smtp/email',
                data=data,
                headers={
                    'api-key': self.api_key,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                method='POST',
            )
            resp = urllib.request.urlopen(req, timeout=30)
            return resp.status == 201
        except Exception:
            if self.fail_silently:
                return False
            raise
