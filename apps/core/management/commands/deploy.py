from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run migrations and collectstatic for deploy'

    def handle(self, *args, **options):
        self.stdout.write('Running migrations...')
        call_command('migrate', '--noinput')
        self.stdout.write('Collecting static files...')
        call_command('collectstatic', '--noinput', '--clear')
        self.stdout.write('Deploy complete!')
