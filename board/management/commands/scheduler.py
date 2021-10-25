from django.core.management.base import BaseCommand
from datetime import datetime
from board.open_api import put_data_to_api_table
from board.models import OpenApi


class Command(BaseCommand):
    def handle(self, *args, **options):
        i = 1
        date = datetime.now().date()
        while i < 5:
            put_data_to_api_table(date, i * 100)
            i += 1
