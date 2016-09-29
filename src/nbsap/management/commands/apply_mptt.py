from django.core.management.base import BaseCommand
from nbsap.models import EuAction, NationalObjective


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('table')

    def handle(self, *args, **options):
        if options['table'] == 'euaction':
            for action in EuAction.objects.exclude(parent__isnull=False):
                action._tree_manager.rebuild()
        if options['table'] == 'nationalobjective':
            for objective in NationalObjective.objects \
                    .exclude(parent__isnull=False):
                objective._tree_manager.rebuild()
