from django.core.management.base import BaseCommand, CommandError
from reservations_list.models import Reservation

import os
import csv
import glob

csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), '*.csv')
csv_files = glob.glob(csv_dir)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for file in csv_files:
            with open(file) as fp:
                reader = csv.DictReader(fp)
                for row in reader:
                    if row:
                        reservation = Reservation.objects.create(
                            number=row['number'],
                            arrival=row['arrival'],
                            departure=row['departure'],
                            name=row['name'],
                            phone=row['phone'],
                            email=row['email'],
                            no_of_people=row['no_of_people'],
                            status=row['status']
                        )
                    reservation.save()
