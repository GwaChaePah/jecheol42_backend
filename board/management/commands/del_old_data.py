from django.core.management.base import BaseCommand
import datetime
from board.models import OpenApi


class Command(BaseCommand):
    def handle(self, *args, **options):
        date = datetime.datetime.now()
        del_date = date - datetime.timedelta(days=7)
        OpenApi.objects.filter(date__lte=del_date.date()).delete()
