import csv
from django.core.management import BaseCommand
from board.models import Region


class Command(BaseCommand):
    help = "Loads products and product categories from CSV file."

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        with open(file_path, "r") as csv_file:
            data = list(csv.reader(csv_file, delimiter=","))
            region_list = [
                Region(
                    state=row[0],
                    city=row[1],
                    address=row[2],
                    code=row[3],
                )
                for row in data
            ]
            Region.objects.bulk_create(region_list)