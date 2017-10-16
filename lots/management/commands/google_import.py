# Requirements:
# - pip install gspread oauth2client
from django.core.management.base import BaseCommand
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from lots.models import Lot, LotType, Contact
from revenue.models import Receipt, Fee


class Command(BaseCommand):
    help = 'Import lots from a .csv file'

    def handle(self, *args, **options):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        self.import_mantenimiento(client)
        exit(0)
        self.delete_all()
        self.import_vecinos(client)

    def delete_all(self):
        Receipt.objects.all().delete()
        Fee.objects.all().delete()
        Contact.objects.all().delete()
        Lot.objects.all().delete()

    def import_mantenimiento(self, client):
        sheet = client.open("R/ I-E MANTENIMIENTO.xlsx").worksheet("ene-17")

        # Extract and print all of the values
        records = sheet.get_all_records(head=5)
        print(records)

    def import_vecinos(self, client):
        sheet = client.open("Vecinos y sugerencias").worksheet("DATOS DE RESIDENTES")

        # Extract and print all of the values
        records = sheet.get_all_records()

        casa = LotType.objects.get(name='Casa')
        lote = LotType.objects.get(name='Lote')

        for row in records:
            if row['M'] in ['', 'M', '0']:
                continue

            lot = Lot(name='M' + str(row['M']).zfill(2) + '-L' + str(row['L']).zfill(2), address=row['Dirección'])
            if row['Tipo'] == 'Casa':
                lot.lot_type = casa
            else:
                lot.lot_type = lote

            if row['MASCOTAS'] != '':
                lot.details = 'Mascotas: ' + row['MASCOTAS']

            if row['PROPIETARIOS'].strip() != '':
                contact, created = Contact.objects.get_or_create(
                    name__exact=row['PROPIETARIOS'],
                    defaults={'name': row['PROPIETARIOS']}
                )
                if row['CELULAR'] != '':
                    contact.phone_number = row['CELULAR']
                if row['PROFESION EL'] != '':
                    contact.details = 'Porfesión: ' + row['PROFESION EL']
                contact.save()
                lot.owner = contact

            # we need to save lots so we can save many-to-many associations
            lot.save()

            if row['ARRENDATARIOS'].strip() != '':
                values = row['ARRENDATARIOS'].split(' - ')
                contact, created = Contact.objects.get_or_create(
                    name__exact=values[0],
                    defaults={'name': values[0], 'details': 'Arrendatario'}
                )
                if len(values) > 1:
                    contact.phone_number = values[1]
                contact.save()
                lot.contacts.add(contact)

            if row['ESPOSA (O)'].strip() != '':
                contact, created = Contact.objects.get_or_create(
                    name__exact=row['ESPOSA (O)'],
                    defaults={'name': row['ESPOSA (O)']}
                )
                if row['PROFESION ELLA'] != '':
                    contact.details = 'Porfesión: ' + row['PROFESION ELLA']
                contact.save()
                lot.contacts.add(contact)