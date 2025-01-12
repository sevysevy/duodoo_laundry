# Generated by Django 5.1.2 on 2024-11-05 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0013_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='annomaly',
            field=models.CharField(choices=[('dechirure', 'Dechirure'), ('tache', 'Tache'), ('moisty', 'Moisissure')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='brand',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='color',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
