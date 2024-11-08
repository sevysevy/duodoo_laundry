# Generated by Django 5.1.2 on 2024-11-06 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0017_remove_order_anormaly_remove_order_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='balance',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='anormaly',
            field=models.CharField(choices=[('Dechirure', 'Dechirure'), ('Tache', 'Tache'), ('Moisissure', 'Moisissure'), ('Teinte', 'Teinte'), ('Delaver', 'Delaver')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='base_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderlineitem',
            name='line_total',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
