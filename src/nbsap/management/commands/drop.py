from django.conf import settings
from django.conf import settings

from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Drop and re-create the database"
    def handle_noargs(self, **options):
        import MySQLdb
        print "Connecting..."

        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd = "root",
                             port=int(settings.DATABASES['default']['PORT'] or 3306))

        cursor = db.cursor()
        print "Dropping database %s" % settings.DATABASES['default']['NAME']
        cursor.execute("drop database %s;" % (settings.DATABASES['default']['NAME']))
        print "Dropped"

        print 'Creating database ...'
        cursor.execute("create database %s DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;" % (settings.DATABASES['default']['NAME']))
        print "Created"

        db.commit()

        print "Granting privileges ..."
        cursor.execute("grant all on nbsap.* to nbsap@localhost identified by 'nbsap';")
        db.commit()
        print 'Successfully granted privileges.'
