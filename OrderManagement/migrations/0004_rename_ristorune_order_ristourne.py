# Generated by Django 5.1.2 on 2024-10-31 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0003_order_ristorune_order_total'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='ristorune',
            new_name='ristourne',
        ),
    ]