# Generated by Django 5.1.2 on 2024-10-29 19:55

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCharacteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PriceList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_characteristic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_entries', to='ServiceManagement.itemcharacteristic')),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_entries', to='ServiceManagement.itemtype')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_entries', to='ServiceManagement.service')),
            ],
            options={
                'unique_together': {('service', 'item_type', 'item_characteristic')},
            },
        ),
    ]