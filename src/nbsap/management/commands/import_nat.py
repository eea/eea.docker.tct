import csv
import cStringIO, codecs
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from nbsap.models import (
    NationalObjective, NationalStrategy, EuTarget, EuAction, AichiTarget,
)


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


def _get_obj(model, code):
    qs = model.objects.filter(code=code).all()
    return qs and qs[0]


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = args and args[0]
        if not filename:
            self.stderr.write('Please provide a file name to import from')
            return

        # header = ['national_target_main_ref', 'description', 'eu_target',
        #           'global_targets', 'eu_actions']
        data = []
        with open(filename, 'r') as f:
            reader = UnicodeReader(f)
            reader.next()
            for row in reader:
                data.append(row)

        for row in data:
            nat_obj = NationalObjective.objects.create()
            nat_obj.title_en = row[0]
            nat_obj.description_en = row[1]
            nat_obj.save()
            strategy = NationalStrategy.objects.create(objective=nat_obj)
            eu_targets = row[2].split(',')
            for code in eu_targets:
                target = _get_obj(EuTarget, code)
                if not target:
                    self.stderr.write(
                        'No EuTarget found for code: {0}'.format(code))
                else:
                    target.national_strategy.add(strategy)
            global_targets = row[3].split(',')
            atarget = _get_obj(AichiTarget, global_targets[0])
            strategy.relevant_target = atarget
            global_targets = global_targets and global_targets[1:]
            for code in global_targets:
                atarget = _get_obj(AichiTarget, code)
                if not atarget:
                    self.stderr.write(
                        'No AichiTarget found for code: {0}'.format(code)
                    )
                else:
                    strategy.other_targets.add(atarget)
            strategy.save()
            eu_actions = row[4].split(',')
            for code in eu_actions:
                action = _get_obj(EuAction, code)
                if not action:
                    self.stderr.write(
                        'No EuAction found for code: {0}'.format(code)
                    )
                else:
                    action.national_strategy.add(strategy)
