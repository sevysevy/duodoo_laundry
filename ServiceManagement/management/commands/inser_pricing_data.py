import pandas as pd
from django.core.management.base import BaseCommand
from ServiceManagement.models import Service, ItemCategory, ItemType, ItemCharacteristic, PriceList
from django.utils import timezone

# Replace with the path to your structured data file or adjust the logic to parse an in-memory object if available.
data_path = 'C:/Users/ngahs/Desktop/Liste_grille_tarifaire_pressing.xlsx'

class Command(BaseCommand):
    help = "Inserts pricing data from an Excel file into the database."

    def handle(self, *args, **kwargs):
        # Load the Excel file
        excel_data = pd.ExcelFile(data_path)
        data_sheet2 = excel_data.parse('Grille tarifaire')

        # Rename columns as per earlier parsing instructions
        data_sheet2.rename(columns={'Catégorie': 'Type de vêtements', 'Type de vêtements': 'Catégorie'}, inplace=True)

        # Set to store unique entries for each model
        services = set()
        item_categories = set()
        item_types = set()
        item_characteristics = set()
        price_list_entries = []

        # Parse the data for each unique value
        for index, row in data_sheet2.iterrows():
            print(row)
            category_name = row['Catégorie']
            item_type_name = row['Type de vêtements']
            characteristic_name = row['Caractéristiques']
            service_name = row['Service']
            price = row['P.U']

            services.add(service_name)
            item_categories.add(category_name)
            item_types.add((item_type_name, category_name))
            item_characteristics.add(characteristic_name)
            price_list_entries.append({
                "service": service_name,
                "item_type": item_type_name,
                "item_category": category_name,
                "item_characteristic": characteristic_name,
                "price": price
            })

        # Insert data into Service model
        for service_name in services:
            Service.objects.get_or_create(name=service_name)

        # Insert data into ItemCategory model
        for category_name in item_categories:
            ItemCategory.objects.get_or_create(name=category_name)

        # Insert data into ItemType model
        for item_type_name, category_name in item_types:
            category = ItemCategory.objects.get(name=category_name)
            ItemType.objects.get_or_create(name=item_type_name, category=category)

        # Insert data into ItemCharacteristic model
        for characteristic_name in item_characteristics:
            ItemCharacteristic.objects.get_or_create(name=characteristic_name)

        # Insert data into PriceList model
        for entry in price_list_entries:
            service = Service.objects.get(name=entry["service"])
            item_type = ItemType.objects.get(name=entry["item_type"], category__name=entry["item_category"])
            item_characteristic = ItemCharacteristic.objects.get(name=entry["item_characteristic"])
            
            # Insert price list entry with unique combination
            PriceList.objects.get_or_create(
                service=service,
                item_type=item_type,
                item_characteristic=item_characteristic,
                defaults={
                    "price": entry["price"],
                    "active": True,
                    "created_at": timezone.now(),
                    "updated_at": timezone.now()
                }
            )

        self.stdout.write(self.style.SUCCESS("Pricing data inserted successfully."))
