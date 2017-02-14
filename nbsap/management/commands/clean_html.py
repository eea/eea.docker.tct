from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from nbsap.utils import remove_tags
from nbsap.models import NationalObjective


class Command(BaseCommand):

    def handle(self, *args, **options):
        for nat_obj in NationalObjective.objects.all():
            print nat_obj.id
            nat_obj.description_en = remove_tags(
                BeautifulSoup(nat_obj.description_en).prettify())
            nat_obj.save()
