# Generated by Django 5.1.2 on 2024-10-31 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0005_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]
