import csv
import cStringIO, codecs
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.conf import settings
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
    return (qs and qs[0]) or None


class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = args and args[0]
        if not filename:
            self.stderr.write('Please provide a file name to import from')
            return

        # cleanup, mandatory
        for nat_obj in NationalObjective.objects.all():
            nat_obj.delete()

        language = settings.LANGUAGE_CODE
        # header = ['national_target_main_ref', 'description', 'eu_target',
        #           'global_targets', 'eu_actions']
        data = []
        with open(filename, 'r') as f:
            reader = UnicodeReader(f, delimiter=';')
            header = reader.next()
            for row in reader:
                if header[0] == 'country':
                    row = row[1:]
                data.append(row)

        national_objectives = {}
        for row in data:
            obj_title = row[0]
            if obj_title == '':
                continue
            national_objectives.setdefault(obj_title, [])
            if row[1]:
                nat_sub_obj_title = row[1]
                national_objectives[obj_title].append(nat_sub_obj_title)

        imported_objectives = []
        for row in data:
            obj_title = row[0]
            if obj_title == '' or obj_title not in imported_objectives:
                # this is a new objective
                nat_obj = NationalObjective()
                setattr(nat_obj, 'title_' + language, obj_title)
                setattr(nat_obj, 'description_' + language, row[2])
                nat_obj.save()
                self.stdout.write(u'Imported objective {0}'.format(nat_obj))
                imported_objectives.append(obj_title)

            # add subobjectives only if there are at least 2 for the same objective
            if obj_title in national_objectives and len(national_objectives[obj_title]) > 1:
                nat_sub_obj = NationalObjective()
                setattr(nat_sub_obj, 'title_' + language, row[1])
                setattr(nat_sub_obj, 'description_' +  language, row[3])
                nat_sub_obj.parent = nat_obj
                nat_sub_obj.save()
                current_obj = nat_sub_obj
            else:
                # this is the objective for which the strategy and targets will be added
                current_obj = nat_obj

            strategy = NationalStrategy.objects.create(objective=current_obj)
            eu_targets = [c for c in row[4].split(',') if c]
            for code in eu_targets:
                target = _get_obj(EuTarget, code)
                if not target:
                    self.stderr.write(
                        'No EuTarget found for code: {0}'.format(code))
                else:
                    target.national_strategy.add(strategy)
                    target.save()
            global_targets = row[5].split(',')
            global_targets = [c for c in global_targets if c]
            for code in global_targets:
                atarget = _get_obj(AichiTarget, code)
                if not atarget:
                    self.stderr.write(
                        'No AichiTarget found for code: {0}'.format(code)
                    )
                else:
                    strategy.relevant_targets.add(atarget)
            strategy.save()
            eu_actions = [c for c in row[6].split(',') if c]
            for code in eu_actions:
                action = _get_obj(EuAction, code)
                if not action:
                    self.stderr.write(
                        'No EuAction found for code: {0}'.format(code)
                    )
                else:
                    action.national_strategy.add(strategy)
            self.stdout.write(u'Imported subojective {0}'.format(current_obj))
