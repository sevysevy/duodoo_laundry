import csv
from django.core.management.base import BaseCommand
from FinanceManagement.models import ExpenseCategory
from ServiceManagement.models import Service, ItemCategory, ItemType, ItemCharacteristic, PriceList
from django.utils import timezone
from django.contrib.auth.models import User

from UserManagement.models import Agency, Role, UserProfile

# Replace with the path to your structured data file or adjust the logic to parse an in-memory object if available.
data_path = 'E:\Projects\duodoo_laundry\ServiceManagement\management\commands\Liste_grille_tarifaire_pressing.csv'

class Command(BaseCommand):
    help = "Inserts pricing data from an Excel file into the database."

    def handle(self, *args, **kwargs):

        data_role = [
                {"name":"Administrateur" ,"desc_role":"Ce type de compte donne un accès totale a la plateforme.", "name_code":"admin" },
                {"name":"Responsable" , "desc_role":"Ce type de compte est réservé aux responsables d’organisation de la société civile", "name_code":"responsable"},
                {"name":"Customer" , "desc_role":"Ce type de compte est réservé aux clients", "name_code":"costumer"},
                
                ]
        
        user_data = {
            "password" : "123456789",
            "firstName" : "Vanessa",
            "lastName"  : "Atangana",
            "phone" : "+237 690 92 27 47",
            "email" : "vanessa@gmail.com"
        }

        agency = {
            "name" : "Obam - Repos du Chef",
            "adress" : "Repos du Chef",
            "email"  : "info@crystalpressing.com",
            "phone" : "+237 690 92 27 47"
        }

        depense = [
            "Facture Eau" , "Facture Electricite" , "Transport" , "Achat Divers" , "Autres"
        ]


        for elm in depense:
            print(elm)
            ExpenseCategory.objects.create(name = elm)

        for rle in data_role:
            print(rle)
            role = Role.objects.create(name = rle["name"]  , name_code = rle["name_code"]  , desc_role = rle["desc_role"])

        agency = Agency.objects.create( name = agency["name"] , address = agency['adress'] , email = agency['email']  , phone = agency["phone"])


        user = User(
                username=user_data['email'],
                email=user_data['email'],
                first_name=user_data['firstName'],
                last_name=user_data['lastName']
            )
        user.set_password(user_data['password'])
        user.save()

            # Save the UserProfile and link it to the User
        profile = UserProfile(
                username=user_data['email'],
                email=user_data['email'],
                firstName=user_data['firstName'],
                lastName=user_data['lastName']
            )
        profile.user = user
        profile.role = Role.objects.get(name_code = "responsable")
        profile.save()


        # Load the Excel file
        with open(data_path, mode='r' , encoding='utf-8') as file:
            csv_reader = csv.reader(file , delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                cat = row[1]
                v_type = row[0]
                caract = row[2]
                serv = row[3]
                price = row[4]

                service = Service.objects.get_or_create(name=serv)

        # Insert data into ItemCategory model
                cate = ItemCategory.objects.get_or_create(name=cat)

                typ = ItemType.objects.get_or_create(name=v_type, category=cate)

                car = ItemCharacteristic.objects.get_or_create(name=caract)

                PriceList.objects.get_or_create(
                    service=service,
                    item_type=typ,
                    item_characteristic=caract,
                    defaults={
                        "price": price,
                        "active": True,
                        "created_at": timezone.now(),
                        "updated_at": timezone.now()
                    }
                )


                print(row)

        """ excel_data = pd.ExcelFile(data_path)
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

        self.stdout.write(self.style.SUCCESS("Pricing data inserted successfully.")) """
