import csv
import cStringIO, codecs
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from nbsap.models import NationalObjective


class UnicodeWriter:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = 'nat.csv'
        header = ['national_target_main_ref', 'description', 'eu_target',
                  'global_targets', 'eu_actions']
        data = [header]
        for nat_obj in NationalObjective.objects.all().order_by('code'):
            description = (
                BeautifulSoup(nat_obj.description_en).get_text()
                .replace("\n", " ").strip()
            )
            row = [nat_obj.title_en, description]
            strategy = nat_obj.objective_national_strategy.all()
            strategy = strategy and strategy[0]
            if not strategy:
                row.extend([''] * 3)
            else:
                row.append(
                    ','.join(
                        target.code for target in strategy.eu_targets.all()))
                row.append(
                    ','.join(
                        atarget.code for atarget in
                        [strategy.relevant_target] +
                        list(strategy.other_targets.all())
                    )
                )
                row.append(
                    ','.join(
                        action.code for action in strategy.eu_actions.all()))
            data.append(row)

        with open(filename, 'wb') as f:
            writer = UnicodeWriter(f)
            writer.writerows(data)

        self.stdout.write('{0} generated'.format(filename))
