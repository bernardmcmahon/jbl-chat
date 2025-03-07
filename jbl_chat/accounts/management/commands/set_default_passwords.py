from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Used for adding default password to "admin" for all users that have no password set.'

    def handle(self, *args, **options):
        User = get_user_model()
        users = User.objects.exclude(password__startswith='pbkdf2_')
        count = 0
        for user in users:
            user.set_password('admin')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Password for user "{user.username}" changed to "admin"'))
            count += 1

        self.stdout.write(self.style.SUCCESS(f'\nTotal {count} users updated.'))