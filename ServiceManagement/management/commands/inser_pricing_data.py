import csv
from django.core.management.base import BaseCommand
from FinanceManagement.models import ExpenseCategory
from ServiceManagement.models import Service, ItemCategory, ItemType, ItemCharacteristic, PriceList
from django.utils import timezone
from django.contrib.auth.models import User

from UserManagement.models import Agency, Role, UserProfile

# Replace with the path to your structured data file or adjust the logic to parse an in-memory object if available.
data_path = 'E:\Projects\duodoo_laundry\ServiceManagement\management\commands\Liste_grille_tarifaire_pressing_1.csv'

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
            "firstName" : "Yves",
            "lastName"  : "Admin",
            "phone" : "+237 656 431 945",
            "email" : "ngahsevy@gmail.com"
        }

        agency = {
            "name" : "Messamendongo",
            "adress" : "Messamendongo",
            "email"  : "info@crystalpressing.com",
            "phone" : "+237 695 13 77 10"
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
                email=user_data['email'],
                firstName=user_data['firstName'],
                lastName=user_data['lastName']
            )
        profile.user = user
        profile.role = Role.objects.get(name_code = "responsable")
        profile.save()

        serve_exp , _ = Service.objects.get_or_create(name="Express")
        # Load the Excel file
        with open(data_path, mode='r' , encoding='utf-8') as file:
            csv_reader = csv.reader(file , delimiter=';')
            next(csv_reader)
            for row in csv_reader:
                print(row)
                cat = row[1]
                v_type = row[0]
                caract = row[2]
                serv = row[3]
                price = row[4]
                ex_price = row[5]

                service , _ = Service.objects.get_or_create(name=serv)

        # Insert data into ItemCategory model
                cate , _ = ItemCategory.objects.get_or_create(name=cat)

                typ , _= ItemType.objects.get_or_create(name=v_type, category=cate)

                car , _= ItemCharacteristic.objects.get_or_create(name=caract)

                PriceList.objects.get_or_create(
                    service=serve_exp,
                    item_type=typ,
                    item_characteristic=car,
                    defaults={
                        "price": ex_price,
                        "active": True,
                        "created_at": timezone.now(),
                        "updated_at": timezone.now()
                    }
                )

                PriceList.objects.get_or_create(
                    service=service,
                    item_type=typ,
                    item_characteristic=car,
                    defaults={
                        "price": price,
                        "active": True,
                        "created_at": timezone.now(),
                        "updated_at": timezone.now()
                    }
                )


                
