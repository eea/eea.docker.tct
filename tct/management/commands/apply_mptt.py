from django.core.management.base import BaseCommand
from django.conf import settings
from tct.models import EuAction, NationalObjective


class Command(BaseCommand):

    help = 'Apply mptt (a technique for storing hierarchical data in a database)'

    def handle(self, *args, **options):
        if settings.EU_STRATEGY:
            for action in EuAction.objects.exclude(parent__isnull=False):
                action._tree_manager.rebuild()
            self.stdout.write('Successfully applied mptt on EuAction')
        if settings.NAT_STRATEGY:
            for objective in NationalObjective.objects \
                    .exclude(parent__isnull=False):
                objective._tree_manager.rebuild()
            self.stdout.write('Successfully applied mptt on NationalObjective')
