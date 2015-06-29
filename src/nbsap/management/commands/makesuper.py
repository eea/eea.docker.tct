from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user_id = args and args[0]
        if not user_id:
            self.stderr.write('Please provide a user_id.')
            return

        try:
            User.objects.get(username=user_id)
        except User.DoesNotExist:
            User.objects.create_superuser(user_id, None, None)
            return
        print "The user_id already exists."
