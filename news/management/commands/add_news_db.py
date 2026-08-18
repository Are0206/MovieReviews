import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from news.models import News


class Command(BaseCommand):
    help = "Carga 5 noticias del dataset Fake.csv en la base de datos"

    def handle(self, *args, **options):
        csv_path = os.path.join(os.path.dirname(__file__), 'Fake.csv')

        if not os.path.exists(csv_path):
            self.stderr.write(f"No se encontró el archivo: {csv_path}")
            return

        News.objects.all().delete()

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for i, row in enumerate(reader):
                if i >= 5:
                    break

                date_value = datetime.strptime(
                    row['date'].strip(),
                    '%B %d, %Y'
                ).date()

                News.objects.create(
                    headline=row['title'].strip()[:200],
                    body=row['text'].strip(),
                    date=date_value,
                )

                self.stdout.write(f"Noticia agregada: {row['title'][:60]}")

        self.stdout.write(self.style.SUCCESS("¡5 noticias cargadas correctamente!"))